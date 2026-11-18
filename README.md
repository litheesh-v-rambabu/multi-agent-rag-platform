---
title: Multi-Agent RAG Platform
emoji: "🤖"
colorFrom: green
colorTo: blue
sdk: streamlit
sdk_version: "1.37.1"
app_file: app.py
pinned: false
license: mit
---

# Multi-Agent Retrieval-Augmented Generation (RAG) Platform for Support Operations

**Live demo:** https://huggingface.co/spaces/LithiVR/multi-agent-rag-platform (Gradio demo on Hugging Face Spaces, same project logic; Streamlit version in `app.py`)

> **Demo notice:** This is a scaled-down public reproduction with a **sample support
> corpus (~30 synthetic articles in `corpus/`)**. Answers are **extractive** from the
> retrieved articles — no paid LLM API key is required or used.

## Why
Support teams triage the same questions repeatedly and keyword search misses answers
phrased differently, which drives hallucinations when an LLM answers without good
retrieval. This platform unifies RAG, data extraction, and automated triage.

## How (architecture from the original project)
- Horizontally scalable microservices (Python, FastAPI, Docker) in the original;
  here `server.py` is the FastAPI service and `app.py` runs the same retrieval
  layer in-process so it works standalone on HF Spaces.
- **LangGraph-style orchestration, implemented in plain Python** (`src/agents.py`):
  a router coordinates a **Triage agent** (classify intent/priority), a **Retrieval
  agent** (search + re-rank), and an **Extraction agent** (pull structured fields).
  This mirrors the agent graph without requiring paid LLM keys.
- **Retrieval (`src/retrieval.py`, `src/rerank.py`):** embeddings + vector search +
  re-ranking in the original (Chroma/FAISS, QLoRA classifier via Hugging Face).
  Demo fallback: TF-IDF cosine index (FAISS-compatible interface) + overlap re-ranker,
  so it runs free and offline.
- **Evaluation (`src/eval.py`):** precision@k script demonstrating the evaluation
  concept on the sample corpus.
- Original also shipped an MCP server + REST API, CI/CD (pytest, GitHub Actions,
  LLM-as-judge), circuit breakers and exponential-backoff retries.

## Reported results (original project, from resume)
- Serving **30K+ requests/month** at **40% higher throughput**
- **Precision@k 68% → 87%**; hallucination rate **−48%**; inference cost **−93%** vs LLM calls
- **99.2% uptime**, **P95 latency < 1,800 ms**

These are the original project's reported results; the demo is a scaled-down
reproduction and its sample-corpus numbers are labelled as demo data.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py          # standalone demo
uvicorn server:app --reload   # optional FastAPI service
pytest -q
```
