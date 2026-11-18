"""Multi-Agent RAG Platform — Streamlit demo (HF Spaces, standalone).
Sample corpus only (~30 synthetic support articles). Answers are extractive —
no paid LLM key is used. Reported original results are in the README."""
import streamlit as st
from src.corpus_loader import load_corpus
from src.retrieval import TfidfIndex
from src.agents import SupportRouter

st.set_page_config(page_title="Multi-Agent RAG Platform", layout="wide")
st.title("🤖 Multi-Agent RAG Platform for Support Operations")
st.caption("DEMO — sample support corpus, extractive answers, no LLM API key. Original reported: 30K+ req/mo, precision@k 68%→87%, P95 <1,800ms.")
@st.cache_resource
def load_router(): return SupportRouter(TfidfIndex(load_corpus()))
router = load_router()
st.write("**How it works:** Triage agent classifies the request → Retrieval agent searches + re-ranks the knowledge base → Extraction agent pulls structured fields → answer is extracted from the top article.")
query = st.text_input("Ask a support question", "How do I reset my password?")
if query:
    out = router.handle(query)
    st.json({"triage": out["triage"], "source": out["source"]})
    st.subheader("Answer (extractive, from retrieved article)")
    st.write(out["answer"] or "No matching article found in the sample corpus.")
    st.subheader("Retrieved articles")
    for doc, score in out["results"]: st.write(f"- **{doc['title']}** — score {score:.3f}")
