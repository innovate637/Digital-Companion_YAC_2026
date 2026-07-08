#!/usr/bin/env python3
"""
build_rag.py
============
Builds the Carebot RAG knowledge base as a LangChain-FAISS store.

Ingests:
  1. The 7 web documents from the report's Table 2
     - 5 PDFs already collected in the repo (repo_digital_companion/app/rag_docs/)
     - 2 HTML pages fetched to rag_sources/ (NHS young-carers page, Jeugdstem rights page)
  2. The 54 Dang YAC interview Q&A pairs from yac_qa_training_db.json, ingested
     FLIPPED: the caregiver's answer is the retrievable page_content; the
     psychologist's eliciting question lives only in metadata.

Build path matches the deployed app (carebot_app.py):
  HuggingFaceEmbeddings(all-mpnet-base-v2) -> FAISS.from_documents -> save_local.

Fully local: no API keys, no GPU. Run:  python build_rag.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Keep the HF model cache inside this project (shared-server etiquette).
os.environ.setdefault("HF_HOME", str(HERE / ".hf_cache"))

from bs4 import BeautifulSoup                              # noqa: E402
from langchain_community.document_loaders import PyPDFLoader  # noqa: E402
from langchain_community.vectorstores import FAISS         # noqa: E402
from langchain_core.documents import Document              # noqa: E402
from langchain_huggingface import HuggingFaceEmbeddings    # noqa: E402
from langchain_text_splitters import RecursiveCharacterTextSplitter  # noqa: E402

# ======================================================================================
# CONFIG
# ======================================================================================
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"   # must match query-time embedder
NORMALIZE_EMBEDDINGS = True                               # cosine-like similarity
CHUNK_SIZE = 1000                                         # matches report §3.3 / embed.py
CHUNK_OVERLAP = 100
STORE_PATH = HERE / "rag_store"
MANIFEST_PATH = STORE_PATH / "store_manifest.json"
YAC_DB_PATH = HERE / "yac_qa_training_db.json"
PDF_DIR = HERE / "repo_digital_companion" / "app" / "rag_docs"
HTML_DIR = HERE / "rag_sources"
SHORT_ANSWER_WORDS = 15          # answers below this get a [Category] context tag
K = 3                            # app's MMR top-k (recorded in manifest; used by tests)
FETCH_K = 12                     # MMR candidate pool (A6: reasonable default, not doc'd)

# The 7 Table-2 sources. PDFs use the repo files; HTML uses the fetched pages.
WEB_SOURCES = [
    {"file": PDF_DIR / "career_1.pdf", "kind": "pdf",
     "title": "Find a fulfilling career that does good (80,000 Hours)",
     "url": "https://80000hours.org/career-guide/",
     # embed.py sliced this 492-page book to pages [12:440] to skip front/back matter.
     "page_slice": (12, 440)},
    {"file": PDF_DIR / "career_2.pdf", "kind": "pdf",
     "title": "Framework for career guidance for young people (Euroguidance)",
     "url": "https://www.euroguidance.nl/", "page_slice": None},
    {"file": PDF_DIR / "career_3.pdf", "kind": "pdf",
     "title": "Professionalism of career guidance (Euroguidance)",
     "url": "https://www.euroguidance.nl/professionalism-of-career-guidance-in-VET",
     "page_slice": None},
    {"file": PDF_DIR / "career_4.pdf", "kind": "pdf",
     "title": "Young carers: Shaping our future (The Children's Society)",
     "url": "https://www.childrenssociety.org.uk/", "page_slice": None},
    {"file": PDF_DIR / "career_5.pdf", "kind": "pdf",
     "title": "Balancing caregiving and career: tips for starting your new job strong "
              "(Bright Horizons)",
     "url": "https://www.brighthorizons.com/", "page_slice": None},
    {"file": HTML_DIR / "nhs_help_for_young_carers.html", "kind": "html",
     "title": "Help for young carers (NHS)",
     "url_file": HTML_DIR / "nhs_help_for_young_carers.url"},
    {"file": HTML_DIR / "jeugdstem_rights_youth_care.html", "kind": "html",
     "title": "Do you know your rights in youth care? (Jeugdstem)",
     "url_file": HTML_DIR / "jeugdstem_rights_youth_care.url"},
]


# ======================================================================================
# Text cleanup helpers
# ======================================================================================
def clean_text(text: str) -> str:
    """Light cleanup: de-hyphenate line breaks, collapse whitespace, drop page numbers."""
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          # hyphenated line-breaks
    text = re.sub(r"^\s*\d{1,4}\s*$", "", text, flags=re.MULTILINE)  # lone page numbers
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def html_main_text(html: str) -> str:
    """Extract main-content text from an HTML page, stripping nav/boilerplate."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form",
                     "noscript", "button", "svg"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    text = main.get_text(separator="\n")
    # drop very short leftover menu-ish lines
    lines = [ln.strip() for ln in text.splitlines()]
    kept = [ln for ln in lines if len(ln.split()) >= 3 or ln.endswith((".", "?", "!", ":"))]
    return clean_text("\n".join(kept))


