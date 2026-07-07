import random as _random


def bogo_sort(arr):
    def _sorted(a):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                return False
        return True

    while not _sorted(arr):
        for i in range(len(arr) - 1):
            yield {"type": "compare", "idx": (i, i + 1)}
        for i in range(len(arr) - 1, 0, -1):
            j = _random.randint(0, i)
            if j != i:
                arr[i], arr[j] = arr[j], arr[i]
                yield {"type": "swap", "idx": (i, j)}

    yield {"type": "done"}
