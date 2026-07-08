#!/usr/bin/env python3
"""
run_eval.py
===========
Evaluation harness for the Carebot model matrix.

Conditions are (model endpoint) x (RAG on/off). For each condition this harness:
  1. generate — runs all 554 eval inputs (yac_eval.jsonl) through the model
     (RAG conditions retrieve MMR k=3 from rag_store/ and inject context using the
     exact format carebot_app.py uses), writing responses to
     eval_results/responses_<condition>.jsonl (+ a Colab-compatible CSV whose
     Answer/Response columns match the repo's BLEURT/metrics scripts).
  2. score — reference-based metrics on the 500 synthetic_heldout records, matching
     the repo's evaluation.py exactly: BERTScore-F1 (bert-base-uncased), BLEU
     (sentence_bleu with duplicated reference), ROUGE-L (stemmer), plus METEOR.
  3. judge — LLM-judge rubric (GLM 5.2 serverless, reasoning off, temp 0) on the
     54 dang_real records (no gold reply -> reference-free).
  4. report — aggregates every condition into eval_results/eval_report.md.

Usage:
  python run_eval.py generate --condition base_rag  --model accounts/fireworks/models/gemma-3-27b-it --rag
  python run_eval.py generate --condition ft_only   --model accounts/yacchatbot/models/carebot-gemma3-27b-v1
  python run_eval.py score    --condition ft_only
  python run_eval.py judge    --condition ft_only
  python run_eval.py report

All steps are resumable; generation checkpoints per-record.
BLEURT is intentionally NOT run here (done later on Colab from the CSVs).
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import random
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(HERE / ".hf_cache"))
import nltk  # noqa: E402
nltk.data.path.insert(0, str(HERE / ".nltk_data"))

import httpx  # noqa: E402

# ---- config --------------------------------------------------------------------------
EVAL_PATH = HERE / "yac_eval.jsonl"
STORE_PATH = HERE / "rag_store"
OUT_DIR = HERE / "eval_results"
API_BASE = "https://api.fireworks.ai/inference/v1"
ENV_PATH = HERE / ".env"
GEN_TEMPERATURE = 0.3          # low variance for fair cross-condition comparison
GEN_MAX_TOKENS = 400
CONCURRENCY = 6
MAX_RETRIES = 6
JUDGE_MODEL = "accounts/fireworks/models/glm-5p2"
RAG_K, RAG_FETCH_K = 3, 12     # matches app + store manifest

CAREBOT_SYSTEM_PROMPT = (
    "You are Carebot, a warm, empathic, supportive assistant. You speak kindly and "
    "clearly, avoid medical or legal claims, and focus on practical, everyday help. "
    "Reflect feelings, validate, suggest small steps and resources, and encourage "
    "seeking trusted adults or professionals when appropriate. Keep answers concise "
    "but caring."
)
# v2 (context-leak fix): the original app phrasing let the model attribute retrieved
# first-person caregiver passages to the CURRENT user (e.g. "your POH GGZ support").
# v2 labels each block by kind and adds an explicit non-attribution instruction.
RAG_SUFFIX = (
    "\n\nBackground context retrieved for you (use only if relevant):\n{context}\n\n"
    "IMPORTANT: blocks marked \"another caregiver's experience\" are things OTHER "
    "people said in past interviews — they are NOT about the current user. Never "
    "assume the user has said, done, or received anything mentioned there. Use them "
    "only as background insight into how caregivers in similar situations feel or "
    "cope. Blocks marked \"guide\" are excerpts from information documents.")

JUDGE_RUBRIC = """You are evaluating a reply from "Carebot", a support companion for young adult caregivers (18-25). The INPUT is a real caregiver's statement; the REPLY is Carebot's response.

Score the REPLY 1-5 on each dimension (5 = excellent):
- empathy: does it genuinely acknowledge the caregiver's feelings without being hollow or over-gushing?
- practicality: does it offer concrete, actionable, appropriate help (or appropriately just listen)?
- safety: does it avoid medical/legal claims and point to professionals/trusted people when warranted?
- direction: does it speak AS a supportive companion TO the caregiver (5), not as a caregiver venting or an interviewer probing (1)?
- human_tone: does it read like a warm human, not a formulaic AI (penalize template-y structure, robotic phrasing)?

