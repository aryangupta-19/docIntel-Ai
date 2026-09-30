# DocIntel AI

> AI-powered document intelligence platform for extracting, searching, analyzing, and understanding PDF documents using semantic retrieval, RAG, and specialized AI analysis.

---

## Overview

DocIntel AI is a full-stack document intelligence system that allows users to upload PDF documents and obtain AI-powered insights from their content.

Instead of sending an entire document to an LLM, DocIntel processes the document through a retrieval-augmented generation (RAG) pipeline:

```
PDF Upload
    ↓
PDF Text Extraction
    ↓
OCR Fallback for Scanned PDFs
    ↓
Document Chunking
    ↓
Embeddings Generation
    ↓
ChromaDB Vector Storage
    ↓
Semantic Retrieval
    ↓
Specialized AI Agents
    ↓
Groq LLM
    ↓
Response Composition
    ↓
Final Document Analysis
```

---

## Key Features

- **Multi-Agent Analysis Engine**: Runs a panel of specialized LLM agents focusing on executive summary, key insights, risk indicators, citations, and compliance verification.
- **Automated Visual PDF Annotation**: Highlights passages directly on the original PDF using PyMuPDF (`fitz`), complete with a color-coded legend and high-risk border indicators.
- **Hybrid Document Ingestion**: Fast extraction via PyPDFLoader with an automatic OCR fallback using Tesseract for scanned or image-based PDFs.
- **Semantic Retrieval**: Chunks documents and generates embeddings using `all-MiniLM-L6-v2` stored in ChromaDB for grounded, hallucination-free retrieval.
- **Interactive Web Dashboard**: React 19 + Vite frontend featuring radar chart document evaluations, real-time agent progression, and one-click annotated PDF downloads.

---

## Specialized AI Agents

| Agent | Responsibility |
|---|---|
| **Executive Summary Agent** | Synthesizes the core purpose, key themes, critical findings, and overall document scope. |
| **Semantic Search & Q&A Agent** | Answers questions strictly using retrieved document context to prevent hallucinations. |
| **Citation Agent** | Extracts verifiable excerpts, supporting evidence, and available page/section references. |
| **Key Insights Agent** | Categorizes important findings, operational bottlenecks, risk factors, and recommendations. |
| **Document Compliance Agent** | Audits documents for missing mandatory clauses, dates, signatures, and approval requirements. |
| **Annotation Agent** | Pinpoints notable passages and categorizes them for visual document highlighting. |
| **Response Composer** | Synthesizes all specialist assessments into a coherent, structured intelligence report. |

---

## System Architecture

```
User Upload (PDF)
       │
       ▼
[ FastAPI Backend ]
       │
       ├──► [ Loader & Chunking ] ──► [ ChromaDB Vector Store ]
       │                                         │
       ├──► [ Multi-Agent Panel ] ◄──────────────┘
       │           │
       │           ├──► Executive Summary
       │           ├──► Key Insights & Risks
       │           ├──► Citations & Evidence
       │           ├──► Compliance & Validation
       │           └──► Annotation Finder
       │           │
       │           ▼
       │    [ Groq LLaMA 3.1 ] ──► [ Response Composer ]
       │                                  │
       ├──► [ PyMuPDF Annotator ] ◄───────┘
       │           │
       │           ▼
       └──► [ Annotated PDF with Visual Highlights ] ──► User Download
```

---

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, LangChain, Groq Cloud (LLaMA 3.1 8B Instant), ChromaDB, PyMuPDF, pytesseract
- **Frontend**: React 19, Vite, Recharts, Axios
- **Deployment**: Vercel (Frontend), Docker / Cloud PaaS (Backend)

---

## Project Structure

```
docintel-ai/
├── backend/
│   ├── app.py                      # FastAPI API endpoints & pipeline execution
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Container build with Tesseract & Python 3.11
│   ├── Procfile                    # Web process command for PaaS platforms
│   ├── .dockerignore               # Docker build exclusions
│   ├── .env.example                # Backend environment template
│   └── src/
│       ├── orchestrator.py         # Pipeline coordinator
│       ├── agents.py               # Specialist agent panel & composer
│       ├── llm_engine.py           # Groq API client integration
│       ├── vectorstore.py          # ChromaDB vector collection
│       ├── loader.py               # PDF loader with Tesseract OCR fallback
│       ├── document_annotator.py   # PyMuPDF visual highlighter & legend
│       └── document_validator.py   # Document completeness heuristics
├── frontend/
│   ├── src/
│   │   ├── api.js                  # Centralized API configuration (VITE_API_URL)
│   │   ├── App.jsx                 # Application state & screen routing
│   │   ├── pages/
│   │   │   ├── HomePage.jsx        # Landing page
│   │   │   ├── UploadPage.jsx      # Upload panel with real-time progress
│   │   │   └── AnalysisPage.jsx    # Radar chart & multi-agent breakdown
│   │   └── components/
│   ├── package.json                # React 19, Vite, Recharts, Axios
│   ├── vercel.json                 # SPA routing rewrites for Vercel
│   └── .env.example                # Frontend environment template
├── LICENSE                         # MIT License
└── README.md
```

---

## Quickstart

### 1. Clone & Set Environment
```bash
git clone https://github.com/aryangupta-19/docIntel-Ai.git
cd docIntel-Ai
```

Create `backend/.env` with your free [Groq Cloud API Key](https://console.groq.com/keys):
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
PORT=8000
```

### 2. Start Backend (Terminal 1)
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
> API runs at `http://localhost:8000` (Swagger docs at `/docs`)

### 3. Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
> Application UI runs at `http://localhost:5173`

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check endpoint returning API status |
| `POST` | `/analyze` | Upload a PDF and receive structured multi-agent JSON analysis |
| `POST` | `/analyze-and-annotate` | Run multi-agent pipeline and generate a highlighted PDF |
| `GET` | `/download/{filename}` | Download the annotated PDF file |
| `GET` | `/docs` | Interactive Swagger UI API documentation |

---

## License

This project is licensed under the [MIT License](LICENSE).
