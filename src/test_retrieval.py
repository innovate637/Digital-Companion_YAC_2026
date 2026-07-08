#!/usr/bin/env python3
"""
test_retrieval.py
=================
Retrieval smoke test for the Carebot RAG store (rag_store/).

Loads the store exactly the way carebot_app.py does (LangChain FAISS.load_local +
HuggingFaceEmbeddings), runs MMR search (k=3, fetch_k=12) on 8 sample caregiver
queries, prints automated PASS/FAIL checks plus full results for manual review.

Run:  python test_retrieval.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(HERE / ".hf_cache"))

from langchain_community.vectorstores import FAISS         # noqa: E402
from langchain_huggingface import HuggingFaceEmbeddings    # noqa: E402

STORE_PATH = HERE / "rag_store"
MANIFEST = json.loads((STORE_PATH / "store_manifest.json").read_text())
EMBED_MODEL = MANIFEST["embedding_model"]
K = MANIFEST["mmr_defaults"]["k"]
FETCH_K = MANIFEST["mmr_defaults"]["fetch_k"]

# (query, plausible metadata topics) — topic check accepts either a matching YAC
# category substring or a web-doc source keyword.
QUERIES: list[tuple[str, list[str]]] = [
    ("I can't balance caring for my mum with my university work.",
     ["Balance & Time", "carer", "career"]),
    ("I feel so alone even though I'm always busy caring for my brother.",
     ["Emotional Impact", "Support", "carer"]),
    ("I look after my grandmother over the phone and I'm always anxious.",
     ["Distance", "Emotional Impact", "carer"]),
    ("I don't know what support exists for someone my age.",
     ["Support Needed", "Support Currently Used", "young carers", "NHS"]),
    ("My dad gets angry when I try to help him with his medication.",
     ["Care Recipient Behavior", "carer"]),
    ("I want to understand my sister's condition better.",
     ["Support Needed", "carer", "NHS"]),
    ("I keep cancelling on friends and they've stopped inviting me.",
     ["Balance & Time", "Emotional Impact", "carer"]),
    ("Are there online communities for young carers that actually help?",
     ["Online Support", "young carers", "NHS"]),
]

INTERVIEWER_Q = re.compile(r"^(can you|how do|how did|what|do you|could you|tell me)\b.*\?\s*$",
                           re.IGNORECASE | re.DOTALL)


def looks_like_interviewer_question(text: str) -> bool:
    t = text.strip()
    return bool(INTERVIEWER_Q.match(t)) and t.endswith("?")


def main() -> None:
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        encode_kwargs={"normalize_embeddings": MANIFEST["normalize_embeddings"]},
    )
    store = FAISS.load_local(str(STORE_PATH), embeddings,
                             allow_dangerous_deserialization=True)
    print(f"Loaded store: {MANIFEST['counts']['total_vectors']} vectors "
          f"({MANIFEST['counts']['web_doc_chunks']} web chunks + "
          f"{MANIFEST['counts']['yac_interview_passages']} YAC passages)\n")

    failures = 0
    for qi, (query, topics) in enumerate(QUERIES, 1):
        results = store.max_marginal_relevance_search(query, k=K, fetch_k=FETCH_K)

        check_a = len(results) == K
        check_b = not any(looks_like_interviewer_question(r.page_content) for r in results)
        def topic_ok(r):
            hay = " ".join([r.metadata.get("category", ""), r.metadata.get("source", ""),
                            r.metadata.get("type", "")])
            return any(t.lower() in hay.lower() for t in topics)
        check_c = any(topic_ok(r) for r in results)

        ok = check_a and check_b and check_c
        failures += (not ok)
        print("=" * 88)
        print(f"[Q{qi}] {query}")
        print(f"  (a) {K} results returned:            {'PASS' if check_a else 'FAIL'}")
        print(f"  (b) no interviewer-style questions:  {'PASS' if check_b else 'FAIL'}")
        print(f"  (c) plausible topic in metadata:     {'PASS' if check_c else 'FAIL'}")
        for ri, r in enumerate(results, 1):
            m = r.metadata
            tag = (f"{m.get('type')} | {m.get('category')}" if m.get("type") == "yac_interview"
                   else f"{m.get('type')} | {m.get('source')}")
            print(f"  --- result {ri} [{tag}]")
            print(f"      {r.page_content[:300].strip()}"
                  f"{'...' if len(r.page_content) > 300 else ''}")
        print()

    print("=" * 88)
    print(f"SUMMARY: {len(QUERIES) - failures}/{len(QUERIES)} queries passed all "
          f"automated checks.")
    print("NOTE: automated checks are necessary but not sufficient — a human must "
          "review the passages above for actual relevance before calling this done.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
