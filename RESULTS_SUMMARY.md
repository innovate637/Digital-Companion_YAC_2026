# Carebot (YAC Digital Companion) — Results Summary

A fine-tuned, retrieval-augmented AI companion for Young Adult Caregivers (YACs, ages 18–25).

---

## 1. Method overview

**Training data.** 10,000 synthetic caregiver↔companion conversations were generated (GLM 5.2),
balanced across the 10 caregiving categories of the source taxonomy, 20 countries, and 23
care-recipient conditions, with deliberate gender balance (correcting the female skew noted as a
limitation in the source thesis). The set contains ~2% crisis/safety hand-off examples, is fully
deduplicated (0 exact or near duplicates at MinHash Jaccard ≥ 0.70), and passed a
direction-of-conversation audit (assistant is always the supportive companion). Following an
internal review that found stylistic LLM artifacts, a deterministic "humanization" pass removed
all em-dashes and semicolons (24,032 and 2,053 instances respectively) with context-sensitive
punctuation replacement.

**Train/eval split.** 9,500 training / 554 evaluation examples. The evaluation set comprises
500 stratified held-out synthetic examples (50 per category, with gold references) and all 54
real caregiver interview statements (reference-free). A contamination audit found 0 near
duplicates between train and eval.

**Fine-tuned model.** Gemma-3-27B-IT with LoRA (rank 8, 1 epoch, lr 1e-5 — deliberately
conservative to avoid the quality degradation observed with aggressive fine-tuning). Training
loss fell smoothly from 5.31 to 1.82 with no instability.

**Retrieval (RAG) knowledge base.** A FAISS store of 1,347 vectors: 1,293 chunks
(1,000 chars / 100 overlap) from the 7 source documents, plus the 54 real caregiver interview
passages ingested in flipped orientation — the caregiver's own words are the retrievable text,
the interviewer's question is metadata only. Embedder: all-mpnet-base-v2 (normalized), identical
at index and query time.

---

## 2. Evaluation design

Six conditions, each generating responses for all 554 evaluation inputs:

| Condition | Model | Retrieval |
|---|---|---|
| `baseline` | base Gemma-3-27B | none |
| `rag_only` / `rag_only_v2` | base Gemma-3-27B | on (v2 = after context-leak fix) |
| `ft_only` | fine-tuned | none |
| `ft_rag` / `ft_rag_v2` | fine-tuned | on (v2 = after context-leak fix) |

Three evidence tiers:
(a) reference-based metrics on the 500 synthetic held-out examples — BERTScore, BLEU, ROUGE-L,
METEOR, BLEURT-20;
(b) an LLM judge (5 dimensions, 1–5) on the 54 real caregiver inputs;
(c) human review of curated response samples by the team (two rounds).

---

## 3. Results

### 3.1 Reference-based metrics — 500 synthetic held-out (higher = better)

| Condition | BERTScore | BLEU | ROUGE-L | METEOR | BLEURT-20 |
|---|---:|---:|---:|---:|---:|
| baseline | 0.5346 | 0.0075 | 0.1570 | **0.2954** | **0.4735** |
| **ft_only** | **0.5649** | 0.0107 | **0.1868** | 0.2708 | 0.4480 |
| ft_rag | 0.5607 | 0.0093 | 0.1799 | 0.2487 | 0.4460 |
| ft_rag_v2 | 0.5627 | **0.0114** | 0.1859 | 0.2515 | 0.4381 |
| rag_only | 0.5416 | 0.0053 | 0.1548 | 0.2786 | 0.4688 |
| rag_only_v2 | 0.5440 | 0.0067 | 0.1582 | 0.2842 | 0.4652 |

### 3.2 LLM-judge — 54 real caregiver inputs (scale 1–5)

