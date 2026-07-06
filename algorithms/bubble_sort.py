def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            yield {"type": "compare", "idx": (j, j + 1)}
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield {"type": "swap", "idx": (j, j + 1)}
    yield {"type": "done"}


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.engine import run_visualizer
    run_visualizer([("Bubble Sort", bubble_sort)])
