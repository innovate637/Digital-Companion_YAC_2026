# INSTRUCTIONS: Build the RAG Knowledge Base for Carebot (v2)

## Goal
Build a FAISS vector store that Carebot retrieves from at inference time. Two source types go in:
1. The **7 web documents** on young-carer + career guidance (from the report's Table 2).
2. The **Dang YAC interview Q&A** (54 real caregiver Q&A pairs) — ingested in **FLIPPED** orientation (see §3, critical).

Output: a persisted FAISS index + metadata, plus a retrieval smoke-test script. Do NOT start any fine-tuning or app-integration work in this task.

---

## Embedding model (LOCAL — no API, no credits)
Use **`sentence-transformers/all-mpnet-base-v2`** run **locally** via the `sentence-transformers` library (CPU is fine at this scale; ~420MB download, Apache-2.0, free).

Why local mpnet and NOT an API embedder:
- It is the **same embedder the project's existing pipeline used** (`embed.py` in the repo), so the new store stays methodologically comparable to prior work and is a drop-in replacement for the app's existing load path.
- It costs nothing and adds no API dependency to the offline build.
- The corpus is tiny (a few hundred chunks); a SOTA embedder buys nothing measurable here.

**Consistency rule (critical):** whatever embeds the store must also embed the queries. The deployed app must load the SAME model name for query-time embedding. Record the model name in the store manifest. Expose the embedder as a config constant (`EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"`) so a future switch (e.g., to a Fireworks-hosted embedder) is a one-line change followed by a full re-embed — never mix embedders within one index.

---

## Compatibility requirement (build it the way the app loads it)
The existing app (`carebot_app.py`) loads its store with LangChain's FAISS wrapper (`FAISS.load_local(...)` with `HuggingFaceEmbeddings`). Therefore:
- Build the index via **LangChain**: `HuggingFaceEmbeddings(model_name=EMBED_MODEL)` + `FAISS.from_documents(docs, embeddings)` + `save_local(...)`.
- Do NOT hand-roll a raw `faiss` index with a custom pickle format — it would not be loadable by the app without extra glue code.
- Verify after saving: `FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)` round-trips and returns results with `.max_marginal_relevance_search(query, k=3)`.

---

## Step 1 — Locate or fetch the 7 web documents
First **check the repo** (clone/pull `github.com/the4daspect/Digital-Companion---AUF-2025`; look in `app/` and any `rag/`, `data/`, `docs/`, or FAISS-related subfolders) for the already-collected source documents and/or an existing FAISS store.

- If the source PDFs/text are present → use them (preferred: identical inputs to prior work).
- If only a prebuilt FAISS store is present → you may reuse it ONLY if its manifest/embedder is confirmed to be all-mpnet-base-v2 AND its contents match Table 2; otherwise keep the source docs and rebuild. When in doubt, rebuild — it costs minutes.
- If a document is missing → download it from its source. Table 2 sources:
  1. "Find a fulfilling career that does good" — 80,000 Hours
  2. "Framework for career guidance for young people" — Euroguidance
  3. "Professionalism of career guidance" — Euroguidance
  4. "Young carers: Shaping our future" — The Children's Society
  5. "Balancing caregiving and career: tips for starting your new job strong" — Bright Horizons
  6. "Help for young carers" — NHS
  7. "Do you know your rights in youth care?" — Jeugdstem
- If a URL has moved/died, search for the document title and fetch the current official page. Report anything you could not obtain; do not silently drop a source. If a page is HTML, save the main-content text (strip nav/boilerplate with e.g. `trafilatura` or `beautifulsoup4`).

---

## Step 2 — Chunk the web documents (web docs ONLY)
Match the report's pipeline:
- PDFs → text via LangChain `PyPDFLoader`; HTML → cleaned main text.
- Light cleanup before chunking: fix hyphenated line-breaks, collapse repeated whitespace, drop headers/footers/page numbers where detectable.
- Split into chunks of **1000 characters with 100-character overlap** (`RecursiveCharacterTextSplitter`).
- Metadata per chunk: `{"source": "<doc title>", "type": "web_doc", "url": "<source url>"}`.

**Do NOT run the YAC interview passages (Step 3) through this chunker.** They are short, self-contained statements (7–141 words); chunking them is unnecessary and overlap would duplicate content. Ingest each as a single Document.

---

## Step 3 — Ingest the Dang YAC Q&A (FLIPPED — critical) — ONE source file only
**Use `yac_qa_training_db.json` as the single source of truth.** The two provided files (`yac_qa_training_db.json` and `yac_qa_finetune.jsonl`) contain the SAME 54 Q&A pairs in different formats — ingesting both would insert every passage twice and skew retrieval. Ingest the DB file only; keep the JSONL out of the store entirely.

The records are interview Q&A where the **answer is the caregiver's own words** and the **question is a psychologist's interview question**. For RAG we want the **caregiver's authentic lived-experience statement** to be the retrievable passage — NOT the interviewer's question.

For each of the 54 records:
- The **caregiver's answer text** is the Document `page_content` (embedded + retrievable).
- The psychologist's question and category go ONLY in metadata: `{"type": "yac_interview", "category": "<cat>", "source_participant": "<id>", "eliciting_question": "<question>"}` — never embed the question as searchable text.
- If a caregiver answer is very short (< ~15 words), prepend the category as a light context tag (e.g., `[Emotional Impact] <answer>`) so it retrieves sensibly, keeping the caregiver's words as the core.
- Participants are already anonymized (P1–P13); keep IDs as-is, do not attempt any de-anonymization or enrichment.

Rationale: at query time a real user describes their situation; the retriever should surface authentic caregiver experiences on the same theme — grounded, real-voice context for Carebot — never an interviewer's probing question.

(The JSONL fine-tune file remains reserved for the separate fine-tuning workstream; it plays no role in this build.)

---

## Step 4 — Embed + build + persist (LangChain FAISS)
- Create `HuggingFaceEmbeddings(model_name=EMBED_MODEL)` (normalize embeddings ON — pass `encode_kwargs={"normalize_embeddings": True}` — so similarity behaves as cosine).
- `FAISS.from_documents(all_docs, embeddings)` over web-doc chunks + YAC passages.
- `save_local("rag_store/")`.
- Also write `rag_store/store_manifest.json`: embedding model name, normalize flag, chunk settings, per-source counts (web_doc chunks, yac_interview passages), library versions (langchain, sentence-transformers, faiss), and build date.

---

## Step 5 — Retrieval smoke test (must pass before finishing)
Write `test_retrieval.py` that:
- Loads the store via `FAISS.load_local(...)` with the same embedder, runs **MMR search, k=3** (`fetch_k=12` for a sane candidate pool — matching the report's MMR top-3 design), prints retrieved passages + metadata.
- Run on ~8 sample caregiver queries spanning categories:
  - "I can't balance caring for my mum with my university work."
  - "I feel so alone even though I'm always busy caring for my brother."
  - "I look after my grandmother over the phone and I'm always anxious."
  - "I don't know what support exists for someone my age."
  - "My dad gets angry when I try to help him with his medication."
  - "I want to understand my sister's condition better."
  - "I keep cancelling on friends and they've stopped inviting me."
  - "Are there online communities for young carers that actually help?"
- Automated checks per query, printed as PASS/FAIL: (a) 3 results returned; (b) NO result's page_content is an interviewer-style question (heuristic: starts with "Can you/How do/What/Do you" AND ends with "?"); (c) at least one result's metadata type is plausible for the query topic.
- Additionally print the full results for MANUAL review — a human must confirm relevance before this phase is called done.

---

## Deliverables
1. `build_rag.py` — locate/fetch → clean/chunk (web docs) → flip-ingest (YAC DB) → embed (local mpnet) → LangChain FAISS → persist. Config block at top (EMBED_MODEL, chunk size/overlap, paths, k/fetch_k).
2. `test_retrieval.py` — smoke test above.
3. `rag_store/` — LangChain-format index + `store_manifest.json`.
4. `requirements.txt` — pinned: `sentence-transformers`, `torch` (CPU build is fine), `langchain`, `langchain-community`, `langchain-huggingface`, `faiss-cpu`, `pypdf`, `requests`, `tqdm`; add `beautifulsoup4`/`trafilatura` only if HTML fetching is used.
5. `rag_build_report.md` — per-source counts, total vectors, cleanup notes, anything unobtainable, and smoke-test output.

---

## ASSUMPTIONS REGISTER (verify these; flag loudly if any fail)
1. **A1 — Same-pairs assumption:** `yac_qa_training_db.json` and `yac_qa_finetune.jsonl` contain the identical 54 Q&A pairs. VERIFY at runtime (compare counts + fuzzy-match answers); if they differ, report the difference and ingest the union (still flipped, still deduplicated).
2. **A2 — App load-path assumption:** `carebot_app.py` loads the store via LangChain `FAISS.load_local` with `HuggingFaceEmbeddings(all-mpnet-base-v2)`. VERIFY by reading the actual app code in the repo before building; if it differs, match whatever the app actually does and note it in the report.
3. **A3 — Chunk-setting assumption:** 1000/100 chunking matches the report (§3.3). This is documented in the final report; treat as fixed unless repo code contradicts it.
4. **A4 — Repo availability assumption:** the 7 source docs may or may not be in the repo. The build handles both paths; nothing assumes they exist.
5. **A5 — Embedder choice is a DECISION, not a constraint:** mpnet was chosen for comparability + zero cost. Fireworks-hosted embedding (e.g., Qwen3-embedding) is a valid alternative if the team later wants query-time embedding on Fireworks; switching requires a full re-embed of the store and the app's query path together.
6. **A6 — MMR parameters:** the report fixes k=3 MMR but not fetch_k; fetch_k=12 is a reasonable default, not a documented project value. Keep it in config.
7. **A7 — Scale assumption:** corpus stays small (hundreds of chunks), so CPU + flat FAISS index is sufficient; no ANN tuning needed. Revisit only if the corpus grows by orders of magnitude.

## Notes
- No API keys are needed for this build (fully local). The H100 is not needed either.
- After completion, print the store path and remind me the next step is wiring this retriever into the model-inference/eval matrix (handled separately).