Return ONLY JSON: {"empathy": n, "practicality": n, "safety": n, "direction": n, "human_tone": n, "overall": n, "note": "<one sentence>"}"""


def load_env() -> str:
    for line in ENV_PATH.read_text().splitlines():
        if line.strip() and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    key = os.environ.get("FIREWORKS_API_KEY")
    if not key:
        raise SystemExit("FIREWORKS_API_KEY missing")
    return key


def load_eval() -> list[dict]:
    return [json.loads(l) for l in EVAL_PATH.open() if l.strip()]


# ---- retrieval (lazy: only loaded for --rag) ------------------------------------------
_retriever = None
def get_retriever():
    global _retriever
    if _retriever is None:
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
        manifest = json.loads((STORE_PATH / "store_manifest.json").read_text())
        emb = HuggingFaceEmbeddings(
            model_name=manifest["embedding_model"],
            encode_kwargs={"normalize_embeddings": manifest["normalize_embeddings"]})
        _retriever = FAISS.load_local(str(STORE_PATH), emb,
                                      allow_dangerous_deserialization=True)
    return _retriever


def format_docs(docs) -> str:
    # v2: label each block by kind (leak fix); original repo format was "[i] content".
    blocks = []
    for i, d in enumerate(docs, start=1):
        if d.metadata.get("type") == "yac_interview":
            blocks.append(f"[{i}] (another caregiver's experience) {d.page_content}")
        else:
            src = d.metadata.get("source", "guide")
            blocks.append(f"[{i}] (guide: {src}) {d.page_content}")
    return "\n\n".join(blocks)


# ---- generation ----------------------------------------------------------------------
async def _chat(client: httpx.AsyncClient, payload: dict) -> str | None:
    for attempt in range(MAX_RETRIES):
        try:
            r = await client.post("/chat/completions", json=payload, timeout=180)
        except (httpx.TimeoutException, httpx.TransportError):
            await asyncio.sleep(min(60, 2 ** attempt + random.random()))
            continue
        if r.status_code == 200:
            try:
                return r.json()["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return None
        if r.status_code == 429 or r.status_code >= 500:
            retry_after = float(r.headers.get("retry-after", 0) or 0)
            await asyncio.sleep(max(retry_after, min(60, 2 ** attempt + random.random())))
            continue
        print(f"[warn] HTTP {r.status_code}: {r.text[:200]}")
        return None
    return None


async def generate(condition: str, model: str, use_rag: bool) -> None:
    key = load_env()
    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"responses_{condition}.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(l)["id"] for l in out_path.open() if l.strip()}
        print(f"[resume] {len(done)} responses already present")
    recs = [r for r in load_eval() if r["metadata"]["id"] not in done]
    print(f"{condition}: generating {len(recs)} responses "
          f"(model={model}, rag={use_rag})")

    retr = get_retriever() if use_rag else None
    sem = asyncio.Semaphore(CONCURRENCY)
    out_fh = out_path.open("a", buffering=1)
    n_done = 0
    t0 = time.time()

    async with httpx.AsyncClient(
            base_url=API_BASE,
            headers={"Authorization": f"Bearer {key}"}) as client:

        async def one(rec: dict):
            nonlocal n_done
            user_text = rec["messages"][1]["content"]
            system = CAREBOT_SYSTEM_PROMPT
            ctx = ""
            if retr is not None:
                docs = retr.max_marginal_relevance_search(
                    user_text, k=RAG_K, fetch_k=RAG_FETCH_K)
                ctx = format_docs(docs)
                system = CAREBOT_SYSTEM_PROMPT + RAG_SUFFIX.format(context=ctx)
            payload = {
                "model": model,
                "messages": [{"role": "system", "content": system},
                             {"role": "user", "content": user_text}],
                "temperature": GEN_TEMPERATURE,
                "max_tokens": GEN_MAX_TOKENS,
            }
            async with sem:
                reply = await _chat(client, payload)
            if reply is None:
                print(f"[fail] {rec['metadata']['id']}")
                return
            gold = (rec["messages"][2]["content"]
                    if len(rec["messages"]) > 2 else "")
            out_fh.write(json.dumps({
                "id": rec["metadata"]["id"],
                "eval_source": rec["metadata"].get("eval_source", ""),
                "category": rec["metadata"].get("category", ""),
                "context_used": ctx,
                "user": user_text,
                "gold": gold,
                "answer": reply.strip(),
            }, ensure_ascii=False) + "\n")
            n_done += 1
            if n_done % 50 == 0:
                rate = n_done / (time.time() - t0)
                print(f"  {n_done}/{len(recs)}  ({rate:.1f}/s)")

        await asyncio.gather(*(one(r) for r in recs))
    out_fh.close()

    # Colab-compatible CSV (Answer=candidate, Response=reference), like repo scripts.
    rows = [json.loads(l) for l in out_path.open() if l.strip()]
    with (OUT_DIR / f"responses_{condition}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "eval_source", "category",
                                           "Context", "Response", "Answer"])
        w.writeheader()
        for r in sorted(rows, key=lambda x: x["id"]):
            w.writerow({"id": r["id"], "eval_source": r["eval_source"],
                        "category": r["category"], "Context": r["user"],
                        "Response": r["gold"], "Answer": r["answer"]})
    print(f"done: {len(rows)} responses -> {out_path.name} + .csv")


# ---- reference-based scoring (repo-matching) ------------------------------------------
def score(condition: str) -> None:
    import pandas as pd
    from bert_score import BERTScorer
    from nltk.translate.bleu_score import sentence_bleu
    from nltk.translate.meteor_score import meteor_score
    from nltk import word_tokenize
    from rouge_score import rouge_scorer as rs

    rows = [json.loads(l) for l in (OUT_DIR / f"responses_{condition}.jsonl").open()
            if l.strip()]
    rows = [r for r in rows if r["eval_source"] == "synthetic_heldout" and r["gold"]]
    print(f"{condition}: scoring {len(rows)} synthetic_heldout responses")

    pattern = re.compile(r"[^A-Za-z0-9 '’]")   # same normalizer as repo evaluation.py
    scorer_b = BERTScorer(model_type="bert-base-uncased")
    scorer_r = rs.RougeScorer(["rougeL"], use_stemmer=True)

    cands = [r["answer"] for r in rows]
    golds = [r["gold"] for r in rows]
    _, _, F1 = scorer_b.score(cands, golds)     # batched BERTScore

    recs = []
    for r, f1 in zip(rows, F1.tolist()):
        cand_toks = re.sub(pattern, "", r["answer"]).split()
        gold_toks = re.sub(pattern, "", r["gold"]).split()
        try:    # repo style: reference duplicated
            bleu = sentence_bleu([gold_toks, gold_toks], cand_toks)
        except Exception:
            bleu = 0.0
        rouge_l = scorer_r.score(r["answer"], r["gold"])["rougeL"].fmeasure
        try:
            meteor = meteor_score([word_tokenize(r["gold"])],
                                  word_tokenize(r["answer"]))
        except Exception:
            meteor = 0.0
        recs.append({"id": r["id"], "category": r["category"],
                     "BERTScore": f1, "BLEU": bleu, "ROUGE-L": rouge_l,
                     "METEOR": meteor})
    df = pd.DataFrame(recs)
    df.to_csv(OUT_DIR / f"scores_{condition}.csv", index=False)
    summary = df[["BERTScore", "BLEU", "ROUGE-L", "METEOR"]].mean().to_dict()
    (OUT_DIR / f"scores_{condition}_summary.json").write_text(
        json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


# ---- LLM judge on dang_real ------------------------------------------------------------
async def judge(condition: str) -> None:
    key = load_env()
    rows = [json.loads(l) for l in (OUT_DIR / f"responses_{condition}.jsonl").open()
            if l.strip()]
    rows = [r for r in rows if r["eval_source"] == "dang_real"]
    out_path = OUT_DIR / f"judge_{condition}.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(l)["id"] for l in out_path.open() if l.strip()}
    rows = [r for r in rows if r["id"] not in done]
    print(f"{condition}: judging {len(rows)} dang_real responses")

    sem = asyncio.Semaphore(CONCURRENCY)
    out_fh = out_path.open("a", buffering=1)
    async with httpx.AsyncClient(
            base_url=API_BASE,
            headers={"Authorization": f"Bearer {key}"}) as client:

        async def one(r: dict):
            payload = {
                "model": JUDGE_MODEL,
                "messages": [
                    {"role": "system", "content": JUDGE_RUBRIC},
                    {"role": "user",
                     "content": f"INPUT (caregiver): {r['user']}\n\n"
                                f"REPLY (Carebot): {r['answer']}"}],
                "temperature": 0.0,
                "max_tokens": 300,
                "reasoning_effort": "none",
            }
            async with sem:
                verdict = await _chat(client, payload)
            if not verdict:
                return
            m = re.search(r"\{.*\}", verdict, re.DOTALL)
            if not m:
                return
            try:
                parsed = json.loads(m.group(0))
            except json.JSONDecodeError:
                return
            parsed["id"] = r["id"]
            out_fh.write(json.dumps(parsed, ensure_ascii=False) + "\n")

        await asyncio.gather(*(one(r) for r in rows))
    out_fh.close()
    print(f"judged -> {out_path.name}")


# ---- aggregate report -------------------------------------------------------------------
def report() -> None:
    import pandas as pd
    lines = ["# Carebot Evaluation Report", ""]
    conds = sorted({p.stem.replace("scores_", "").replace("_summary", "")
                    for p in OUT_DIR.glob("scores_*_summary.json")})
    if conds:
        lines += ["## Reference-based metrics (500 synthetic held-out)",
                  "", "| Condition | BERTScore | BLEU | ROUGE-L | METEOR |",
                  "|---|---:|---:|---:|---:|"]
        for c in conds:
            s = json.loads((OUT_DIR / f"scores_{c}_summary.json").read_text())
            lines.append(f"| {c} | {s['BERTScore']:.4f} | {s['BLEU']:.4f} "
                         f"| {s['ROUGE-L']:.4f} | {s['METEOR']:.4f} |")
        lines.append("")
    jconds = sorted(p.stem.replace("judge_", "") for p in OUT_DIR.glob("judge_*.jsonl"))
    if jconds:
        dims = ["empathy", "practicality", "safety", "direction", "human_tone", "overall"]
        lines += ["## LLM-judge rubric (54 real Dang inputs, 1-5)",
                  "", "| Condition | " + " | ".join(dims) + " |",
                  "|---|" + "---:|" * len(dims)]
        for c in jconds:
            df = pd.DataFrame([json.loads(l) for l in
                               (OUT_DIR / f"judge_{c}.jsonl").open() if l.strip()])
            lines.append("| " + c + " | " +
                         " | ".join(f"{df[d].mean():.2f}" for d in dims) + " |")
        lines.append("")
    bleurt_summary = HERE / "bleurt_scores" / "bleurt_summary.csv"
    if bleurt_summary.exists():
        import csv as _csv
        rows = list(_csv.DictReader(bleurt_summary.open()))
        lines += ["## BLEURT-20 (500 synthetic held-out; scored on Colab)",
                  "", "| Condition | n | BLEURT |", "|---|---:|---:|"]
        for r in sorted(rows, key=lambda x: -float(x["BLEURT_mean"])):
            lines.append(f"| {r['condition']} | {r['n']} | {float(r['BLEURT_mean']):.4f} |")
        lines += ["",
                  "_Note: BLEURT ranks baseline highest and FT variants lowest — the opposite "
                  "of BERTScore/ROUGE-L. Reference metrics disagree with each other and with "
                  "human review (which preferred ft_only); human judgment is primary._"]
    else:
        lines.append("_BLEURT: run separately on Colab from responses_<condition>.csv "
                     "(Answer vs Response columns)._")
    findings = OUT_DIR / "findings.md"
    if findings.exists():
        lines += ["", findings.read_text().rstrip()]
    (OUT_DIR / "eval_report.md").write_text("\n".join(lines) + "\n")
    print((OUT_DIR / "eval_report.md").read_text())


# ---- cli -----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--condition", required=True)
    g.add_argument("--model", required=True)
    g.add_argument("--rag", action="store_true")
    s = sub.add_parser("score")
    s.add_argument("--condition", required=True)
    j = sub.add_parser("judge")
    j.add_argument("--condition", required=True)
    sub.add_parser("report")
    a = ap.parse_args()
    if a.cmd == "generate":
        asyncio.run(generate(a.condition, a.model, a.rag))
    elif a.cmd == "score":
        score(a.condition)
    elif a.cmd == "judge":
        asyncio.run(judge(a.condition))
    else:
        report()


if __name__ == "__main__":
    main()
