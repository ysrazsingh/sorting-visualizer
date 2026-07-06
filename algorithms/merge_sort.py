import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.primitives import _merge


def merge_sort(arr):
    def sort(lo, hi):
        if lo < hi:
            mid = (lo + hi) // 2
            yield from sort(lo, mid)
            yield from sort(mid + 1, hi)
            yield from _merge(arr, lo, mid, hi)

    yield from sort(0, len(arr) - 1)
    yield {"type": "done"}


if __name__ == "__main__":
    from core.engine import run_visualizer
    run_visualizer([("Merge Sort", merge_sort)])
