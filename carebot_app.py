from __future__ import annotations

from pathlib import Path

import streamlit as st

from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage, AIMessage

import PIL.Image

APP_DIR = Path(__file__).resolve().parent

# ------------------------------------------------
# initialize api and LLM model
# ------------------------------------------------

API_KEY = st.secrets["API_KEY"]

# Full "model#deployment" route. On-demand deployments are EPHEMERAL (created fresh per
# study session and deleted after, per the batched-session cost plan — gemma-3-27b-it is
# not serverless, so a live 2xH200 deployment is required whenever this app is in use).
# A hardcoded deployment ID here WILL go stale the moment that deployment is torn down —
# that was the root cause of the previous dead-model bug. Set this via .streamlit/secrets.toml
# (same file as API_KEY) and update it each time deploy_for_session.sh brings up a new
# deployment. Recommended base model per the evaluation report (2026-07-15): v2
# (carebot-gemma3-27b-v2), which showed the strongest and most thoroughly validated results.
#
# Example secrets.toml entry:
#   MODEL = "accounts/yacchatbot/models/carebot-gemma3-27b-v2#accounts/yacchatbot/deployments/<id>"
MODEL = st.secrets["MODEL"]

@st.cache_resource
def load_llm():
    # Matches the generation config actually used in evaluation (run_eval.py
    # GEN_TEMPERATURE / GEN_MAX_TOKENS). Only these two were set there, so only these two
    # are set here. The previous top_p/top_k/presence_penalty/frequency_penalty overrides
    # were never evaluated and have been removed.
    # Passed explicitly rather than through model_kwargs: LangChain deprecated the latter
    # and warns on every boot.
    return init_chat_model(
        model=MODEL,
        model_provider="fireworks",
        api_key=API_KEY,
        temperature=0.3,
        max_tokens=400,
    )

llm = load_llm()

# Appended to the final user message on every turn (see the note above llm.generate below).
CONCISENESS_RIDER = "\n\n(Keep your response concise, except when asked for details.)"

# ------------------------------------------------
# create profile received from URL parameters
# ------------------------------------------------

PROFILE_FIELDS = [
    # required
    {"key": "name", "label": "Name:"},
    {"key": "age", "label": "Age:"},
    {"key": "gender", "label": "Gender:"},
    {"key": "location_country", "label": "Country of residence:"},

    {"key": "location_city", "label": "City of residence:"},
    {"key": "study_subject", "label": "Study:"},
    {"key": "religion", "label": "Religion:"},
    {"key": "religion_importance", "label": "Importance of religion:"},
    {"key": "ethnicity", "label": "Ethnic/family origins:"},

    {"key": "informal_care_count", "label": "Number of adults (18+) cared for:"},
    {"key": "age_loved_one", "label": "Age(s) of loved one(s):"},
    {"key": "relation_loved_one", "label": "Relation to loved one(s):"},
    {"key": "condition_loved_one", "label": "Loved one(s) health condition(s):"},
    {"key": "duration_loved_one", "label": "Duration of loved one(s) condition:"},
    {"key": "care_time", "label": "Duration(s) of providing care:"},
    {"key": "most_care_time", "label": "Provides most care:"},
    {"key": "other_care", "label": "Number of paid care workers:"},
    {"key": "satisfaction", "label": "Satisfaction with relationship:"},

    {"key": "prefers_quick_response", "label": "Prefers quick response:"},
]

params = st.query_params

profile = {}

for field in PROFILE_FIELDS:
    key = field["key"]
    value = params.get(key, "N/A")

    # special case - prepend a space before name
    if key == "name":
        profile[key] = " " + value
    else:
        profile[key] = value

user_profile = " | ".join(
    f"{field['label']} {profile.get(field['key'], 'N/A')}"
    for field in PROFILE_FIELDS
)

# ------------------------------------------------
# miscellaneous loads
# ------------------------------------------------

