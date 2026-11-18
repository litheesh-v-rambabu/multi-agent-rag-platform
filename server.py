"""Optional FastAPI service — same retrieval layer as the Streamlit demo."""
from fastapi import FastAPI
from pydantic import BaseModel
from src.corpus_loader import load_corpus
from src.retrieval import TfidfIndex
from src.agents import SupportRouter
app = FastAPI(title="Multi-Agent RAG Platform (demo)")
router = SupportRouter(TfidfIndex(load_corpus()))
class Query(BaseModel): query: str
@app.get("/health")
def health(): return {"status": "ok", "demo": True}
@app.post("/ask")
def ask(q: Query):
    out = router.handle(q.query)
    out["results"] = [(d["title"], s) for d,s in out["results"]]
    return out
