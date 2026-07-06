"""
Shared generator building-blocks used by multiple sorting algorithms.

Each function mutates `arr` in-place and yields event dicts:
  {"type": "compare",   "idx": (i, j)}
  {"type": "swap",      "idx": (i, j)}
  {"type": "overwrite", "idx": i, "val": v}
"""


def _ins_sort(arr, lo: int, hi: int):
    """Insertion sort over arr[lo..hi] inclusive."""
    for i in range(lo + 1, hi + 1):
        key = arr[i]
        j   = i - 1
        while j >= lo:
            yield {"type": "compare", "idx": (j, j + 1)}
            if arr[j] > key:
                arr[j + 1] = arr[j]
                yield {"type": "overwrite", "idx": j + 1, "val": arr[j + 1]}
                j -= 1
            else:
                break
        arr[j + 1] = key
        yield {"type": "overwrite", "idx": j + 1, "val": key}


def _merge(arr, lo: int, mid: int, hi: int):
    """Merge arr[lo..mid] with arr[mid+1..hi] in-place."""
    L, R = arr[lo:mid + 1], arr[mid + 1:hi + 1]
    i = j = 0
    k = lo
    while i < len(L) and j < len(R):
        yield {"type": "compare", "idx": (lo + i, mid + 1 + j)}
        if L[i] <= R[j]:
            arr[k] = L[i]; i += 1
        else:
            arr[k] = R[j]; j += 1
        yield {"type": "overwrite", "idx": k, "val": arr[k]}
        k += 1
    for v in L[i:]:
        arr[k] = v; yield {"type": "overwrite", "idx": k, "val": v}; k += 1
    for v in R[j:]:
        arr[k] = v; yield {"type": "overwrite", "idx": k, "val": v}; k += 1


def _heapify(arr, size: int, i: int, offset: int = 0):
    """Iterative max-heapify arr[offset .. offset+size-1] rooted at index i."""
    while True:
        lg, l, r = i, 2 * i + 1, 2 * i + 2
        if l < size:
            yield {"type": "compare", "idx": (offset + lg, offset + l)}
            if arr[offset + l] > arr[offset + lg]:
                lg = l
        if r < size:
            yield {"type": "compare", "idx": (offset + lg, offset + r)}
            if arr[offset + r] > arr[offset + lg]:
                lg = r
        if lg != i:
            arr[offset + i], arr[offset + lg] = arr[offset + lg], arr[offset + i]
            yield {"type": "swap", "idx": (offset + i, offset + lg)}
            i = lg
        else:
            break


def _heap_sort_range(arr, lo: int, hi: int):
    """Heap sort arr[lo..hi] in-place (reuses _heapify)."""
    size = hi - lo + 1
    for i in range(size // 2 - 1, -1, -1):
        yield from _heapify(arr, size, i, lo)
    for i in range(size - 1, 0, -1):
        arr[lo], arr[lo + i] = arr[lo + i], arr[lo]
        yield {"type": "swap", "idx": (lo, lo + i)}
        yield from _heapify(arr, i, 0, lo)


def _partition(arr, lo: int, hi: int, out: list, median_of_three: bool = False):
    """
    Lomuto partition scheme.  Writes the pivot's final index into out[0].
    With median_of_three=True uses median-of-three pivot selection.
    """
    if median_of_three:
        mid = (lo + hi) // 2
        for a, b in ((lo, mid), (lo, hi), (mid, hi)):
            yield {"type": "compare", "idx": (a, b)}
            if arr[a] > arr[b]:
                arr[a], arr[b] = arr[b], arr[a]
                yield {"type": "swap", "idx": (a, b)}
        arr[mid], arr[hi] = arr[hi], arr[mid]
        yield {"type": "swap", "idx": (mid, hi)}

    pivot = arr[hi]
    i     = lo - 1
    for j in range(lo, hi):
        yield {"type": "compare", "idx": (j, hi)}
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield {"type": "swap", "idx": (i, j)}
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    yield {"type": "swap", "idx": (i + 1, hi)}
    out[0] = i + 1
