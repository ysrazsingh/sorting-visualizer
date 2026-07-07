def cocktail_shaker_sort(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        new_hi = lo
        for j in range(lo, hi):
            yield {"type": "compare", "idx": (j, j + 1)}
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield {"type": "swap", "idx": (j, j + 1)}
                new_hi = j
        hi = new_hi

        new_lo = hi
        for j in range(hi, lo, -1):
            yield {"type": "compare", "idx": (j - 1, j)}
            if arr[j - 1] > arr[j]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                yield {"type": "swap", "idx": (j - 1, j)}
                new_lo = j
        lo = new_lo

    yield {"type": "done"}
