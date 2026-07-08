# Carebot — YAC Digital Companion

A fine-tuned, retrieval-augmented AI companion for **Young Adult Caregivers** (YACs, ages 18–25),
built on Gemma-3-27B. This repository contains the full data-generation, fine-tuning-preparation,
RAG, and evaluation pipeline, plus all results.

**Start here:** [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md) — the paper-ready summary of methods,
results, and findings.

## Headline results

- The **fine-tuned model (`ft_only`) is the recommended production model** — preferred by human
  reviewers over the strong but generic base model.
- **Automatic metrics disagreed with each other and with humans** (BERTScore/ROUGE-L favored the
  fine-tune; BLEURT/METEOR and an LLM judge favored the baseline; humans chose the fine-tune).
  Human evaluation was decisive.
- Naive RAG suffered a **context-leak failure mode** (retrieved first-person passages absorbed as
  the user's own history); fixed via provenance-labeled context. Post-fix, retrieval is
  cost-neutral on average → deployed design is **gated retrieval** (inject context only when
  best-hit cosine ≥ 0.60, ~20% of queries).

## Repository layout

| Folder | Contents |
|---|---|
| `src/` | Pipeline code: dataset generation (`generate_dataset.py`), humanization pass (`humanize_dataset.py`), train/eval split (`make_eval_split.py`), RAG build + smoke test (`build_rag.py`, `test_retrieval.py`), evaluation harness (`run_eval.py`, `run_eval_v3_gate.py`), BLEURT Colab notebook |
| `data/` | `yac_synthetic_finetune.jsonl` (10k master), `..._train.jsonl` (9.5k, **use this for fine-tuning**), `yac_eval.jsonl` (554 eval) |
| `rag/` | LangChain-FAISS store (1,347 vectors) + fetched HTML sources |
| `results/` | All evaluation outputs: per-condition responses, metric scores, LLM-judge verdicts, BLEURT scores, gate calibration, and `eval_report.md` (all tables + findings) |
| `training/` | Fine-tuning loss curve (`training_metrics_gemma_v1.jsonl`) and job record |
| `docs/` | Task specifications, build reports, human-review packs |
| `app_patch/` | `carebot_app_leakfix_gate.patch` — leak fix + gated retrieval for the deployed app |

## Key facts

- **Fine-tuned model:** `carebot-gemma3-27b-v1` (Gemma-3-27B-IT, LoRA rank 8, 1 epoch, lr 1e-5;
  hosted on Fireworks AI — weights not in this repo)
- **Evaluation:** 6 conditions × 554 inputs; metrics (BERTScore/BLEU/ROUGE-L/METEOR/BLEURT-20) +
  5-dim LLM judge + 2 rounds of human review
- **Embedder:** `sentence-transformers/all-mpnet-base-v2` (normalized) — must be identical at
  index and query time

## Notes for re-running

- Scripts were developed in a flat workspace; each has a config block at the top — adjust the
  path constants (e.g., dataset/store locations) to this repo layout before re-running.
- API keys are read from a `.env` file (`FIREWORKS_API_KEY=...`) — **never commit it**.
- Dependencies: `requirements.txt` (Python 3.12).

## Data note

The 54 real caregiver interview Q&A files (`yac_qa_training_db.json` / `yac_qa_finetune.jsonl`)
and the source thesis PDF are **deliberately not included**: they contain real participant data.
Add them only to a private repository, after confirming the study's consent terms permit
redistribution. The 54 interview passages do appear inside the RAG store vectors and the
evaluation inputs/outputs in `results/`, which the team should keep in mind when choosing
repo visibility.
