def shell_sort(arr):
    n, gap = len(arr), len(arr) // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j    = i
            while j >= gap:
                yield {"type": "compare", "idx": (j - gap, j)}
                if arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    yield {"type": "overwrite", "idx": j, "val": arr[j]}
                    j -= gap
                else:
                    break
            arr[j] = temp
            yield {"type": "overwrite", "idx": j, "val": temp}
        gap //= 2
    yield {"type": "done"}


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.engine import run_visualizer
    run_visualizer([("Shell Sort", shell_sort)])
