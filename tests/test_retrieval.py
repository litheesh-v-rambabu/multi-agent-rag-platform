import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.corpus_loader import load_corpus
from src.retrieval import TfidfIndex
from src.agents import SupportRouter
def test_corpus_size():
    assert len(load_corpus()) >= 25
def test_retrieval_finds_password():
    idx=TfidfIndex(load_corpus()); results=idx.search("reset my password", k=3)
    assert results and "password" in results[0][0]["title"].lower()
def test_router_answer():
    out=SupportRouter(TfidfIndex(load_corpus())).handle("I need a refund for a duplicate charge")
    assert out["triage"]["category"]=="billing" and out["answer"]