# ======================================================================================
# Step 2 — load + chunk the 7 web documents
# ======================================================================================
def load_web_docs() -> tuple[list[Document], dict[str, int]]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, add_start_index=True)
    all_chunks: list[Document] = []
    counts: dict[str, int] = {}
    for src in WEB_SOURCES:
        path = src["file"]
        if not path.exists():
            print(f"[MISSING] {src['title']} — expected at {path}", file=sys.stderr)
            counts[src["title"]] = 0
            continue
        if src["kind"] == "pdf":
            pages = PyPDFLoader(str(path)).load()
            if src.get("page_slice"):
                a, b = src["page_slice"]
                pages = pages[a:b]
            for p in pages:
                p.page_content = clean_text(p.page_content)
            docs = [p for p in pages if p.page_content]
            url = src["url"]
        else:
            url = (src["url_file"].read_text().strip()
                   if src.get("url_file") and src["url_file"].exists() else "")
            text = html_main_text(path.read_text())
            docs = [Document(page_content=text)]
        chunks = splitter.split_documents(docs)
        for c in chunks:
            c.metadata = {"source": src["title"], "type": "web_doc", "url": url}
        counts[src["title"]] = len(chunks)
        all_chunks.extend(chunks)
        print(f"  {src['title'][:60]:62s} -> {len(chunks)} chunks")
    return all_chunks, counts


# ======================================================================================
# Step 3 — flip-ingest the 54 YAC interview Q&A (DB file only, never the JSONL)
# ======================================================================================
def load_yac_passages() -> list[Document]:
    data = json.loads(YAC_DB_PATH.read_text())
    pairs = data["qa_pairs"]
    docs = []
    for rec in pairs:
        answer = rec["answer"].strip()
        # very short answers get a light category tag so they retrieve sensibly
        if len(answer.split()) < SHORT_ANSWER_WORDS:
            answer = f"[{rec['category']}] {answer}"
        docs.append(Document(
            page_content=answer,                       # caregiver's words = retrievable
            metadata={
                "type": "yac_interview",
                "category": rec["category"],
                "source_participant": rec["source_participant"],
                "eliciting_question": rec["question"],  # metadata ONLY, never embedded
            },
        ))
    print(f"  YAC interview passages (flipped, DB only)                      -> {len(docs)} docs")
    return docs


# ======================================================================================
# Step 4 — embed + build + persist
# ======================================================================================
def main() -> None:
    t0 = time.time()
    print("== Step 1-2: web documents ==")
    web_chunks, web_counts = load_web_docs()
    print("== Step 3: YAC interview passages ==")
    yac_docs = load_yac_passages()
    all_docs = web_chunks + yac_docs
    print(f"\nTotal documents to embed: {len(all_docs)}")

    print(f"\n== Step 4: embedding with {EMBED_MODEL} (local, CPU) ==")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        encode_kwargs={"normalize_embeddings": NORMALIZE_EMBEDDINGS},
    )
    store = FAISS.from_documents(all_docs, embeddings)
    STORE_PATH.mkdir(exist_ok=True)
    store.save_local(str(STORE_PATH))

    # manifest
    import langchain, sentence_transformers, faiss
    manifest = {
        "embedding_model": EMBED_MODEL,
        "normalize_embeddings": NORMALIZE_EMBEDDINGS,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "mmr_defaults": {"k": K, "fetch_k": FETCH_K},
        "counts": {
            "web_doc_chunks": len(web_chunks),
            "yac_interview_passages": len(yac_docs),
            "total_vectors": len(all_docs),
            "per_source": web_counts,
        },
        "versions": {
            "langchain": langchain.__version__,
            "sentence_transformers": sentence_transformers.__version__,
            "faiss": faiss.__version__,
        },
        "build_date": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    # round-trip verification (the way the app loads it)
    reloaded = FAISS.load_local(str(STORE_PATH), embeddings,
                                allow_dangerous_deserialization=True)
    res = reloaded.max_marginal_relevance_search(
        "I can't balance caring for my mum with my studies", k=K, fetch_k=FETCH_K)
    assert len(res) == K, "round-trip MMR search failed"
    print(f"\nRound-trip verified: load_local + MMR returned {len(res)} results.")
    print(f"Store persisted at {STORE_PATH}/  ({len(all_docs)} vectors, "
          f"{time.time()-t0:.0f}s)")
    print("\nNEXT STEP: wire this retriever into the model-inference/eval matrix "
          "(handled separately — not part of this build).")


if __name__ == "__main__":
    main()
