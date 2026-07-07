def counting_sort(arr):
    if not arr:
        yield {"type": "done"}
        return

    min_val = min(arr)
    max_val = max(arr)
    count   = [0] * (max_val - min_val + 1)

    for i, v in enumerate(arr):
        count[v - min_val] += 1
        yield {"type": "compare", "idx": (i, i)}

    k = 0
    for i, c in enumerate(count):
        for _ in range(c):
            arr[k] = i + min_val
            yield {"type": "overwrite", "idx": k, "val": arr[k]}
            k += 1

    yield {"type": "done"}
