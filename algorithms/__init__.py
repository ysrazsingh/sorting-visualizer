from .bogo_sort             import bogo_sort
from .bubble_sort           import bubble_sort
from .bucket_sort           import bucket_sort
from .cocktail_shaker_sort  import cocktail_shaker_sort
from .comb_sort             import comb_sort
from .counting_sort         import counting_sort
from .heap_sort             import heap_sort
from .insertion_sort        import insertion_sort
from .intro_sort            import intro_sort
from .merge_sort            import merge_sort
from .quick_sort            import quick_sort
from .radix_sort            import radix_sort
from .selection_sort        import selection_sort
from .shell_sort            import shell_sort
from .tim_sort              import tim_sort

# key  →  (display name, generator function)
ALGO_MAP = {
    "bogo":      ("Bogo Sort",           bogo_sort),
    "bubble":    ("Bubble Sort",         bubble_sort),
    "bucket":    ("Bucket Sort",         bucket_sort),
    "cocktail":  ("Cocktail Sort",       cocktail_shaker_sort),
    "comb":      ("Comb Sort",           comb_sort),
    "counting":  ("Counting Sort",       counting_sort),
    "heap":      ("Heap Sort",           heap_sort),
    "insertion": ("Insertion Sort",      insertion_sort),
    "intro":     ("Intro Sort",          intro_sort),
    "merge":     ("Merge Sort",          merge_sort),
    "quick":     ("Quick Sort",          quick_sort),
    "radix":     ("Radix Sort (LSD)",    radix_sort),
    "selection": ("Selection Sort",      selection_sort),
    "shell":     ("Shell Sort",          shell_sort),
    "tim":       ("Tim Sort",            tim_sort),
}

ALL_ALGORITHMS = list(ALGO_MAP.values())
