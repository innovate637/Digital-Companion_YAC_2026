# Carebot Evaluation Set — Report

- **Eval file:** `yac_eval.jsonl` — 554 records
  - `synthetic_heldout`: 500 (gold replies -> reference-based metrics)
  - `dang_real`: 54 (real caregiver statements, flipped; reference-free -> LLM-judge/rubric)
- **Train file:** `yac_synthetic_finetune_train.jsonl` — 9500 records (use THIS for fine-tuning, not the original 10k file)
- **Original file:** `yac_synthetic_finetune.jsonl` — untouched (10,000)
- Selection seed: 20260705 (deterministic)

## Decisions encoded here
- All 54 Dang pairs are **eval-only** (user decision 2026-07-05): `yac_qa_finetune.jsonl` must NOT be used for fine-tuning.
- Records with the partner+'as long as I can remember' realism quirk are excluded from eval (remain in train).
- Crisis/safety hand-off examples in eval: 10 (min 10).
- NOTE: the 54 dang_real inputs are also passages in the RAG store; at eval time retrieval will surface the input's own text. By design (the store exists to ground replies in real experiences), but remember it when reading grounding scores.

## Category distribution (synthetic_heldout)
- Caregiving Challenges – Balance & Time: 50
- Caregiving Challenges – Care Recipient Behavior: 50
- Caregiving Challenges – Distance Caregiving: 50
- Caregiving Challenges – Emotional Impact: 50
- Caregiving Challenges – None Reported: 50
- Current Digital Tool Use: 50
- Online Support – Barriers: 50
- Online Support – Willingness: 50
- Support Currently Used: 50
- Support Needed: 50

## Style split (synthetic_heldout): {'quick': 250, 'scaffolded': 250}

## Contamination audit (MinHash near-dup vs train, threshold 0.7)
- synthetic_heldout inputs near-duplicated in train: **0**
- dang_real inputs near-duplicated in train: **0**
