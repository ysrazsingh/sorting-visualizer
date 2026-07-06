import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.primitives import _ins_sort, _heap_sort_range, _partition


def intro_sort(arr):
    n         = len(arr)
    max_depth = 2 * math.floor(math.log2(max(n, 2)))

    def introsort(lo, hi, depth):
        size = hi - lo + 1
        if size <= 1:
            return
        elif size <= 16:
            yield from _ins_sort(arr, lo, hi)
        elif depth == 0:
            yield from _heap_sort_range(arr, lo, hi)
        else:
            out = [0]
            yield from _partition(arr, lo, hi, out, median_of_three=True)
            pi = out[0]
            yield from introsort(lo, pi - 1, depth - 1)
            yield from introsort(pi + 1, hi, depth - 1)

    yield from introsort(0, n - 1, max_depth)
    yield {"type": "done"}


if __name__ == "__main__":
    from core.engine import run_visualizer
    run_visualizer([("IntroSort", intro_sort)])
