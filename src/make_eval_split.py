#!/usr/bin/env python3
"""
make_eval_split.py
==================
Builds the Carebot evaluation set and the corresponding decontaminated train split.

Inputs:
  - yac_synthetic_finetune.jsonl   (10,000 synthetic examples; left untouched)
  - yac_qa_training_db.json        (54 real Dang-thesis interview Q&A pairs)

Outputs:
  - yac_eval.jsonl                 554 records:
        * 500 synthetic held-out (50 per category, gold replies -> reference-based eval)
        * 54  real Dang pairs, flipped (caregiver statement as user input, no gold
          reply -> reference-free / LLM-judge eval). Eval-only by user decision
          (2026-07-05): yac_qa_finetune.jsonl is NOT to be used for fine-tuning.
  - yac_synthetic_finetune_train.jsonl   9,500 records (10k minus the eval carve-out)
  - eval_set_report.md             split stats + contamination audit

Selection rules:
  - stratified 50/category, ~50/50 quick/scaffolded within each stratum
  - records with the known partner+"as long as I can remember" realism quirk are
    ineligible for eval (they remain in train)
  - at least MIN_CRISIS crisis/safety-hand-off examples are included in eval
  - deterministic (SEED)

Run:  python make_eval_split.py
"""

from __future__ import annotations

import json
import random
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---- config -------------------------------------------------------------------------
SOURCE_PATH = HERE / "yac_synthetic_finetune.jsonl"
DANG_DB_PATH = HERE / "yac_qa_training_db.json"
EVAL_PATH = HERE / "yac_eval.jsonl"
TRAIN_PATH = HERE / "yac_synthetic_finetune_train.jsonl"
REPORT_PATH = HERE / "eval_set_report.md"
PER_CATEGORY = 50
MIN_CRISIS = 10
SEED = 20260705
NEAR_DUP_THRESHOLD = 0.70     # same as generation-time dedupe

CRISIS_RE = re.compile(
    r"crisis line|better off without|self-harm|suicid|this comes first|"
    r"talk to a trained person", re.IGNORECASE)
QUIRK = ("partner", "as long as")   # relation contains / duration contains


def is_quirk(rec: dict) -> bool:
    p = rec["metadata"].get("profile", {})
    return (QUIRK[0] in p.get("relation_to_cr", "")
            and QUIRK[1] in p.get("care_duration", ""))


def is_crisis(rec: dict) -> bool:
    return bool(CRISIS_RE.search(rec["messages"][2]["content"]))


