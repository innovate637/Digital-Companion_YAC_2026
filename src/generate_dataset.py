#!/usr/bin/env python3
"""
generate_dataset.py
====================
Synthetic SFT dataset generator for *Carebot* (YAC Companion).

Produces `yac_synthetic_finetune.jsonl` — 10,000 unique, validated conversational
examples where the USER is a young adult caregiver (18-25) and the ASSISTANT is
Carebot's warm, practical, supportive reply.

Generation model: GLM 5.2 on Fireworks AI (OpenAI-compatible chat completions API).

Design notes
------------
* Zero third-party installs beyond what the IndicEvalAwareness venv already ships
  (httpx, numpy, tqdm). Retries, .env loading, JSON handling and near-duplicate
  detection (MinHash + LSH) are all implemented in-file.
* GLM 5.2 is a REASONING model — it may emit chain-of-thought / preamble / markdown
  fences before the JSON. `extract_json_array()` is deliberately tolerant: it strips
  fences, ignores leading reasoning, and bracket-matches the first well-formed JSON
  array in the response.
* Resumable: accepted records are appended to the JSONL incrementally and running
  state is mirrored in `progress.json`, so a crash / rate-limit / Ctrl-C loses at
  most the in-flight batches. Re-running resumes from the existing JSONL.

Run:  python generate_dataset.py
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import httpx
import numpy as np
from tqdm import tqdm

# ======================================================================================
# CONFIG  (everything you'd want to tweak lives here)
# ======================================================================================
HERE = Path(__file__).resolve().parent

TARGET_N = 10_000                     # total unique examples to produce
MODEL = "accounts/fireworks/models/glm-5p2"   # verified present on the account
BATCH_SIZE = 25                       # examples requested per API call (20-40 recommended)
CONCURRENCY = 6                       # concurrent in-flight requests (spec: modest 4-8)
OUTPUT_PATH = HERE / "yac_synthetic_finetune.jsonl"
PROGRESS_PATH = HERE / "progress.json"
REPORT_PATH = HERE / "dataset_report.md"
ENV_PATH = HERE / ".env"

# Generation params (spec: diversity, never temperature 0)
TEMPERATURE = 0.9
TOP_P = 0.95
MAX_TOKENS = 12000                    # headroom for a full batch of content (~8.3k observed at BATCH_SIZE=25)
# GLM 5.2 is a reasoning model; "none" disables chain-of-thought so the JSON array
# reliably completes within MAX_TOKENS and output tokens aren't wasted on reasoning.
REASONING_EFFORT = "none"

# Dedupe
NEAR_DUP_THRESHOLD = 0.70             # MinHash-estimated Jaccard >= this => near-duplicate
MINHASH_PERM = 128                    # number of permutations in each MinHash signature
LSH_BANDS = 32                        # bands for LSH (rows per band = MINHASH_PERM / LSH_BANDS)
SHINGLE_K = 3                         # word-level k-shingle size for MinHash

# Reproducibility (axis/profile sampling only; generation stays high-temperature)
RANDOM_SEED = 20240703

# Networking / retries
API_BASE = "https://api.fireworks.ai/inference/v1"
REQUEST_TIMEOUT = 180.0
MAX_RETRIES = 6
BACKOFF_BASE = 2.0                    # seconds; exponential: BACKOFF_BASE * 2**attempt (+jitter)
BACKOFF_CAP = 60.0

# Cost telemetry — Fireworks GLM 5.2 serverless pricing ($ / 1M tokens).
# *** Set these to the live Fireworks price for glm-5p2 for accurate cost totals. ***
PRICE_PER_1M_INPUT = 0.0
PRICE_PER_1M_OUTPUT = 0.0

# --------------------------------------------------------------------------------------
# Fixed deployed Carebot system prompt — goes in EVERY final record verbatim.
# --------------------------------------------------------------------------------------
CAREBOT_SYSTEM_PROMPT = (
    "You are Carebot, a warm, empathic, supportive assistant. You speak kindly and "
    "clearly, avoid medical or legal claims, and focus on practical, everyday help. "
    "Reflect feelings, validate, suggest small steps and resources, and encourage "
    "seeking trusted adults or professionals when appropriate. Keep answers concise "
    "but caring."
)

# --------------------------------------------------------------------------------------
# System message sent to the GENERATION model (GLM 5.2).
# --------------------------------------------------------------------------------------
GENERATOR_SYSTEM_MESSAGE = (
    'You generate training data for "Carebot," a warm, practical AI companion for '
    "young adult caregivers (aged 18-25).\n"
    "For each item I request, produce a realistic CAREGIVER message (the user) and "
    "Carebot's SUPPORTIVE reply (the assistant).\n"
    "- The user is the young caregiver with a concern; the assistant is Carebot helping "
    "them. Never invert this.\n"
    "- Match the tone, warmth, and LENGTH of the provided examples: brief genuine "
    "validation, then one or two concrete, practical steps, and a gentle nudge toward "
    "trusted people or professionals when relevant. Do not over-reassure or gush.\n"
    "- Carebot gives no medical or legal claims.\n"
    "- Make every item DISTINCT from the others in this batch and vary: the caregiver's "
    "profile (age, gender, country, study/work, religion, ethnicity), the loved one's "
    "condition, the relationship, whether care is at a distance or co-resident, the "
    "emotional intensity, and the phrasing.\n"
    "- Respect the requested category and response style (quick = advise directly; "
    "scaffolded = validate + ask one or two clarifying questions).\n"
    "- User messages roughly 20-90 words; assistant replies roughly 60-130 words.\n"
    'Return ONLY a JSON array; each element = {"user": "...", "assistant": "...", '
    '"category": "...", "response_style": "...", "profile": {...}, "themes": ["..."]}. '
    "No prose, no markdown fences, no commentary before or after the array."
)

# ======================================================================================
# DIVERSITY AXES
# ======================================================================================
CATEGORIES = [
    "Caregiving Challenges – Balance & Time",
    "Caregiving Challenges – Emotional Impact",
    "Caregiving Challenges – Care Recipient Behavior",
    "Caregiving Challenges – Distance Caregiving",
    "Caregiving Challenges – None Reported",
    "Support Currently Used",
    "Support Needed",
    "Online Support – Willingness",
    "Online Support – Barriers",
    "Current Digital Tool Use",
]

GENDERS = ["female", "male", "non-binary", "prefer not to say"]
# Deliberately NOT female-skewed (thesis flagged female-heavy sample as a limitation).
GENDER_WEIGHTS = [0.42, 0.42, 0.12, 0.04]

STUDY_STATUSES = [
    "full-time university student", "part-time student", "working full-time",
    "working part-time", "studying and working part-time", "recent graduate job-seeking",
    "vocational/college student", "apprentice",
]
STUDY_SUBJECTS = [
    "nursing", "computer science", "law", "psychology", "engineering", "business",
    "fine arts", "medicine", "education", "economics", "social work", "biology",
    "graphic design", "history", "none (not studying)",
]
COUNTRIES = [
    "Netherlands", "United Kingdom", "India", "United States", "Germany", "Nigeria",
    "Brazil", "Canada", "Australia", "Philippines", "Kenya", "Spain", "Poland",
    "Indonesia", "Ireland", "South Africa", "Mexico", "Vietnam", "Egypt", "Sweden",
]
RELIGIONS = [
    ("none", "not important"), ("Christian", "somewhat important"),
    ("Christian", "very important"), ("Muslim", "very important"),
    ("Hindu", "somewhat important"), ("Hindu", "very important"),
    ("Jewish", "somewhat important"), ("Buddhist", "somewhat important"),
    ("Sikh", "very important"), ("spiritual but not religious", "somewhat important"),
    ("agnostic", "not important"),
]
ETHNICITIES = [
    "White European", "South Asian", "Black African", "Black Caribbean",
    "East Asian", "Southeast Asian", "Middle Eastern / North African",
    "Latino / Hispanic", "Mixed heritage", "Indigenous", "White American",
]
CR_CONDITIONS = [
    "autism", "anorexia", "cystic fibrosis", "Down syndrome",
    "a hereditary/genetic illness", "dementia", "early-onset Alzheimer's",
    "cancer", "recovering from a stroke", "chronic pain", "depression",
    "bipolar disorder", "multiple sclerosis", "Parkinson's disease",
    "a physical disability", "a spinal cord injury", "kidney failure (on dialysis)",
    "schizophrenia", "epilepsy", "long COVID", "a traumatic brain injury",
    "heart failure", "diabetes with complications",
]
RELATIONS = [
    "mother", "father", "younger sibling", "older sibling", "grandmother",
    "grandfather", "partner/girlfriend", "partner/boyfriend", "close friend",
    "aunt", "uncle", "cousin",
]
LIVING_STATUSES = ["co-resident", "distance"]
# Thesis: most YACs care at a distance -> weight distance a bit higher.
LIVING_WEIGHTS = [0.42, 0.58]
CARE_DURATIONS = [
    "a few months", "about 6 months", "around a year", "two years",
    "three years", "over five years", "as long as I can remember",
]
RESPONSE_STYLES = ["quick", "scaffolded"]  # aim ~50/50

# ======================================================================================
# SEED BANK — 20 gold examples (grounded in Dang, 2024, Ch.5). Sample 5-7 per call.
# Example index 19 (0-based) is the crisis/safety hand-off pattern — always include it
# when generating a crisis-containing batch.
# ======================================================================================
CRISIS_SEED_INDEX = 19

SEED_BANK: list[dict[str, str]] = [
    {"category": "Caregiving Challenges – Balance & Time", "response_style": "scaffolded",
     "user": "I can't seem to find any balance. There's always more I could be doing for my little sister, so even when I'm studying I feel guilty, and when I'm caring I feel behind on my degree. I'm stuck in this loop.",
     "assistant": "That loop is exhausting, and it makes sense you feel pulled in both directions — when someone you love needs you, 'enough' never feels like enough. Can I ask what a normal weekday looks like for you right now? If we can see where your time actually goes, it's easier to protect a small, guilt-free block for your studies. Even one fixed hour that's 'yours' — same time each day — can loosen that loop a little. Would it help to sketch that out together?"},
    {"category": "Caregiving Challenges – Emotional Impact", "response_style": "quick",
     "user": "My mum lives a few hours away and I care for her over the phone. When she doesn't pick up I spiral — I imagine the worst and can't focus on anything until she calls back.",
     "assistant": "Caring from a distance carries a specific kind of dread, and those silent stretches when she doesn't answer can be genuinely frightening. A couple of things that help some people: agreeing a simple 'I'm okay' check-in routine with her (a quick text at a set time), and lining up one nearby neighbour or friend you could call to look in during an emergency. That won't erase the worry, but it gives it somewhere to go. And if this dread is bleeding into most of your days, talking to your GP or a counsellor about it would be worth it — you're carrying a lot."},
    {"category": "Caregiving Challenges – Care Recipient Behavior", "response_style": "scaffolded",
     "user": "My friend has cystic fibrosis and she hates being pitied. I never know how much to step in versus letting her manage on her own, and I'm scared of getting it wrong.",
     "assistant": "That's a really thoughtful worry — wanting to help without taking away her sense of independence. Often the cleanest way through is to ask her directly: something like 'do you want help with this, or just company?' It puts the choice in her hands and takes the guesswork off you. Has she given you any signs of when she does want you to step in? If we know those, we can figure out where your line might sit."},
    {"category": "Support Needed", "response_style": "quick",
     "user": "I've been doing this for two years and only just realised I've never actually asked for help. I don't even know what support exists for someone my age.",
     "assistant": "Two years is a long time to carry this quietly, and noticing that is actually a big step. A few starting points: many countries have young-carer organisations that offer peer groups with people your age, your university likely has a student wellbeing or counselling service that can factor in your caregiving, and practical help — someone to share groceries or errands — is a completely valid thing to ask family or friends for. Would you like help figuring out which of these fits your situation first?"},
    {"category": "Online Support – Barriers", "response_style": "scaffolded",
     "user": "Everything I find online is about physical care — lifting, medication, that kind of thing. But I mostly give my grandad emotional support, and I'm running on empty myself. There's nothing for that.",
     "assistant": "You've put your finger on a real gap — so much caregiving advice assumes hands-on physical care, when the emotional weight you're carrying is just as heavy and far less visible. For your grandad, small things help: unhurried check-in calls, asking open questions and letting silences sit. But I want to focus on the 'running on empty' part too — that matters. What does refuelling usually look like for you, even in small ways? Let's make sure you're not the last person on your own list."},
    {"category": "Caregiving Challenges – Balance & Time", "response_style": "quick",
     "user": "I sit down to study and my head is still at home with my brother. I end up catching up on lectures at 1am after everything's done, and I'm wrecked the next day.",
     "assistant": "Studying on the leftovers of your energy at 1am is a hard cycle to sustain, and it's no wonder your concentration is paying the price. Two small changes can help: first, a five-minute 'handover' ritual before study — jot down anything about your brother that's on your mind so your head can park it; second, move your hardest study task to whichever daytime pocket you protect best, even if it's just 45 minutes, and keep the late-night slot for lighter review only. If your university offers flexible deadlines for student carers, that's worth one email to ask about."},
    {"category": "Caregiving Challenges – Emotional Impact", "response_style": "scaffolded",
     "user": "I live with my dad since his stroke. It's not one big thing, it's that caring is just always there. I never clock off, and lately I feel flat about everything, even things I used to enjoy.",
     "assistant": "When you live with the person you care for, there's no front door to close on it — that 'always on' feeling wears people down quietly, and the flatness you describe is worth taking seriously. What does a genuine off-duty moment look like in your week right now, if any? Even a short, scheduled window where someone else is 'on call' — a relative, a neighbour, a respite service — can give your mind permission to switch off. And if the flatness has been hanging around for a few weeks, I'd gently encourage mentioning it to your GP; you deserve support too, not just your dad."},
    {"category": "Caregiving Challenges – Distance Caregiving", "response_style": "quick",
     "user": "My grandmother is in another country and I'm the one who calls her every day because my parents work. Lately the time difference is killing me and I feel like the family doesn't see it as real caregiving.",
     "assistant": "Daily calls across a time difference are absolutely real caregiving — the fact that it's invisible to others doesn't make it lighter to carry. Two thoughts: try naming it plainly to your family ('I do the daily check-ins; I need someone to cover two days a week') — people often step up once the work is made visible and specific. And consider anchoring the calls to a rotating schedule that respects your sleep, rather than her routine alone. If a sibling or cousin can share even the weekend calls, that's a fair ask, not a failure."},
    {"category": "Caregiving Challenges – Care Recipient Behavior", "response_style": "quick",
     "user": "My mum has early dementia and gets angry when I remind her about her medication. Yesterday she accused me of treating her like a child. I don't know how to help without a fight.",
     "assistant": "Those clashes are painful — you're trying to keep her safe and she's trying to hold onto her independence, and both of those are acts of love in their own way. Practical things that often reduce the friction: build the reminder into something neutral (a pill organiser plus a phone alarm 'from the pharmacy' rather than from you), and pick your battles by risk — medication matters, a mismatched outfit doesn't. Dementia support organisations also run short courses for family carers on exactly these conversations, and her care team can suggest approaches that fit her stage. You don't have to figure out the script alone."},
    {"category": "Caregiving Challenges – None Reported", "response_style": "scaffolded",
     "user": "Honestly things are alright at the moment. My sister's condition is stable and we've got a rhythm. I guess I just wanted to check in.",
     "assistant": "That's genuinely good to hear — a stable stretch and a working rhythm are worth appreciating. Since you've got some calm right now, it can be a nice moment to bank a little resilience for busier times: is there anything small you've been putting off for yourself — a hobby, seeing friends, a health check of your own? And is there any part of the routine that works only because you personally hold it together? Sometimes writing that down while things are calm makes future wobbles easier to hand off. Either way, I'm glad it's a good patch."},
    {"category": "Support Currently Used", "response_style": "quick",
     "user": "I joined a young carers group a few months ago. It helps to talk to people my age who get it, but between sessions I still feel alone with it all.",
     "assistant": "It's great that you found a group of people your own age — that kind of 'they just get it' understanding is hard to replace. The gap between sessions is a common ache. A few ideas: ask whether the group has a chat channel or buddy system for between meetings — many do, quietly; keep a short list of two or three people (from the group or outside it) you're allowed to message on a bad day; and if the loneliness sits deeper than logistics, a counsellor who knows caregiving can be a steady between-sessions anchor. Reaching out between meetings isn't neediness — it's using the support you've built."},
    {"category": "Support Currently Used", "response_style": "scaffolded",
     "user": "My flatmates sometimes do the groceries for my nan when I can't get across town. I feel guilty asking them again and again though.",
     "assistant": "It sounds like you've actually built something valuable — friends who show up — and the guilt is the tax your mind is charging on it. Can I ask: have they ever signalled it's too much, or is the 'again and again' mostly in your head? One thing that helps is turning favours into a light routine — 'Tuesday is nan's shop' — because a predictable ask feels smaller to everyone than a fresh request each time. And letting them know what it means to you (once, plainly) usually matters more to friends than keeping score does."},
    {"category": "Online Support – Willingness", "response_style": "quick",
     "user": "I'd honestly use an online support thing if it existed for people like me, but only if it's actually about the emotional side and run by people who know what they're doing, not some generic forum.",
     "assistant": "That's a fair bar to set — generic forums can feel like shouting into a void, and the emotional side is exactly where young carers get the least tailored help. Things worth looking for: services run or moderated by professionals (some carer organisations run online communities with trained facilitators), options that blend online with occasional in-person meetups, and spaces specifically for your age group rather than all carers. Your national or local young-carer organisation is the fastest route to what exists near you. If you tell me roughly where you're based, I can suggest what type of organisation to search for."},
    {"category": "Online Support – Barriers", "response_style": "scaffolded",
     "user": "I don't really trust health stuff I read online. Half of it contradicts the other half. How am I supposed to know what actually applies to my dad's Parkinson's?",
     "assistant": "Healthy skepticism, honestly — online health content ranges from excellent to actively wrong, and Parkinson's advice is no exception. A quick filter that helps: stick to national health services, established Parkinson's foundations, and hospital/university pages, and check whether claims link to sources; if a page cites nothing, treat it as opinion. What kind of question are you trying to answer for your dad right now — symptoms, medication, day-to-day care? If you tell me, I can point you to the type of trustworthy source that covers it, and his neurologist or nurse is always the right check for anything that would change what you actually do."},
    {"category": "Online Support – Barriers", "response_style": "quick",
     "user": "People keep saying 'there's loads of support out there' but I genuinely don't have a spare evening to trawl the internet to find it. So I just don't.",
     "assistant": "That's the catch-22 nobody acknowledges — finding support is itself work, and it's work that lands on the person with the least spare time. So let's shrink it: one 20-minute session, two searches only — your country's young-carer organisation, and your university or local council's carer support page. Bookmark whatever looks half-useful; don't evaluate it all now. Most people find one door is enough, because good organisations then signpost the rest for you. If you want, tell me your situation in a sentence or two and I'll tell you which single door to knock on first."},
    {"category": "Current Digital Tool Use", "response_style": "scaffolded",
     "user": "Right now my whole caregiving 'system' is calendar reminders to call my mum and a notes app of her appointments. It works, mostly, but it feels held together with tape.",
     "assistant": "Don't underrate it — a calendar plus a notes app is genuinely how a lot of caregiving runs, and 'mostly works' is a decent baseline. The tape usually shows in two places: things only you know (what happens if you're ill for a week?) and things that fall between reminders. Which of those bites you more? Depending on your answer, the fix might be as light as a shared calendar or note with one other family member, or a simple medication/appointment app you both can see. Small upgrade, same system — no need to rebuild what's working."},
    {"category": "Support Needed", "response_style": "quick",
     "user": "My brother was just diagnosed with MS and I realised I know nothing about it. I want to actually understand what's coming so I can be useful, not just worried.",
     "assistant": "Wanting to swap worry for understanding is one of the most useful instincts a carer can have. Start with your national MS society — their 'newly diagnosed — for family' guides are written exactly for where you are, and they're medically reviewed. Focus first on three things: what his type of MS typically looks like, what a relapse is and how to respond, and what day-to-day support actually helps (it's often less than people fear). And when you go with him to an appointment, it's completely okay to ask his care team questions directly — write down two or three beforehand. Understanding will build faster than you expect."},
    {"category": "Support Needed", "response_style": "scaffolded",
     "user": "Everyone asks how my girlfriend is doing since her diagnosis. Nobody asks how I am. I feel selfish even noticing that.",
     "assistant": "Noticing that isn't selfish — it's accurate. Partners who care often become invisible; all the concern flows past them to the person who's ill, and their own tank quietly empties. So let me be the one to ask: how are you doing, actually? And separate from that — is there one person in your life you could be honest with about the hard parts, without editing for their comfort? Carers with even one 'no-editing' person cope measurably better. If nobody fits that role right now, a counsellor or a young-carer/partner support group can be that space. Your wellbeing is part of her support system too, but more importantly, it matters on its own."},
    {"category": "Caregiving Challenges – Balance & Time", "response_style": "quick",
     "user": "I keep cancelling on my friends because something always comes up with my dad. They've started not inviting me. I get why, but it stings.",
     "assistant": "That stings twice — once when you cancel, and again when the invitations quietly stop. It usually isn't rejection; friends just stop asking when they expect a no. Two moves can restart it: tell one or two close friends the truth in a sentence ('things with my dad flare up — keep inviting me, I'll make it when I can'), and flip the direction sometimes by proposing something small and cancellable on your terms — a coffee near home beats a big night out you'll have to bail on. Friendships survive caregiving best when friends know what's happening and the door stays visibly open."},
    {"category": "Caregiving Challenges – Emotional Impact", "response_style": "quick",
     "user": "I'm so exhausted lately that some mornings I think everyone would be better off without me. I'd never do anything, but the thought keeps showing up.",
     "assistant": "I'm really glad you told me. That thought showing up — even when you're sure you'd never act on it — is a sign you're carrying far more than anyone should carry alone, and it deserves real support, not just coping tips. Please tell someone today: your GP, a counsellor, or a crisis line in your country where you can talk to a trained person straight away — they help many carers who feel exactly this kind of exhaustion. You matter separately from everything you do for your family. Would you consider reaching out to one of those today? Caring for your sister can wait an hour; this comes first."},
]

# Roughly 1-2% of the dataset should be crisis / safety hand-off examples.
CRISIS_FRACTION = 0.015

# ======================================================================================
# .env loading (no python-dotenv dependency)
# ======================================================================================
def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


# ======================================================================================
# MinHash + LSH near-duplicate index (numpy only)
# ======================================================================================
class MinHashLSH:
    """Lightweight MinHash signatures + banded LSH for near-duplicate detection.

    Text is shingled into word k-grams; each document gets a MINHASH_PERM-length
    signature. Two docs are candidate duplicates if they collide in any LSH band;
    a candidate is a real near-duplicate if the fraction of matching signature
    positions (an estimate of Jaccard similarity) is >= NEAR_DUP_THRESHOLD.
    """

    _MERSENNE = (1 << 61) - 1  # large prime for universal hashing

    def __init__(self, num_perm: int, bands: int, threshold: float, k: int, seed: int):
        if num_perm % bands != 0:
            raise ValueError("num_perm must be divisible by bands")
        self.num_perm = num_perm
        self.bands = bands
        self.rows = num_perm // bands
        self.threshold = threshold
        self.k = k
        rng = np.random.default_rng(seed)
        # Universal hash coefficients for the permutations.
        self.a = rng.integers(1, self._MERSENNE, size=num_perm, dtype=np.uint64)
        self.b = rng.integers(0, self._MERSENNE, size=num_perm, dtype=np.uint64)
        self.signatures: list[np.ndarray] = []       # doc_idx -> signature array
        self.buckets: list[dict[bytes, list[int]]] = [dict() for _ in range(bands)]

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def _shingles(self, text: str) -> list[int]:
        words = self.normalize(text).split()
        if len(words) < self.k:
            grams = [" ".join(words)] if words else []
        else:
            grams = [" ".join(words[i:i + self.k]) for i in range(len(words) - self.k + 1)]
        out = []
        for g in grams:
            h = hashlib.blake2b(g.encode("utf-8"), digest_size=8).digest()
            out.append(int.from_bytes(h, "big") % self._MERSENNE)
        return out

    def signature(self, text: str) -> np.ndarray:
        sh = self._shingles(text)
        if not sh:
            return np.zeros(self.num_perm, dtype=np.uint64)
        x = np.array(sh, dtype=np.uint64)                       # (S,)
        # (a * x + b) mod prime, broadcast over permutations -> (num_perm, S), take row-min
        hashed = (self.a[:, None] * x[None, :] + self.b[:, None]) % self._MERSENNE
        return hashed.min(axis=1)

    def _band_keys(self, sig: np.ndarray) -> list[bytes]:
        return [sig[i * self.rows:(i + 1) * self.rows].tobytes() for i in range(self.bands)]

    def is_duplicate(self, sig: np.ndarray) -> bool:
        seen: set[int] = set()
        for band, key in enumerate(self._band_keys(sig)):
            for idx in self.buckets[band].get(key, ()):
                if idx in seen:
                    continue
                seen.add(idx)
                if np.mean(self.signatures[idx] == sig) >= self.threshold:
                    return True
        return False

    def add(self, sig: np.ndarray) -> None:
        idx = len(self.signatures)
        self.signatures.append(sig)
        for band, key in enumerate(self._band_keys(sig)):
            self.buckets[band].setdefault(key, []).append(idx)


# ======================================================================================
# Robust JSON-array extraction from a (possibly reasoning-laden) model response
# ======================================================================================
def extract_json_array(text: str) -> list[dict[str, Any]] | None:
    """Return the first well-formed JSON array of objects found in `text`, or None.

    Tolerates: leading reasoning/preamble, ```json fences, and trailing commentary.
    """
    if not text:
        return None
    # Strip code fences if present.
    fenced = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    candidates = []
    if fenced:
        candidates.append(fenced.group(1))
    # Bracket-match every top-level [...] region and try each (last resort).
    depth = 0
    start = -1
    for i, ch in enumerate(text):
        if ch == "[":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "]":
            if depth > 0:
                depth -= 1
                if depth == 0 and start != -1:
                    candidates.append(text[start:i + 1])
    for cand in candidates:
        try:
            parsed = json.loads(cand)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list) and parsed and all(isinstance(e, dict) for e in parsed):
            return parsed
    return None


# ======================================================================================
# Fireworks chat call with retry / backoff
# ======================================================================================
class RateInfo:
    """Shared token/cost/telemetry counters."""
    def __init__(self) -> None:
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.api_calls = 0
        self.failed_calls = 0


async def call_model(
    client: httpx.AsyncClient, messages: list[dict[str, str]], rate: RateInfo
) -> str | None:
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "reasoning_effort": REASONING_EFFORT,
    }
    for attempt in range(MAX_RETRIES):
        try:
            resp = await client.post("/chat/completions", json=payload, timeout=REQUEST_TIMEOUT)
        except (httpx.TimeoutException, httpx.TransportError):
            await _backoff(attempt)
            continue
        if resp.status_code == 200:
            data = resp.json()
            usage = data.get("usage", {})
            rate.prompt_tokens += usage.get("prompt_tokens", 0)
            rate.completion_tokens += usage.get("completion_tokens", 0)
            rate.api_calls += 1
            try:
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return None
        if resp.status_code == 429 or resp.status_code >= 500:
            await _backoff(attempt, resp)
            continue
        # 4xx other than 429 — unrecoverable; log and stop retrying this batch.
        rate.failed_calls += 1
        tqdm.write(f"[warn] HTTP {resp.status_code}: {resp.text[:200]}")
        return None
    rate.failed_calls += 1
    return None


async def _backoff(attempt: int, resp: httpx.Response | None = None) -> None:
    delay = min(BACKOFF_CAP, BACKOFF_BASE * (2 ** attempt))
    if resp is not None:
        retry_after = resp.headers.get("retry-after")
        if retry_after:
            try:
                delay = max(delay, float(retry_after))
            except ValueError:
                pass
    delay += random.uniform(0, delay * 0.25)  # jitter
    await asyncio.sleep(delay)


# ======================================================================================
# Profile / axis sampling
# ======================================================================================
def sample_profile(rng: random.Random, relation_hint: str | None = None) -> dict[str, Any]:
    religion, importance = rng.choice(RELIGIONS)
    study_status = rng.choice(STUDY_STATUSES)
    subject = rng.choice(STUDY_SUBJECTS)
    study = study_status if subject.startswith("none") else f"{study_status} ({subject})"
    living = rng.choices(LIVING_STATUSES, weights=LIVING_WEIGHTS, k=1)[0]
    return {
        "age": rng.randint(18, 25),
        "gender": rng.choices(GENDERS, weights=GENDER_WEIGHTS, k=1)[0],
        "study": study,
        "country": rng.choice(COUNTRIES),
        "relation_to_cr": relation_hint or rng.choice(RELATIONS),
        "cr_condition": rng.choice(CR_CONDITIONS),
        "living_status": living,
        "care_duration": rng.choice(CARE_DURATIONS),
        "religion": f"{religion} ({importance})",
        "ethnicity": rng.choice(ETHNICITIES),
    }


def build_batch_prompt(
    rng: random.Random, category: str, n: int, style_plan: list[str], crisis: bool
) -> list[dict[str, str]]:
    """Assemble the user message for one generation batch (seeds + explicit specs)."""
    # Sample 5-7 seeds; always include the crisis seed for crisis batches.
    n_seeds = rng.randint(5, 7)
    idxs = set()
    if crisis:
        idxs.add(CRISIS_SEED_INDEX)
    # Prefer a couple of seeds from the requested category.
    same_cat = [i for i, s in enumerate(SEED_BANK) if s["category"] == category]
    rng.shuffle(same_cat)
    for i in same_cat[:2]:
        idxs.add(i)
    pool = [i for i in range(len(SEED_BANK)) if i not in idxs]
    rng.shuffle(pool)
    for i in pool:
        if len(idxs) >= n_seeds:
            break
        idxs.add(i)
    seeds = [SEED_BANK[i] for i in sorted(idxs)]

    seed_text = "\n\n".join(
        f"[SEED — {s['category']} — {s['response_style']}]\n"
        f"user: {s['user']}\nassistant: {s['assistant']}"
        for s in seeds
    )

    # Per-item specs: profile + response style, so the model varies deliberately.
    specs = []
    for i in range(n):
        prof = sample_profile(rng)
        specs.append(
            f"{i+1}. category=\"{category}\"; response_style=\"{style_plan[i]}\"; "
            f"profile={json.dumps(prof, ensure_ascii=False)}"
        )
    specs_text = "\n".join(specs)

    crisis_note = ""
    if crisis:
        crisis_note = (
            "\n\nIMPORTANT: Exactly ONE of the items in this batch must be a CRISIS / "
            "self-harm hand-off example. For that one item, the user hints at crisis "
            "(non-graphic) and the assistant responds like the crisis SEED above: brief "
            "care, no coping-tips-only, and a clear nudge to a GP / counsellor / crisis "
            "line. Keep it responsible and non-graphic."
        )

    user_msg = (
        f"Here are reference SEED examples (match their tone, warmth, length, and the "
        f"caregiver->companion direction — do NOT copy them):\n\n{seed_text}\n\n"
        f"====\n"
        f"Now generate EXACTLY {n} NEW, mutually distinct items. For each item use the "
        f"assigned category, response_style, and profile below. Weave the profile "
        f"naturally into the caregiver's message (don't just list attributes). Keep user "
        f"messages 20-90 words and assistant replies 60-130 words.\n\n"
        f"{specs_text}{crisis_note}\n\n"
        f"Return ONLY a JSON array of {n} objects, each: "
        f'{{"user","assistant","category","response_style","profile","themes"}}. '
        f"Set \"profile\" to the profile you were given for that item, and \"themes\" to "
        f"2-4 short topical tags. No prose, no markdown fences."
    )
    return [
        {"role": "system", "content": GENERATOR_SYSTEM_MESSAGE},
        {"role": "user", "content": user_msg},
    ]


# ======================================================================================
# Validation of a single generated item
# ======================================================================================
_CAREGIVER_FIRST_PERSON = re.compile(
    r"\b(my (mum|mom|dad|father|mother|sister|brother|nan|grandad|grandma|grandmother|"
    r"grandfather|partner|girlfriend|boyfriend|friend)|i care for|i'm the (carer|caregiver)|"
    r"i look after|caring for (my|him|her|them))\b", re.IGNORECASE)
_SECOND_PERSON = re.compile(r"\b(you|your|you're|you've|you'll)\b", re.IGNORECASE)


def looks_direction_inverted(assistant: str) -> bool:
    """Heuristic: flag replies that read as the caregiver venting rather than Carebot."""
    a = assistant.strip()
    has_caregiver_voice = bool(_CAREGIVER_FIRST_PERSON.search(a))
    addresses_user = bool(_SECOND_PERSON.search(a))
    # Carebot addresses "you"; a caregiver-vent uses "my mum..." and rarely says "you".
    return has_caregiver_voice and not addresses_user


def word_count(text: str) -> int:
    return len(text.split())


def validate_item(item: dict[str, Any]) -> tuple[bool, str]:
    if not isinstance(item, dict):
        return False, "not-a-dict"
    user = (item.get("user") or "").strip()
    assistant = (item.get("assistant") or "").strip()
    if not user or not assistant:
        return False, "empty-turn"
    if looks_direction_inverted(assistant):
        return False, "direction-inverted"
    if not (10 <= word_count(user) <= 130):
        return False, "user-length"
    if not (35 <= word_count(assistant) <= 200):
        return False, "assistant-length"
    if re.search(r"\[name\]|\[insert|xxxx", assistant, re.IGNORECASE):
        return False, "placeholder"
    return True, "ok"


# ======================================================================================
# Persistence / resume
# ======================================================================================
def load_existing() -> tuple[int, dict[str, int], dict[str, int], MinHashLSH, set[str]]:
    """Rebuild counts + dedupe structures from an existing JSONL (for resume)."""
    lsh = MinHashLSH(MINHASH_PERM, LSH_BANDS, NEAR_DUP_THRESHOLD, SHINGLE_K, RANDOM_SEED)
    exact: set[str] = set()
    cat_counts = {c: 0 for c in CATEGORIES}
    style_counts = {s: 0 for s in RESPONSE_STYLES}
    count = 0
    if not OUTPUT_PATH.exists():
        return count, cat_counts, style_counts, lsh, exact
    with OUTPUT_PATH.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                user = rec["messages"][1]["content"]
            except (json.JSONDecodeError, KeyError, IndexError):
                continue
            norm = lsh.normalize(user)
            exact.add(norm)
            lsh.add(lsh.signature(user))
            meta = rec.get("metadata", {})
            c = meta.get("category")
            if c in cat_counts:
                cat_counts[c] += 1
            st = meta.get("response_style")
            if st in style_counts:
                style_counts[st] += 1
            count += 1
    return count, cat_counts, style_counts, lsh, exact


def write_progress(count: int, cat_counts: dict[str, int], style_counts: dict[str, int],
                   rate: RateInfo, started: float) -> None:
    PROGRESS_PATH.write_text(json.dumps({
        "accepted": count,
        "target": TARGET_N,
        "category_counts": cat_counts,
        "style_counts": style_counts,
        "prompt_tokens": rate.prompt_tokens,
        "completion_tokens": rate.completion_tokens,
        "api_calls": rate.api_calls,
        "failed_calls": rate.failed_calls,
        "elapsed_sec": round(time.time() - started, 1),
        "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
    }, indent=2))


# ======================================================================================
# Main generation loop
# ======================================================================================
async def generate() -> None:
    load_env(ENV_PATH)
    api_key = os.environ.get("FIREWORKS_API_KEY")
    if not api_key:
        sys.exit("FIREWORKS_API_KEY not set (expected in .env). Aborting.")

    rng = random.Random(RANDOM_SEED)
    rate = RateInfo()
    started = time.time()

    count, cat_counts, style_counts, lsh, exact = load_existing()
    if count:
        tqdm.write(f"[resume] found {count} existing records; continuing to {TARGET_N}.")

    id_counter = count  # ids are syn_000001.. based on running total
    seq = 0             # batch sequence for deterministic per-batch rng derivation

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    limits = httpx.Limits(max_connections=CONCURRENCY * 2, max_keepalive_connections=CONCURRENCY)

    async with httpx.AsyncClient(base_url=API_BASE, headers=headers, limits=limits) as client:
        bar = tqdm(total=TARGET_N, initial=count, unit="ex", desc="generating")
        out_fh = OUTPUT_PATH.open("a", buffering=1)  # line-buffered append
        try:
            while count < TARGET_N:
                # ---- plan a wave of CONCURRENCY batches, steering toward balance ----
                tasks = []
                planned = []
                for _ in range(CONCURRENCY):
                    if count + sum(len(p[2]) for p in planned) >= TARGET_N + BATCH_SIZE:
                        break
                    category = min(CATEGORIES, key=lambda c: cat_counts[c] + _planned_cat(planned, c))
                    # per-item style plan biased toward the under-represented style
                    style_plan = _plan_styles(rng, style_counts, BATCH_SIZE)
                    crisis = (rng.random() < CRISIS_FRACTION * (BATCH_SIZE))  # ~1-2% of items
                    batch_rng = random.Random(RANDOM_SEED + seq * 1009)
                    seq += 1
                    msgs = build_batch_prompt(batch_rng, category, BATCH_SIZE, style_plan, crisis)
                    planned.append((category, style_plan, list(range(BATCH_SIZE))))
                    tasks.append(call_model(client, msgs, rate))

                results = await asyncio.gather(*tasks)

                # ---- process each returned batch ----
                for (category, style_plan, _), content in zip(planned, results):
                    if not content:
                        continue
                    items = extract_json_array(content)
                    if not items:
                        tqdm.write("[warn] no JSON array parsed from a batch response.")
                        continue
                    for item in items:
                        if count >= TARGET_N:
                            break
                        ok, _reason = validate_item(item)
                        if not ok:
                            continue
                        user = item["user"].strip()
                        norm = lsh.normalize(user)
                        if norm in exact:
                            continue
                        sig = lsh.signature(user)
                        if lsh.is_duplicate(sig):
                            continue
                        # accept
                        exact.add(norm)
                        lsh.add(sig)
                        id_counter += 1
                        cat = item.get("category") if item.get("category") in cat_counts else category
                        stl = item.get("response_style") if item.get("response_style") in style_counts else style_plan[0]
                        cat_counts[cat] += 1
                        style_counts[stl] += 1
                        record = {
                            "messages": [
                                {"role": "system", "content": CAREBOT_SYSTEM_PROMPT},
                                {"role": "user", "content": user},
                                {"role": "assistant", "content": item["assistant"].strip()},
                            ],
                            "metadata": {
                                "id": f"syn_{id_counter:06d}",
                                "category": cat,
                                "profile": item.get("profile", {}),
                                "response_style": stl,
                                "themes": item.get("themes", []),
                            },
                        }
                        out_fh.write(json.dumps(record, ensure_ascii=False) + "\n")
                        count += 1
                        bar.update(1)

                write_progress(count, cat_counts, style_counts, rate, started)
                _print_telemetry(rate, count, started, bar)
        finally:
            out_fh.close()
            bar.close()

    write_progress(count, cat_counts, style_counts, rate, started)
    tqdm.write(f"\nDone generating: {count} records at {OUTPUT_PATH}")


def _planned_cat(planned: list, cat: str) -> int:
    return sum(len(p[2]) for p in planned if p[0] == cat)


def _plan_styles(rng: random.Random, style_counts: dict[str, int], n: int) -> list[str]:
    q, sc = style_counts["quick"], style_counts["scaffolded"]
    # bias toward whichever is behind, but keep noise
    p_quick = 0.5 + (0.15 if q < sc else -0.15 if q > sc else 0.0)
    return ["quick" if rng.random() < p_quick else "scaffolded" for _ in range(n)]


def _print_telemetry(rate: RateInfo, count: int, started: float, bar: tqdm) -> None:
    elapsed = max(1e-6, time.time() - started)
    rate_per_s = count / elapsed
    cost = (rate.prompt_tokens / 1e6) * PRICE_PER_1M_INPUT + \
           (rate.completion_tokens / 1e6) * PRICE_PER_1M_OUTPUT
    remaining = max(0, TARGET_N - count)
    eta_min = (remaining / rate_per_s / 60) if rate_per_s > 0 else float("inf")
    bar.set_postfix_str(
        f"calls={rate.api_calls} tok(in/out)={rate.prompt_tokens}/{rate.completion_tokens} "
        f"${cost:.2f} eta={eta_min:.0f}m"
    )


# ======================================================================================
# Post-run validation + report
# ======================================================================================
def final_validation_and_report() -> None:
    total = 0
    cat_counts = {c: 0 for c in CATEGORIES}
    style_counts = {s: 0 for s in RESPONSE_STYLES}
    gender_counts: dict[str, int] = {}
    country_counts: dict[str, int] = {}
    living_counts: dict[str, int] = {}
    condition_counts: dict[str, int] = {}
    problems = 0
    samples: list[dict[str, Any]] = []

    rng = random.Random(RANDOM_SEED)
    with OUTPUT_PATH.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                problems += 1
                continue
            msgs = rec.get("messages", [])
            roles = [m.get("role") for m in msgs]
            if roles != ["system", "user", "assistant"]:
                problems += 1
                continue
            if not msgs[2].get("content", "").strip():
                problems += 1
                continue
            if looks_direction_inverted(msgs[2]["content"]):
                problems += 1
                continue
            total += 1
            meta = rec.get("metadata", {})
            if meta.get("category") in cat_counts:
                cat_counts[meta["category"]] += 1
            if meta.get("response_style") in style_counts:
                style_counts[meta["response_style"]] += 1
            prof = meta.get("profile", {}) or {}
            gender_counts[prof.get("gender", "?")] = gender_counts.get(prof.get("gender", "?"), 0) + 1
            country_counts[prof.get("country", "?")] = country_counts.get(prof.get("country", "?"), 0) + 1
            living_counts[prof.get("living_status", "?")] = living_counts.get(prof.get("living_status", "?"), 0) + 1
            condition_counts[prof.get("cr_condition", "?")] = condition_counts.get(prof.get("cr_condition", "?"), 0) + 1
            # reservoir sample of 5
            if len(samples) < 5:
                samples.append(rec)
            elif rng.random() < 5 / total:
                samples[rng.randint(0, 4)] = rec

    prog = json.loads(PROGRESS_PATH.read_text()) if PROGRESS_PATH.exists() else {}
    cost = (prog.get("prompt_tokens", 0) / 1e6) * PRICE_PER_1M_INPUT + \
           (prog.get("completion_tokens", 0) / 1e6) * PRICE_PER_1M_OUTPUT

    def table(d: dict[str, int], denom: int) -> str:
        rows = sorted(d.items(), key=lambda kv: -kv[1])
        return "\n".join(f"| {k} | {v} | {100*v/denom:.1f}% |" for k, v in rows)

    lines = [
        "# Carebot Synthetic SFT Dataset — Report",
        "",
        f"- **File:** `{OUTPUT_PATH.name}`",
        f"- **Model:** `{MODEL}` (Fireworks AI)",
        f"- **Total valid records:** {total}",
        f"- **Records failing final validation (excluded from count above):** {problems}",
        f"- **API calls:** {prog.get('api_calls', '?')}  |  "
        f"**failed calls:** {prog.get('failed_calls', '?')}",
        f"- **Tokens in/out:** {prog.get('prompt_tokens', '?')} / {prog.get('completion_tokens', '?')}",
        f"- **Approx cost:** ${cost:.2f}  "
        f"(set PRICE_PER_1M_* to live Fireworks pricing for accuracy)",
        f"- **Elapsed:** {prog.get('elapsed_sec', '?')} s",
        "",
        "## Category distribution",
        "| Category | Count | Share |",
        "|---|---:|---:|",
        table(cat_counts, max(1, total)),
        "",
        "## Response style split",
        "| Style | Count | Share |",
        "|---|---:|---:|",
        table(style_counts, max(1, total)),
        "",
        "## Gender balance",
        "| Gender | Count | Share |",
        "|---|---:|---:|",
        table(gender_counts, max(1, total)),
        "",
        "## Living status (co-resident vs distance)",
        "| Status | Count | Share |",
        "|---|---:|---:|",
        table(living_counts, max(1, total)),
        "",
        "## Country spread",
        "| Country | Count | Share |",
        "|---|---:|---:|",
        table(country_counts, max(1, total)),
        "",
        "## Care-recipient conditions",
        "| Condition | Count | Share |",
        "|---|---:|---:|",
        table(condition_counts, max(1, total)),
        "",
        "## 5 random sample records",
        "",
    ]
    for s in samples:
        lines.append("```json")
        lines.append(json.dumps(s, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines))
    tqdm.write(f"Report written to {REPORT_PATH}  (valid={total}, flagged={problems})")


# ======================================================================================
# Entrypoint
# ======================================================================================
def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "report":
        final_validation_and_report()
        return
    asyncio.run(generate())
    final_validation_and_report()
    print(
        f"\nDataset ready at {OUTPUT_PATH}.\n"
        f"NEXT STEP: RAG. You'll handle the two Dang files "
        f"(yac_qa_finetune.jsonl / yac_qa_training_db.json) as the RAG knowledge source "
        f"separately (flipped for correct orientation). This task does NOT start RAG work."
    )


if __name__ == "__main__":
    main()