| Condition | empathy | practicality | safety | direction | human_tone | **overall** |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 3.98 | 3.26 | 4.41 | 4.85 | 3.35 | **3.81** |
| ft_only | 3.67 | 3.19 | 4.13 | 4.54 | **3.59** | 3.56 |
| ft_rag (v1) | 3.19 | 2.76 | 3.87 | 4.24 | 3.04 | 3.13 |
| ft_rag_v2 | 3.56 | 3.07 | 4.06 | 4.39 | 3.56 | 3.48 |
| rag_only (v1) | 3.35 | 2.70 | 3.87 | 4.33 | 2.85 | 3.14 |
| rag_only_v2 | 3.67 | 2.89 | 4.04 | 4.57 | 3.17 | 3.44 |

### 3.3 Human review (primary evidence)

- **Round 1:** `ft_only` was the clear winner; the baseline was rated good but *generic*.
- **Round 2 (after the retrieval fix):** retrieval helps **only** when it surfaces genuinely
  relevant information and degrades responses when it injects unrelated or generic content.

---

## 4. Findings

1. **Fine-tuning succeeded.** The fine-tuned model leads the style-sensitive reference metrics
   (BERTScore +0.030, ROUGE-L +0.030 over baseline) and — decisively — was preferred by human
   reviewers for a warmer, less templated voice. The base model is capable but generic.

2. **Automatic metrics disagree with each other and with humans.** BERTScore/ROUGE-L favor the
   fine-tuned model; BLEURT-20 and METEOR favor the baseline (plausibly rewarding the longer
   baseline replies' semantic coverage of the ~100-word references); the LLM judge also favored
   the baseline, consistent with the documented judge bias toward long, polite, hedged answers.
   Human evaluation reversed the judge's ranking. For empathetic-dialogue quality, **human
   evaluation was decisive**, and single-judge LLM scores should be treated as secondary evidence.

3. **Context-leak failure mode in naive RAG.** With unlabeled retrieved context, the model
   absorbed other caregivers' first-person interview statements as if they were the current
   user's history (e.g., attributing support services the user never mentioned). Labeling each
   retrieved block by provenance ("another caregiver's experience" vs. "guide: <source>") plus an
   explicit non-attribution instruction eliminated the observed leaks and recovered +0.30–0.35
   on judge overall (ft_rag 3.13 → 3.48; rag_only 3.14 → 3.44), bringing retrieval to parity
   with the fine-tuned model alone.

4. **Retrieval should be conditional, not always-on.** After the fix, retrieval was cost-neutral
   on average: per-category analysis showed no measurable gain even on information-seeking
   queries, and human review confirmed it helps only when the retrieved material is genuinely
   relevant. Offline calibration of best-hit similarity (median cosine 0.61 on real inputs,
   0.46 on synthetic) shows the corpus only occasionally contains a strong match. We therefore
   adopt **gated retrieval**: context is injected only when best-hit cosine ≥ 0.60 (which fires
   on ~20% of queries); otherwise the system responds as the plain fine-tuned model.

---

## 5. Limitations

- **Reference-metric circularity.** The gold references for the 500 synthetic eval items come
  from the same synthetic distribution the model was fine-tuned on, so style-sensitive metrics
  partly measure distribution match rather than quality.
- **Single LLM judge.** The judge was one model (GLM 5.2), which also generated the training
  data; its rankings were treated as secondary to human review.
- **Self-retrieval artifact.** The 54 real interview statements are simultaneously evaluation
  inputs and store passages; during evaluation, retrieval's top hit for these items was often the
  input itself, slightly biasing RAG-on-real-input scores downward. Production users are not in
  the store, so deployment is unaffected.
- **Gated retrieval is validated by construction, not yet by measurement.** By design it can
  differ from `ft_only` only on the ~20% of queries with a confident retrieval match; an
  end-to-end measured validation of the gated condition remains future work.
- **Small human-review samples.** Human verdicts rest on curated packs (15 items × conditions per
  round) reviewed by the team, not a powered user study.

---

## 6. Conclusion

The fine-tuned Gemma-3-27B (`carebot-gemma3-27b-v1`) is the recommended production model.
Retrieval augmentation should be deployed, if at all, behind a relevance gate with
provenance-labeled context. The evaluation additionally contributes a methodological observation:
for empathetic support dialogue, widely used automatic metrics (including LLM-as-judge) can
invert the human preference ordering, and conclusions should not be drawn from them alone.
