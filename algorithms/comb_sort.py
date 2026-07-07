def comb_sort(arr):
    n        = len(arr)
    gap      = n
    shrink   = 1.3
    is_sorted = False

    while not is_sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            is_sorted = True

        i = 0
        while i + gap < n:
            yield {"type": "compare", "idx": (i, i + gap)}
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                yield {"type": "swap", "idx": (i, i + gap)}
                is_sorted = False
            i += 1

    yield {"type": "done"}
