"""TF-IDF cosine retrieval — light fallback for FAISS + sentence embeddings.
Same interface (index documents, search query -> ranked docs) with no downloads."""
import re, math
from collections import Counter

def _tokens(t): return re.findall(r"[a-z0-9]+", t.lower())
class TfidfIndex:
    def __init__(self, docs):
        self.docs = docs  # list of dicts: id, title, text
        self.vocab = {}
        df = Counter()
        self.doc_tokens = []
        for d in docs:
            toks = _tokens(d["title"]+" "+d["text"]); self.doc_tokens.append(Counter(toks)); df.update(set(toks))
        for w in sorted({w for c in self.doc_tokens for w in c}): self.vocab[w]=len(self.vocab)
        n=len(docs); self.idf={w: math.log((1+n)/(1+df[w]))+1 for w in self.vocab}
        self.vectors=[self._vec(c) for c in self.doc_tokens]
    def _vec(self, counter):
        v=[0.0]*len(self.vocab)
        for w,c in counter.items():
            if w in self.vocab: v[self.vocab[w]]=c*self.idf[w]
        norm=math.sqrt(sum(x*x for x in v)) or 1.0
        return [x/norm for x in v]
    def search(self, query, k=5):
        qv=self._vec(Counter(_tokens(query)))
        scored=[]
        for i,v in enumerate(self.vectors):
            s=sum(a*b for a,b in zip(qv,v)); scored.append((s,i))
        scored.sort(reverse=True)
        return [(self.docs[i], float(s)) for s,i in scored[:k] if s>0]
