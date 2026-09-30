# DocIntel AI Deployment Guide

This guide walks you through deploying **DocIntel AI** using the production-recommended split deployment:
- **Backend (FastAPI + Groq + ChromaDB + PyMuPDF)**: Deployed on **Render** (or **Railway**)
- **Frontend (React + Vite)**: Deployed on **Vercel**

---

## Prerequisites
1. **GitHub Account**: Your code pushed to a GitHub repository.
2. **Groq Cloud API Key**: Free API key from [Groq Console](https://console.groq.com/keys).
3. **Render Account**: Free account at [render.com](https://render.com) (or [railway.com](https://railway.com)).
4. **Vercel Account**: Free account at [vercel.com](https://vercel.com).

---

## Step 1: Commit and Push Your Code to GitHub

Open your terminal in the project root and commit the updated configuration:

```bash
git add .
git commit -m "feat: configure project for Vercel and Render deployment"
git push origin main
```

---

## Step 2: Deploy Backend to Render

### Method A: Web UI (Standard & Recommended)

1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository (`docintel-ai`).
4. Configure the service:
   - **Name**: `docintel-backend` (or your choice)
   - **Region**: Choose the closest region (e.g., Oregon, Frankfurt, Singapore)
   - **Root Directory**: `backend`
   - **Runtime**: **Docker** *(Recommended because it automatically bundles `tesseract-ocr` and required C libraries)*
     - *Alternative*: If using **Python 3**, set:
       - **Build Command**: `pip install -r requirements.txt`
       - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **Free**
5. Add Environment Variables:
   - Click **Add Environment Variable**:
     - Key: `GROQ_API_KEY`
     - Value: `gsk_your_actual_groq_api_key`
6. Click **Create Web Service**.
7. Wait 2–4 minutes for the build to finish. Once deployed, copy your backend URL:
   `https://docintel-backend-xxxx.onrender.com`

> **Note on Render Free Tier**: Free instances spin down after 15 minutes of inactivity and take ~30–50 seconds to wake up on the first request.

---

### Alternative Backend Option: Railway
1. Go to [railway.app](https://railway.app) and create a **New Project**.
2. Select **Deploy from GitHub repo** and choose your repo.
3. In service **Settings** > **Source**, set **Root Directory** to `/backend`.
4. In **Variables**, add:
   - `GROQ_API_KEY`: `gsk_...`
5. Railway will automatically detect the `Dockerfile` or `Procfile` and deploy your API.
6. Generate a domain under **Networking** (e.g., `https://docintel-backend.up.railway.app`).

---

## Step 3: Deploy Frontend to Vercel

1. Log in to [vercel.com](https://vercel.com) and click **Add New...** > **Project**.
2. Import your GitHub repository.
3. Under **Configure Project**:
   - **Project Name**: `docintel-frontend`
   - **Framework Preset**: `Vite` (automatically detected)
   - **Root Directory**: Click **Edit** and select `frontend`.
4. Expand **Environment Variables**:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-url.onrender.com` *(Paste your Render/Railway backend URL from Step 2, without a trailing slash)*
5. Click **Deploy**.
6. Vercel will build and deploy your React app in ~30 seconds, giving you a live production URL:
   `https://docintel-frontend.vercel.app`

---

## Step 4: Verify Deployment

1. **Test Backend**:
   Visit `https://your-backend-url.onrender.com/` in your browser. You should see:
   ```json
   {"status": "DocIntel API is running"}
   ```
   Or visit `https://your-backend-url.onrender.com/docs` to see the interactive Swagger API documentation.

2. **Test Frontend**:
   Open your Vercel URL, upload a PDF document, and click **Analyze Document**.
   The frontend will communicate with your live backend, process the PDF with Groq and ChromaDB, and display the interactive radar charts and download button.

---

## 🛠️ Summary of Files Configured

| File | Purpose |
|---|---|
| `frontend/src/api.js` | Dynamic API URL via `VITE_API_URL` with fallback to `http://localhost:8000` |
| `frontend/vercel.json` | Single Page Application (SPA) routing rules for Vercel |
| `frontend/.env.example` | Template for local and production environment variables |
| `backend/Dockerfile` | Production container bundling Python 3.11, Tesseract OCR, PyMuPDF, and ChromaDB |
| `backend/Procfile` | Startup command for native PaaS platforms (`uvicorn app:app --port $PORT`) |
| `backend/app.py` | Production directory safety (`uploads/` & `outputs/`) and `$PORT` binding |
| `backend/.env.example` | Template for `GROQ_API_KEY` configuration |
| `render.yaml` | Blueprint for automated one-click Render deployment |
| `.gitignore` | Prevents secrets (`.env`) and heavy artifacts from being pushed to git |
