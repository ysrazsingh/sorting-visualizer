def bucket_sort(arr):
    n = len(arr)
    if n <= 1:
        yield {"type": "done"}
        return

    min_val = min(arr)
    max_val = max(arr)
    span    = max(max_val - min_val, 1)

    num_buckets = max(1, n // 5)
    buckets     = [[] for _ in range(num_buckets)]

    for i, v in enumerate(arr):
        bi = min(int((v - min_val) / span * num_buckets), num_buckets - 1)
        buckets[bi].append(v)
        yield {"type": "compare", "idx": (i, i)}

    k = 0
    for bucket in buckets:
        # insertion sort within bucket
        for i in range(1, len(bucket)):
            key = bucket[i]
            j   = i - 1
            while j >= 0 and bucket[j] > key:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = key

        for v in bucket:
            arr[k] = v
            yield {"type": "overwrite", "idx": k, "val": v}
            k += 1

    yield {"type": "done"}
