"""Simple re-ranker: boost documents whose title overlaps the query (cross-signal)."""
def rerank(query, results):
    q=set(query.lower().split())
    def key(item):
        doc, score = item
        boost = 0.05 * len(q & set(doc["title"].lower().split()))
        return score + boost
    return sorted(results, key=key, reverse=True)
