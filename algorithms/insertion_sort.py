import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.primitives import _ins_sort


def insertion_sort(arr):
    yield from _ins_sort(arr, 0, len(arr) - 1)
    yield {"type": "done"}


if __name__ == "__main__":
    from core.engine import run_visualizer
    run_visualizer([("Insertion Sort", insertion_sort)])
