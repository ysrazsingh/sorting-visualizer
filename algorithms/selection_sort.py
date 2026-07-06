def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            yield {"type": "compare", "idx": (m, j)}
            if arr[j] < arr[m]:
                m = j
        if m != i:
            arr[i], arr[m] = arr[m], arr[i]
            yield {"type": "swap", "idx": (i, m)}
    yield {"type": "done"}


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.engine import run_visualizer
    run_visualizer([("Selection Sort", selection_sort)])
