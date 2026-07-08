# Carebot Evaluation Report

## Reference-based metrics (500 synthetic held-out)

| Condition | BERTScore | BLEU | ROUGE-L | METEOR |
|---|---:|---:|---:|---:|
| baseline | 0.5346 | 0.0075 | 0.1570 | 0.2954 |
| ft_only | 0.5649 | 0.0107 | 0.1868 | 0.2708 |
| ft_rag | 0.5607 | 0.0093 | 0.1799 | 0.2487 |
| ft_rag_v2 | 0.5627 | 0.0114 | 0.1859 | 0.2515 |
| rag_only | 0.5416 | 0.0053 | 0.1548 | 0.2786 |
| rag_only_v2 | 0.5440 | 0.0067 | 0.1582 | 0.2842 |

## LLM-judge rubric (54 real Dang inputs, 1-5)

| Condition | empathy | practicality | safety | direction | human_tone | overall |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 3.98 | 3.26 | 4.41 | 4.85 | 3.35 | 3.81 |
| ft_only | 3.67 | 3.19 | 4.13 | 4.54 | 3.59 | 3.56 |
| ft_rag | 3.19 | 2.76 | 3.87 | 4.24 | 3.04 | 3.13 |
| ft_rag_v2 | 3.56 | 3.07 | 4.06 | 4.39 | 3.56 | 3.48 |
| rag_only | 3.35 | 2.70 | 3.87 | 4.33 | 2.85 | 3.14 |
| rag_only_v2 | 3.67 | 2.89 | 4.04 | 4.57 | 3.17 | 3.44 |

## BLEURT-20 (500 synthetic held-out; scored on Colab)

| Condition | n | BLEURT |
|---|---:|---:|
| baseline | 500 | 0.4735 |
| rag_only | 500 | 0.4688 |
| rag_only_v2 | 500 | 0.4652 |
| ft_only | 500 | 0.4480 |
| ft_rag | 500 | 0.4460 |
| ft_rag_v2 | 500 | 0.4381 |

_Note: BLEURT ranks baseline highest and FT variants lowest — the opposite of BERTScore/ROUGE-L. Reference metrics disagree with each other and with human review (which preferred ft_only); human judgment is primary._

## Findings & verdicts (evidence hierarchy: human review > all automated metrics)

### Human review (primary evidence)
- **Round 1 (4 conditions):** ft_only is the clear winner; baseline is good but generic.
  This OVERTURNED the LLM-judge overall ranking (judge preferred baseline 3.81 > 3.56) —
  consistent with known judge bias toward verbose, polite, generic replies. The judge's
  human_tone dimension (ft_only 3.59 > baseline 3.35) was the only one agreeing with humans.
- **Round 2 (post leak-fix, v2 pack):** ft_rag_v2 is good ONLY where retrieval adds genuinely
  relevant information; it hurts when it injects unrelated/generic content. Verdict: neither
  always-on nor always-off RAG — use SELECTIVE (gated) retrieval.

### RAG context-leak bug (found & fixed)
- v1 RAG conditions attributed retrieved interview passages to the CURRENT user
  (e.g. "your POH GGZ support" the user never mentioned). Root cause: unlabeled first-person
  context. Fix (v2): blocks labeled "another caregiver's experience" / "guide: <source>" +
  explicit non-attribution instruction. All documented leak cases clean after fix; judge
  scores recovered +0.30-0.35. The same fix is still needed in the deployed carebot_app.py.

### Metric disagreement (methodological finding)
- BERTScore/ROUGE-L favor ft_only (style match with references); BLEURT-20 REVERSES this,
  favoring baseline (semantic coverage of longer gold replies); the LLM judge favored baseline
  (verbosity bias); humans chose ft_only. Conclusion for the report: automatic metrics are
  unreliable for empathetic-dialogue quality; human evaluation was decisive.

### Self-retrieval caveat (affects dang_real RAG numbers)
- The 54 dang_real eval inputs are themselves passages in the RAG store; hit #1 for every
  dang query was the user's own statement (distance 0), wasting a context slot and biasing
  RAG-on-real-inputs downward in v1/v2. Not an issue for production users (their messages
  are not in the store).

### Retrieval-gate calibration (offline, `retrieval_gate_calibration.json`)
- Excluding self-hits: best-hit cosine median 0.61 (dang) / 0.46 (synthetic) — the corpus
  only occasionally has a strong match, matching the human verdict.
- Gate sweep: cos>=0.60 fires on ~20% of queries; >=0.65 on ~14%.
- **Recommended design:** inject only chunks with cos >= 0.60 (tunable); if none qualify,
  respond without context (= ft_only behavior). Caveat: similarity approximates relevance,
  not usefulness — threshold is a tuning start, not gospel.

### Production candidate
- **`accounts/yacchatbot/models/carebot-gemma3-27b-v1` (ft_only), optionally with gated RAG.**
- Open: port leak-fix + gate to carebot_app.py; optional gated-RAG validation run (ft_rag_v3,
  ~$8); hosting decision (Fireworks scale-to-zero for pilots vs university vLLM self-host);
  Dang data provenance (2/54 verbatim in thesis — pending team answer).
