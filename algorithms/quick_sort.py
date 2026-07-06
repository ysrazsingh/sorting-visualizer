import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.primitives import _partition


def quick_sort(arr):
    def sort(lo, hi):
        if lo < hi:
            out = [0]
            yield from _partition(arr, lo, hi, out)
            pi = out[0]
            yield from sort(lo, pi - 1)
            yield from sort(pi + 1, hi)

    yield from sort(0, len(arr) - 1)
    yield {"type": "done"}


if __name__ == "__main__":
    from core.engine import run_visualizer
    run_visualizer([("Quick Sort", quick_sort)])
