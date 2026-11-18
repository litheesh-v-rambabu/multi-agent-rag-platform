"""Precision@k evaluation — demonstrates the concept used in the original project."""
def precision_at_k(retrieved_ids, relevant_ids, k):
    if k==0: return 0.0
    top=retrieved_ids[:k]
    return sum(1 for i in top if i in set(relevant_ids))/k
def mean_precision_at_k(cases, k=5):
    if not cases: return 0.0
    return sum(precision_at_k(r, rel, k) for r,rel in cases)/len(cases)
