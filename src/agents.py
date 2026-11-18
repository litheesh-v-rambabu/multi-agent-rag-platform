"""LangGraph-style multi-agent orchestration in plain Python (no paid LLM keys).
Router -> Triage agent -> Retrieval agent -> Extraction agent."""
import re
from src.rerank import rerank

class TriageAgent:
    RULES = {"billing": ["bill","charge","refund","invoice","payment"],
             "account": ["password","login","account","access"],
             "technical": ["error","crash","slow","bug","not working"]}
    def run(self, query):
        q=query.lower()
        for label, words in self.RULES.items():
            if any(w in q for w in words): return {"category": label, "priority": "high" if "urgent" in q or "crash" in q else "normal"}
        return {"category": "general", "priority": "normal"}

class RetrievalAgent:
    def __init__(self, index): self.index=index
    def run(self, query, k=5): return rerank(query, self.index.search(query, k=k))

class ExtractionAgent:
    def run(self, query):
        emails=re.findall(r"[\w.]+@[\w.]+", query)
        return {"emails": emails, "word_count": len(query.split())}

class SupportRouter:
    def __init__(self, index):
        self.triage=TriageAgent(); self.retrieval=RetrievalAgent(index); self.extraction=ExtractionAgent()
    def handle(self, query):
        triage=self.triage.run(query); results=self.retrieval.run(query)
        answer=""
        if results:
            doc=results[0][0]; answer=doc["text"][:600]  # extractive answer from retrieved doc
        return {"triage": triage, "results": results, "extraction": self.extraction.run(query), "answer": answer, "source": results[0][0]["title"] if results else None}
