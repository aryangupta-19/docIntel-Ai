# DocIntel AI

> AI-powered document intelligence platform for extracting, searching, analyzing, and understanding PDF documents using semantic retrieval, RAG, and specialized AI analysis.

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
