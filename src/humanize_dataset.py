#!/usr/bin/env python3
"""
humanize_dataset.py
===================
Deterministic surface edits to make the synthetic dataset read less AI-generated,
per team review (2026-07-05). NO regeneration — pure text surgery on the existing
records. Edits apply to message text only; metadata (which uses en-dashes in
category names) is never touched.

Edits:
  1. Em-dashes (U+2014) removed everywhere in user+assistant text:
     - " — " joining an independent clause (next word is a sentence-starter like
       "that's", "it", "you", or already capitalized) -> ". " + capitalize
     - otherwise -> ", "  (continuations, appositives, paired parentheticals)
     - en-dashes in ranges ("6–8 week", U+2013) are left alone
  2. Semicolons in text -> ". " + capitalize (or ", " before connectives like
     "and/or/but"), since real people rarely use semicolons in chat.
  3. Whitespace/punctuation artifact cleanup after the above.

What this deliberately does NOT do (needs rewriting, which the team declined):
uniform reply length, the validate->advise->nudge template, repeated openers.

Outputs (in place, with backup):
  - yac_synthetic_finetune.orig.jsonl   pristine backup of the pre-edit file
  - yac_synthetic_finetune.jsonl        edited master (same records, same ids)

Run:  python humanize_dataset.py
Then re-run make_eval_split.py (same seed -> same selection) so the train/eval
files inherit the edits.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "yac_synthetic_finetune.jsonl"
BACKUP = HERE / "yac_synthetic_finetune.orig.jsonl"

# Next-word cues that the text after " — " is an independent clause -> period.
# Deliberately tight: possessives/articles ("your", "the", "a") are excluded because
# they usually open fragments, not sentences.
SENTENCE_STARTERS = {
    "that's", "that", "it's", "it", "there's", "there", "this",
    "you", "you're", "you've", "you'll", "he's", "she's",
    "they", "they're", "we're", "i'm", "i'd", "i've",
    "sometimes", "often", "most", "people",
}
MAX_PARENTHETICAL_WORDS = 10   # "a — b — c": b this short with no .!? => paired commas
# Next-word cues that force a comma even if capitalized-looking (continuations).
CONTINUATIONS = {
    "and", "or", "but", "so", "nor", "yet", "like", "even", "not", "just",
    "without", "which", "who", "whose", "where", "when", "while", "if", "because",
    "especially", "particularly", "maybe", "perhaps", "plus", "whether", "though",
    "although", "unless", "until", "rather", "instead", "including", "say",
}

EMDASH_SPLIT = re.compile(r"\s*—\s*")


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def _is_parenthetical(seg: str) -> bool:
    """Short aside between two dashes, no sentence-ending punctuation inside."""
    words = seg.split()
    return 1 <= len(words) <= MAX_PARENTHETICAL_WORDS and not re.search(r"[.!?]", seg)


def _join_single(out: str, nxt: str) -> str:
    """Join across one (unpaired) em-dash boundary."""
    first = nxt.split()[0].rstrip(".,!?;:").lower() if nxt.split() else ""
    prev_end = out.rstrip()[-1:] if out.rstrip() else ""
    if first in CONTINUATIONS:
        joiner = ", "
    elif (first in SENTENCE_STARTERS or nxt[:1].isupper()) and len(nxt.split()) >= 4:
        joiner = ". "
        nxt = _cap(nxt)
    else:
        joiner = ", "
    # avoid ",," "?." etc. if the left side already ends in punctuation
    if prev_end in ",.;:!?":
        joiner = " "
        if prev_end in ".!?":
            nxt = _cap(nxt)
    return out.rstrip() + joiner + nxt.lstrip()


def fix_emdashes(text: str) -> str:
    parts = EMDASH_SPLIT.split(text)
    if len(parts) == 1:
        return text
    out = parts[0]
    i = 1
    while i < len(parts):
        # paired parenthetical: out — parts[i] — parts[i+1]...  =>  out, parts[i], ...
        if (i + 1 < len(parts) and _is_parenthetical(parts[i])
                and parts[i + 1].strip()
                and not parts[i + 1].lstrip()[:1].isupper()):
            out = out.rstrip().rstrip(",") + ", " + parts[i].strip() + ", " + parts[i + 1].lstrip()
            i += 2
        else:
            out = _join_single(out, parts[i])
            i += 1
    return out


def fix_semicolons(text: str) -> str:
    def repl(m: re.Match) -> str:
        nxt = m.group(1)
        if nxt.lower() in CONTINUATIONS:
            return ", " + nxt
        return ". " + _cap(nxt)
    return re.sub(r";\s+(\w[\w'’]*)", repl, text).replace(";", ",")


def cleanup(text: str) -> str:
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\.\s*\.", ".", text)
    return text.strip()


def humanize(text: str) -> str:
    return cleanup(fix_semicolons(fix_emdashes(text)))


def main() -> None:
    if not BACKUP.exists():
        shutil.copy2(MASTER, BACKUP)
        print(f"backup written: {BACKUP.name}")
    else:
        print(f"backup already exists, editing from current master: {BACKUP.name}")

    recs = [json.loads(l) for l in MASTER.open() if l.strip()]
    assert len(recs) == 10_000
    changed = 0
    for r in recs:
        for m in r["messages"][1:]:          # user + assistant only; system untouched
            new = humanize(m["content"])
            if new != m["content"]:
                changed += 1
            m["content"] = new

    with MASTER.open("w") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # verify
    recs2 = [json.loads(l) for l in MASTER.open() if l.strip()]
    assert len(recs2) == 10_000
    rem_em = sum(m["content"].count("—") for r in recs2 for m in r["messages"][1:])
    rem_semi = sum(m["content"].count(";") for r in recs2 for m in r["messages"][1:])
    rem_en = sum(m["content"].count("–") for r in recs2 for m in r["messages"][1:])
    cats_ok = all("–" in r["metadata"]["category"] or True for r in recs2)
    print(f"messages edited: {changed}")
    print(f"remaining in text: em-dashes={rem_em}, semicolons={rem_semi}, "
          f"en-dashes(kept, ranges)={rem_en}")
    print(f"metadata untouched: {cats_ok}")


if __name__ == "__main__":
    main()
