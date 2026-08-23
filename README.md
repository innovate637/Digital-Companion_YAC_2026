# Carebot — YAC Digital Companion (study app)

Streamlit chat app used for the young adult caregiver (YAC) user study. It serves the
fine-tuned Carebot model over the Fireworks API and is embedded inside a Qualtrics survey.

The research pipeline (dataset generation, fine-tuning prep, RAG build, evaluation harness,
all results) lives on the `legacy` branch. That branch contains real participant data. Keep
this repository private.

## Contents

| Path | Purpose |
|---|---|
| `carebot_app.py` | The whole app: profile intake, chat loop, Fireworks call |
| `static/` | Avatars and the Baloo2 font files |
| `.streamlit/config.toml` | Theme and static file serving |
| `requirements.txt` | Pinned dependencies |
| `secrets.toml.example` | Template for the secrets file |

## Secrets

Two values, both required. Locally they go in `.streamlit/secrets.toml`, which is gitignored.
On Streamlit Community Cloud they go in the app's Secrets panel.

- `API_KEY` — Fireworks API key
- `MODEL` — full model route

`MODEL` is not a plain model name. Gemma-3-27B is not serverless on Fireworks, so the study
model requires a live on-demand deployment and the route takes the form
`accounts/<account>/models/carebot-gemma3-27b-v2#accounts/<account>/deployments/<id>`.
That deployment id changes every time a deployment is brought up, and a stale id here is what
caused the previous dead-model failure. Update the secret whenever the deployment is recreated.

For any testing that is not the study itself, point `MODEL` at a cheap serverless model. The
code path is identical.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp secrets.toml.example .streamlit/secrets.toml   # then fill it in
streamlit run carebot_app.py
```

Run from this directory. `config.toml` uses relative static paths for the theme fonts and the
theme breaks if the app is launched from a parent directory.

The app reads the participant profile from URL query parameters, so test with them attached:

```
http://localhost:8501/?name=Test&age=22&gender=female&prefers_quick_response=Yes
```

Without parameters every field reads `N/A` and the greeting says "Hi N/A".

## Retrieval is deliberately absent

Earlier versions had retrieval-augmented generation wired in. It was removed after evaluation,
not by accident. Blinded human review preferred the no-retrieval model on 85% of the queries
where gated retrieval fired, and debiased LLM-judge pairwise comparisons agreed at roughly
60/40. The likely cause is corpus quality rather than retrieval mechanics: a knowledge base
dominated by general career guidance rarely holds anything a specific caregiver's message
needs, and injecting it dilutes the fine-tuned voice.

Do not re-add retrieval without re-running the evaluation. The build code and the full result
set are on the `legacy` branch under `rag/` and `results/`.

## Model

`carebot-gemma3-27b-v2`, a LoRA fine-tune of Gemma-3-27B-IT (rank 8, 1 epoch, lr 1e-5) on
9,500 synthetic caregiver conversations. Weights are on Fireworks, not in this repository.

## Still to add

- Conversation logging to an external store, keyed by participant id. The Community Cloud
  filesystem is ephemeral, so anything written locally is lost on restart.
- A replacement for passing the profile in the URL. The current mechanism puts the care
  recipient's health condition in the query string, where it reaches browser history and
  server logs.
- The Qualtrics iframe embed snippet, once the survey is ready.
