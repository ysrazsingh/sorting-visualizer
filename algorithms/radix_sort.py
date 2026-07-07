def radix_sort(arr):
    if not arr:
        yield {"type": "done"}
        return

    max_val = max(arr)
    exp     = 1

    while max_val // exp > 0:
        n      = len(arr)
        output = [0] * n
        count  = [0] * 10

        for i in range(n):
            digit = (arr[i] // exp) % 10
            count[digit] += 1
            yield {"type": "compare", "idx": (i, i)}

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            digit             = (arr[i] // exp) % 10
            output[count[digit] - 1] = arr[i]
            count[digit]     -= 1

        for i in range(n):
            arr[i] = output[i]
            yield {"type": "overwrite", "idx": i, "val": arr[i]}

        exp *= 10
        if max_val // exp == 0:
            break

    yield {"type": "done"}
