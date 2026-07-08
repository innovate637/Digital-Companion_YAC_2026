#!/usr/bin/env python3
"""
run_eval_v3_gate.py
===================
Spliced evaluation of GATED retrieval (ft_rag_v3) — validates the design shipped in
carebot_app_leakfix_gate.patch without regenerating all 554 responses.

By construction, queries where the gate keeps nothing produce prompts identical to
ft_only, so their ft_only responses are reused verbatim (gate_fired=false). Only
queries whose gate fires (cos >= GATE_COS after self-hit exclusion) are generated
fresh against the deployed tuned model with the labeled-context v2 prompt.

Self-hit exclusion: the 54 dang_real eval inputs are themselves store passages
(distance ~0). Production users are never in the store, so self-hits are dropped
before gating to keep the eval production-faithful.

Usage:
  python run_eval_v3_gate.py plan                      # offline: gate decisions + contexts
  python run_eval_v3_gate.py generate --model <route>  # deployment: gated subset only
  python run_eval_v3_gate.py splice                    # assemble responses_ft_rag_v3.jsonl|csv
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(HERE / ".hf_cache"))

import run_eval  # reuse harness: prompts, chat client, env loading

GATE_COS = 0.60
FETCH_K = 12
K = 3
SELF_HIT_DIST = 0.05           # drop store hits that ARE the query (dang eval inputs)
PLAN_PATH = HERE / "eval_results" / "v3_gate_plan.json"
OUT_JSONL = HERE / "eval_results" / "responses_ft_rag_v3.jsonl"
OUT_CSV = HERE / "eval_results" / "responses_ft_rag_v3.csv"
FT_ONLY_PATH = HERE / "eval_results" / "responses_ft_only.jsonl"


def plan() -> None:
    """Offline: for each eval record, decide gate + build labeled context."""
    retr = run_eval.get_retriever()
    evals = run_eval.load_eval()
    items = []
    fired = 0
    for r in evals:
        q = r["messages"][1]["content"]
        hits = retr.similarity_search_with_score(q, k=FETCH_K)
        hits = [(d, dist) for d, dist in hits if dist > SELF_HIT_DIST]
        kept = [d for d, dist in hits if (1 - dist ** 2 / 2) >= GATE_COS][:K]
        ctx = run_eval.format_docs(kept) if kept else ""
        best_cos = max((1 - float(dist) ** 2 / 2) for _, dist in hits) if hits else 0.0
        fired += bool(kept)
        items.append({"id": r["metadata"]["id"], "gate_fired": bool(kept),
                      "best_cos": round(best_cos, 3), "n_chunks": len(kept),
                      "context": ctx})
    PLAN_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=1))
    print(f"plan: {fired}/{len(items)} queries fire the gate "
          f"({100*fired/len(items):.0f}%) -> {PLAN_PATH.name}")


async def generate(model: str) -> None:
    """Generate responses ONLY for gate-fired queries, resumable."""
    run_eval.load_env()
    plan_items = {p["id"]: p for p in json.loads(PLAN_PATH.read_text())}
    evals = {r["metadata"]["id"]: r for r in run_eval.load_eval()}
    todo = [pid for pid, p in plan_items.items() if p["gate_fired"]]
    part_path = HERE / "eval_results" / "responses_ft_rag_v3.partial.jsonl"
    done = set()
    if part_path.exists():
        done = {json.loads(l)["id"] for l in part_path.open() if l.strip()}
    todo = [t for t in todo if t not in done]
    print(f"generating {len(todo)} gated responses (resume skipped {len(done)})")

    import httpx
    sem = asyncio.Semaphore(run_eval.CONCURRENCY)
    out = part_path.open("a", buffering=1)
    key = os.environ["FIREWORKS_API_KEY"]
    async with httpx.AsyncClient(base_url=run_eval.API_BASE,
                                 headers={"Authorization": f"Bearer {key}"}) as client:
        async def one(pid: str):
            rec, p = evals[pid], plan_items[pid]
            system = run_eval.CAREBOT_SYSTEM_PROMPT + run_eval.RAG_SUFFIX.format(
                context=p["context"])
            payload = {"model": model,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user",
                                     "content": rec["messages"][1]["content"]}],
                       "temperature": run_eval.GEN_TEMPERATURE,
                       "max_tokens": run_eval.GEN_MAX_TOKENS}
            async with sem:
                reply = await run_eval._chat(client, payload)
            if reply is None:
                print(f"[fail] {pid}")
                return
            out.write(json.dumps({"id": pid, "answer": reply.strip()},
                                 ensure_ascii=False) + "\n")
        await asyncio.gather(*(one(t) for t in todo))
    out.close()
    n = sum(1 for _ in part_path.open())
    print(f"partial file now has {n} gated responses")


def splice() -> None:
    """Assemble the full 554-row v3 condition: gated fresh + ft_only reused."""
    plan_items = {p["id"]: p for p in json.loads(PLAN_PATH.read_text())}
    part = {json.loads(l)["id"]: json.loads(l)["answer"]
            for l in (HERE / "eval_results" / "responses_ft_rag_v3.partial.jsonl").open()
            if l.strip()}
    ft_only = {json.loads(l)["id"]: json.loads(l)
               for l in FT_ONLY_PATH.open() if l.strip()}
    missing = [pid for pid, p in plan_items.items()
               if p["gate_fired"] and pid not in part]
    assert not missing, f"gated responses missing: {missing[:5]}"

    rows = []
    for pid, p in plan_items.items():
        base = ft_only[pid]
        row = dict(base)
        row["gate_fired"] = p["gate_fired"]
        row["context_used"] = p["context"]
        if p["gate_fired"]:
            row["answer"] = part[pid]
        rows.append(row)
    with OUT_JSONL.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with OUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "eval_source", "category",
                                           "Context", "Response", "Answer"])
        w.writeheader()
        for r in sorted(rows, key=lambda x: x["id"]):
            w.writerow({"id": r["id"], "eval_source": r["eval_source"],
                        "category": r["category"], "Context": r["user"],
                        "Response": r["gold"], "Answer": r["answer"]})
    n_f = sum(1 for r in rows if r["gate_fired"])
    print(f"spliced {len(rows)} rows -> {OUT_JSONL.name} "
          f"({n_f} fresh gated + {len(rows)-n_f} reused from ft_only)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    g = sub.add_parser("generate")
    g.add_argument("--model", required=True)
    sub.add_parser("splice")
    a = ap.parse_args()
    if a.cmd == "plan":
        plan()
    elif a.cmd == "generate":
        asyncio.run(generate(a.model))
    else:
        splice()
