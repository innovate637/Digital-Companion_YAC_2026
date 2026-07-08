# Carebot RAG Knowledge Base — Build Report

**Build date:** 2026-07-05 · **Store:** `rag_store/` (LangChain FAISS) · **Build time:** ~3 min (CPU) · **Cost:** $0 (fully local, no API)

## Store contents

| Source | Type | Vectors |
|---|---|---:|
| Find a fulfilling career that does good (80,000 Hours) | web_doc (PDF, pages 12–440 as in original `embed.py`) | 1,019 |
| Professionalism of career guidance (Euroguidance) | web_doc (PDF) | 118 |
| Framework for career guidance for young people (Euroguidance) | web_doc (PDF) | 84 |
| Young carers: Shaping our future (The Children's Society) | web_doc (PDF) | 39 |
| Balancing caregiving and career… (Bright Horizons) | web_doc (PDF) | 20 |
| Help for young carers (NHS) | web_doc (fetched HTML) | 9 |
| Do you know your rights in youth care? (Jeugdstem) | web_doc (fetched HTML) | 4 |
| **Dang YAC interview passages (flipped)** | yac_interview | **54** |
| **Total** | | **1,347** |

- Embedder: `sentence-transformers/all-mpnet-base-v2`, local, normalized embeddings (cosine-like). Same model the app (`carebot_app.py`) uses at query time — consistency rule satisfied.
- Chunking: 1000 chars / 100 overlap (`RecursiveCharacterTextSplitter`) — matches report §3.3 and repo `embed.py`. YAC passages NOT chunked (ingested whole, per spec).
- Round-trip verified: `FAISS.load_local(...)` + `max_marginal_relevance_search(k=3)` works — the exact load path the app uses.

## Flipped YAC ingestion (§3 of the instructions)
- Source of truth: `yac_qa_training_db.json` only (54 records). The JSONL was **excluded** from the store (same 54 pairs — verified 54/54 fuzzy-match; ingesting both would double-insert).
- `page_content` = caregiver's answer (their authentic words, retrievable).
- Psychologist's question + category + participant ID = metadata only (`eliciting_question` is never embedded).
- 5 answers under 15 words received a `[Category]` prefix tag.
- Participants remain anonymized (P1–P13), untouched.

## Assumptions register — outcomes
- **A1 (same pairs)** ✅ verified: 54 = 54, all answers fuzzy-matched (>0.85 ratio).
- **A2 (app load path)** ✅ verified in `carebot_app.py`: `HuggingFaceEmbeddings(all-mpnet-base-v2)` + `FAISS.load_local(..., allow_dangerous_deserialization=True)` + `max_marginal_relevance_search(query, k=3)`.
- **A3 (1000/100 chunking)** ✅ confirmed in repo `embed.py`, replicated (incl. the career_1 page slice 12:440).
- **A4 (repo docs)** — 5 of 7 present as PDFs; NHS + Jeugdstem fetched fresh. The repo's prebuilt store (`app/vector_stores/UvA_AUG_YAG_chatbot/`) contained ONLY the 5 career PDFs (no NHS/Jeugdstem/YAC passages) → rebuilt, per spec.
- **A5/A6/A7** — mpnet kept; fetch_k=12 recorded in manifest; flat CPU index (1,347 vectors is tiny).

## Fetch notes / anything unobtainable
- **Nothing unobtainable.** All 7 Table-2 sources are in the store.
- **Jeugdstem URL had moved** (old path 404s). Located current page via site nav: `https://jeugdstem.nl/ken-je-rechten`. **The page is in Dutch.** all-mpnet-base-v2 is English-centric, so these 4 chunks will embed/retrieve poorly for English queries. Options if this matters: translate to English before ingesting, or accept them as Dutch-audience content. Flagged rather than silently translated.
- NHS page fetched from its canonical URL (9 chunks).

## Smoke test (`test_retrieval.py`, MMR k=3 / fetch_k=12)
Full output: `smoke_test_output.txt`. Summary: **6/8 queries pass all three automated checks; 8/8 pass (a) k=3-results and (b) no-interviewer-question.**

The 2 (c)-topic failures on manual review:
- **Q6** ("understand my sister's condition better") — retrieved passages ARE relevant (professional-info access + two sister/care-recipient experiences); the automated topic list was too narrow. False negative, no action needed.
- **Q7** ("cancelling on friends") — 2 of 3 results relevant; 1 result is an off-topic 80,000 Hours negotiation chunk. Real but mild quality finding, see below.

## Known limitation: corpus imbalance
The 80,000 Hours book contributes **76% of all vectors** (1,019/1,347). Under MMR's diversity re-ranking, an off-topic book chunk occasionally enters the top-3 (seen in Q7). If this bothers retrieval quality in practice, options (not applied — they'd deviate from the report's documented pipeline):
1. Retrieve with `filter` or higher `k` + post-filter by source diversity in the app.
2. Cap per-source chunks or drop the book's front/back matter more aggressively.
3. Raise `fetch_k` so MMR has a richer candidate pool.

## Deliverables
- `build_rag.py` — build script (config block at top).
- `test_retrieval.py` — smoke test (exit code 1 while any automated check fails).
- `rag_store/` — `index.faiss` + `index.pkl` + `store_manifest.json`.
- `requirements.txt` — pinned versions (shared with the SFT-generation deps).
- `smoke_test_output.txt` — full retrieval output for the 8 queries, for human review.

## Next step (per instructions — NOT started)
Wire this retriever into the model-inference/eval matrix (separate task). The store loads with the app's existing code unchanged if pointed at `rag_store/`.
