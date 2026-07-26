# 🚀 Deployment Guide — Free Tier

This guide deploys your Enterprise Agentic RAG chatbot using **100% free** platforms:

| Component | Platform | URL Format |
|-----------|----------|------------|
| FastAPI Backend | HuggingFace Spaces | `https://<your-username>-<space-name>.hf.space` |
| Streamlit Frontend | Streamlit Community Cloud | `https://<app-name>.streamlit.app` |

---

## Step 1: Push Code to GitHub

Make sure your latest code is pushed:

```bash
git add .
git commit -m "Add deployment files"
git push origin main
```

> ⚠️ Verify `.env` is in `.gitignore` — your secrets must NOT be pushed to GitHub.

---

## Step 2: Deploy Backend on HuggingFace Spaces

### 2.1 Create the Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in:
   - **Space name**: `enterprise-rag-api` (or anything you like)
   - **SDK**: Select **Docker**
   - **Visibility**: Public (free tier requires public)
3. Click **Create Space**

### 2.2 Connect to GitHub (Automatic Sync)

1. In your new Space, go to **Settings** → **Repository**
2. Under **Factory reboot** or **Files**, you can either:
   - **Option A (Recommended)**: Link your GitHub repo for auto-sync
   - **Option B**: Push directly to the HF Space repo

**Option B — Push directly:**
```bash
# Add HuggingFace as a remote
git remote add hf https://huggingface.co/spaces/<YOUR_USERNAME>/enterprise-rag-api

# Push to HuggingFace
git push hf main
```

### 2.3 Set Environment Secrets

1. Go to your Space → **Settings** → **Variables and secrets**
2. Add each secret (click "New secret" for each):

| Secret Name | Value |
|------------|-------|
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_FALLBACK_API_KEY` | Your fallback Groq key |
| `QDRANT_API_KEY` | Your Qdrant API key |
| `QDRANT_CLUSTER_END_POINT` | Your Qdrant cluster URL |
| `GEMINI_API_KEY` | Your Gemini API key |
| `PORTKEY_API_KEY` | Your Portkey API key |
| `PORTKEY_CONFIG_SLUG` | Your Portkey config slug |
| `LOGFIRE_TOKEN` | Your Logfire token |
| `LANGSMITH_TRACING` | `true` |
| `LANGSMITH_API_KEY` | Your LangSmith API key |
| `LANGSMITH_PROJECT` | Your LangSmith project name |
| `LANGSMITH_ENDPOINT` | `https://api.smith.langchain.com` |

### 2.4 Wait for Build

HuggingFace will build your Docker image and start the app. This takes **5-10 minutes** the first time.

Once running, your backend will be at:
```
https://<your-username>-enterprise-rag-api.hf.space
```

Test it by visiting:
```
https://<your-username>-enterprise-rag-api.hf.space/
```
You should see: `{"message": "AI Enterprise Langgraph is alive"}`

---

## Step 3: Deploy Frontend on Streamlit Community Cloud

### 3.1 Connect Your Repo

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub** account
3. Click **"New app"**
4. Select:
   - **Repository**: Your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `app/ui/app.py`
   - **Requirements file** (Advanced): `requirements-streamlit.txt`

### 3.2 Set Secrets

1. Click **"Advanced settings"** before deploying (or go to app Settings after)
2. In the **Secrets** box, paste in **TOML format**:

```toml
BACKEND_URL = "https://<your-username>-enterprise-rag-api.hf.space"
LOGFIRE_TOKEN = "your_logfire_token_here"
```

> 📌 Replace `<your-username>-enterprise-rag-api` with your actual HuggingFace Space URL.

### 3.3 Deploy

Click **"Deploy!"** — Streamlit Cloud will install the lightweight requirements and start your app.

Your frontend will be at:
```
https://<app-name>.streamlit.app
```

---

## Step 4: Verify Everything Works

1. Open your Streamlit app URL
2. Type a question in the chat
3. It should call your HF Spaces backend and return a RAG answer

---

## Troubleshooting

### Backend not responding
- Check HF Space logs: Space page → **Logs** tab
- Make sure all secrets are set correctly
- The Space may be sleeping — visit the URL to wake it up

### CORS errors
- The backend already runs on FastAPI which handles CORS
- If needed, add CORS middleware to `app/main.py`

### Cold starts (30-60 seconds)
- Normal for free tier — the app sleeps after ~48 hours of inactivity
- First request after sleep takes 30-60 seconds to wake up

---

## Architecture (Deployed)

```
User → streamlit.app (Frontend) → hf.space (Backend API)
                                       ↓
                              ┌────────┼────────┐
                              ↓        ↓        ↓
                           Groq     Qdrant   Portkey
                          (LLM)   (VectorDB) (Gateway)
```