@st.cache_resource
def load_pfps():
    # Paths resolved relative to this file's own location (APP_DIR), not the process's
    # working directory — the previous "streamlit/static/..." string assumed a specific
    # launch directory and crashed on startup otherwise.
    static_dir = APP_DIR / "static"
    return PIL.Image.open(static_dir / "carebot_pfp.png"), \
        PIL.Image.open(static_dir / "carebot_pfp_larger.png"), \
        PIL.Image.open(static_dir / "user_pfp.png")

bot_pfp, bot_pfp_larger, user_pfp = load_pfps()

# ------------------------------------------------
# streamlit start
# ------------------------------------------------

st.set_page_config(page_title="Carebot", page_icon="❤️", layout="wide")

st.title("Carebot")
st.caption("I'm here to listen and help 🤗")

# init and show chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar=m.get("avatar", "🤖")):
        st.markdown(m["content"])

# greet the user once at start
if "greeted" not in st.session_state:
    with st.chat_message("assistant", avatar=bot_pfp):
        st.markdown(f"Hi{profile['name']}, nice to meet you!")

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Hi{profile['name']}, nice to meet you!",
        "avatar": bot_pfp
    })

    st.session_state.greeted = True
    
# create chat input field 
if prompt := st.chat_input("What is on your mind?"):
    
    # store and display the current prompt.
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "avatar": user_pfp}
    )

    with st.chat_message("user", avatar=user_pfp):
        st.markdown(prompt)

    # convert session messages to langchain message objects
    session_messages = []

    for m in st.session_state.messages:
        role = m.get("role", "user")
        content = m.get("content", "")

        if role == "system":
            session_messages.append(SystemMessage(content=content))
        elif role == "assistant":
            session_messages.append(AIMessage(content=content))
        else:
            session_messages.append(HumanMessage(content=content))

    # RAG intentionally removed (evaluation report, 2026-07-15): blinded human review found
    # gated retrieval degraded replies on 85% of the queries where it fired (11-2-2 verdict,
    # human_review_pack_v2_clean.md), corroborated by debiased LLM-judge pairwise comparisons
    # (~60/40 against RAG). The fine-tuned model alone outperforms both the base model and
    # the RAG-augmented fine-tune, so no retrieval step runs here.
    instruction = (
        "You are Carebot, a warm, empathic, supportive assistant. "
        "You speak kindly and clearly, avoid medical or legal claims, and focus on practical, everyday help. "
        "Reflect feelings, validate, suggest small steps and resources, and encourage seeking trusted adults or professionals when appropriate. "
        "Keep answers concise but caring. Use the user's profile to personalize your tone and suggestions:\n "
        f"{user_profile}\n\n"
        "If the user prefers a quick response, immediately give your advice. If not, employ scaffolding techniques and ask one or two questions"
        "to better understand the situation before giving advice. Keep this scaffolding process concise.\n\n"
        "Here is the user query:\n\n"
    )

    # Gemma's chat template has no system role and requires strict user/assistant
    # alternation. Fireworks folds a LEADING system message into the first user turn, but a
    # system message arriving AFTER a user turn has nowhere to go and the template render
    # fails server-side as a 500 (internal_server_error / invalid_request_error). The
    # conciseness rider therefore has to travel inside the final user message instead of as
    # a trailing SystemMessage. Models with a real system role (e.g. Llama) tolerate the old
    # form, which is why this only shows up against the Gemma fine-tune.
    if session_messages and isinstance(session_messages[-1], HumanMessage):
        session_messages[-1] = HumanMessage(
            content=session_messages[-1].content + CONCISENESS_RIDER
        )

    all_context = [SystemMessage(content=instruction)] + session_messages

    # generate
    with st.spinner("Thinking..."):
        response = llm.generate([all_context])

    assistant_text = ""

    try:
        assistant_text = response.generations[0][0].text or ""
    except Exception:
        assistant_text = "Sorry, I couldn't generate a response. Try again later."

    # display
    with st.chat_message("assistant", avatar=bot_pfp):
        st.markdown(assistant_text)

    # append the message into history
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_text, "avatar": bot_pfp}
    )
