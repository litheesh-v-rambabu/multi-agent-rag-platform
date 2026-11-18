import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.eval import precision_at_k, mean_precision_at_k
def test_precision_at_k():
    assert precision_at_k(["a","b","c"], {"a","c"}, 3) == 2/3
    assert precision_at_k([], {"a"}, 5) == 0.0
def test_mean_precision():
    assert mean_precision_at_k([(["a"],{"a"})], k=1) == 1.0