def main() -> None:
    rng = random.Random(SEED)
    recs = [json.loads(l) for l in SOURCE_PATH.open() if l.strip()]
    assert len(recs) == 10_000, f"expected 10000 records, got {len(recs)}"

    # ---- stratified selection --------------------------------------------------------
    by_cat: dict[str, list[dict]] = {}
    for r in recs:
        by_cat.setdefault(r["metadata"]["category"], []).append(r)

    eval_ids: set[str] = set()
    for cat, pool in sorted(by_cat.items()):
        eligible = [r for r in pool if not is_quirk(r)]
        quick = [r for r in eligible if r["metadata"]["response_style"] == "quick"]
        scaff = [r for r in eligible if r["metadata"]["response_style"] == "scaffolded"]
        rng.shuffle(quick)
        rng.shuffle(scaff)
        take = quick[:PER_CATEGORY // 2] + scaff[:PER_CATEGORY // 2]
        # top up from either style if one ran short
        if len(take) < PER_CATEGORY:
            rest = [r for r in eligible if r not in take]
            rng.shuffle(rest)
            take += rest[:PER_CATEGORY - len(take)]
        eval_ids.update(r["metadata"]["id"] for r in take)

    # ---- ensure crisis coverage ------------------------------------------------------
    eval_recs = [r for r in recs if r["metadata"]["id"] in eval_ids]
    n_crisis = sum(map(is_crisis, eval_recs))
    if n_crisis < MIN_CRISIS:
        needed = MIN_CRISIS - n_crisis
        candidates = [r for r in recs
                      if is_crisis(r) and not is_quirk(r)
                      and r["metadata"]["id"] not in eval_ids]
        rng.shuffle(candidates)
        for add in candidates[:needed]:
            cat = add["metadata"]["category"]
            style = add["metadata"]["response_style"]
            # swap out a same-category same-style non-crisis record to keep strata sizes
            swap_pool = [r for r in eval_recs
                         if r["metadata"]["category"] == cat
                         and r["metadata"]["response_style"] == style
                         and not is_crisis(r)]
            if not swap_pool:
                continue
            out = rng.choice(swap_pool)
            eval_ids.discard(out["metadata"]["id"])
            eval_ids.add(add["metadata"]["id"])
            eval_recs = [r for r in recs if r["metadata"]["id"] in eval_ids]
        n_crisis = sum(map(is_crisis, eval_recs))

    train_recs = [r for r in recs if r["metadata"]["id"] not in eval_ids]
    assert len(eval_recs) + len(train_recs) == 10_000

    # ---- Dang real subset (flipped, reference-free) ----------------------------------
    dang = json.loads(DANG_DB_PATH.read_text())["qa_pairs"]
    system_prompt = recs[0]["messages"][0]["content"]   # deployed Carebot prompt
    dang_eval = []
    for rec in dang:
        dang_eval.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": rec["answer"].strip()},
                # no assistant turn: reference-free subset (LLM-judge / rubric eval)
            ],
            "metadata": {
                "id": f"dang_{rec['id']}",
                "eval_source": "dang_real",
                "reference": "none (reference-free: judge/rubric eval)",
                "category": rec["category"],
                "source_participant": rec["source_participant"],
                "eliciting_question": rec["question"],
                "themes": rec.get("themes", []),
            },
        })

    # ---- write outputs ---------------------------------------------------------------
    with EVAL_PATH.open("w") as fh:
        for r in eval_recs:
            r = json.loads(json.dumps(r))       # copy; don't mutate train view
            r["metadata"]["eval_source"] = "synthetic_heldout"
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in dang_eval:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with TRAIN_PATH.open("w") as fh:
        for r in train_recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---- contamination audit (MinHash near-dup, eval vs train) ------------------------
    import generate_dataset as g
    lsh = g.MinHashLSH(g.MINHASH_PERM, g.LSH_BANDS, NEAR_DUP_THRESHOLD,
                       g.SHINGLE_K, g.RANDOM_SEED)
    for r in train_recs:
        lsh.add(lsh.signature(r["messages"][1]["content"]))
    def contaminated(texts):
        return sum(lsh.is_duplicate(lsh.signature(t)) for t in texts)
    syn_contam = contaminated(r["messages"][1]["content"] for r in eval_recs)
    dang_contam = contaminated(r["messages"][1]["content"] for r in dang_eval)

    # ---- report -----------------------------------------------------------------------
    cats = Counter(r["metadata"]["category"] for r in eval_recs)
    styles = Counter(r["metadata"]["response_style"] for r in eval_recs)
    lines = [
        "# Carebot Evaluation Set — Report",
        "",
        f"- **Eval file:** `{EVAL_PATH.name}` — {len(eval_recs) + len(dang_eval)} records",
        f"  - `synthetic_heldout`: {len(eval_recs)} (gold replies -> reference-based metrics)",
        f"  - `dang_real`: {len(dang_eval)} (real caregiver statements, flipped; "
        f"reference-free -> LLM-judge/rubric)",
        f"- **Train file:** `{TRAIN_PATH.name}` — {len(train_recs)} records "
        f"(use THIS for fine-tuning, not the original 10k file)",
        f"- **Original file:** `{SOURCE_PATH.name}` — untouched (10,000)",
        f"- Selection seed: {SEED} (deterministic)",
        "",
        "## Decisions encoded here",
        "- All 54 Dang pairs are **eval-only** (user decision 2026-07-05): "
        "`yac_qa_finetune.jsonl` must NOT be used for fine-tuning.",
        "- Records with the partner+'as long as I can remember' realism quirk are "
        "excluded from eval (remain in train).",
        f"- Crisis/safety hand-off examples in eval: {n_crisis} (min {MIN_CRISIS}).",
        "- NOTE: the 54 dang_real inputs are also passages in the RAG store; at eval "
        "time retrieval will surface the input's own text. By design (the store exists "
        "to ground replies in real experiences), but remember it when reading grounding "
        "scores.",
        "",
        "## Category distribution (synthetic_heldout)",
        *(f"- {c}: {n}" for c, n in sorted(cats.items())),
        "",
        f"## Style split (synthetic_heldout): {dict(styles)}",
        "",
        "## Contamination audit (MinHash near-dup vs train, "
        f"threshold {NEAR_DUP_THRESHOLD})",
        f"- synthetic_heldout inputs near-duplicated in train: **{syn_contam}**",
        f"- dang_real inputs near-duplicated in train: **{dang_contam}**",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n")
    print(f"eval:  {len(eval_recs)+len(dang_eval)} -> {EVAL_PATH.name} "
          f"({len(eval_recs)} synthetic + {len(dang_eval)} dang_real, crisis={n_crisis})")
    print(f"train: {len(train_recs)} -> {TRAIN_PATH.name}")
    print(f"contamination: synthetic={syn_contam}, dang={dang_contam}")
    print(f"report: {REPORT_PATH.name}")


if __name__ == "__main__":
    main()
