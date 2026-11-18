import pathlib
def load_corpus(base=None):
    base = pathlib.Path(base) if base else pathlib.Path(__file__).resolve().parents[1]/"corpus"
    docs=[]
    for p in sorted(base.glob("*.md")):
        text=p.read_text(encoding="utf-8")
        title=text.splitlines()[0].lstrip("# ").strip() if text else p.stem
        docs.append({"id": p.stem, "title": title, "text": text})
    return docs
