import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.primitives import _ins_sort, _merge


def tim_sort(arr):
    RUN, n = 32, len(arr)

    # sort each run with insertion sort
    for i in range(0, n, RUN):
        yield from _ins_sort(arr, i, min(i + RUN - 1, n - 1))

    # merge runs bottom-up
    size = RUN
    while size < n:
        for lo in range(0, n, 2 * size):
            mid = min(lo + size - 1,     n - 1)
            hi  = min(lo + 2 * size - 1, n - 1)
            if mid < hi:
                yield from _merge(arr, lo, mid, hi)
        size *= 2

    yield {"type": "done"}


if __name__ == "__main__":
    from core.engine import run_visualizer
    run_visualizer([("TimSort", tim_sort)])
