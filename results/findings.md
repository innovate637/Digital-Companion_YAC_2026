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
- Resolved: leak-fix + gate ported to carebot_app.py (patch); Dang provenance CONFIRMED real
  interview data (team, 2026-07-06); URL click-check passed. Open: hosting decision
  (Fireworks scale-to-zero for pilots vs university vLLM self-host); gated-RAG validation
  (ft_rag_v3) in progress.
