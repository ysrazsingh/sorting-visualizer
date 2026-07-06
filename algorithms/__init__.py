from .bubble_sort    import bubble_sort
from .selection_sort import selection_sort
from .insertion_sort import insertion_sort
from .merge_sort     import merge_sort
from .quick_sort     import quick_sort
from .heap_sort      import heap_sort
from .shell_sort     import shell_sort
from .tree_sort      import tree_sort
from .tim_sort       import tim_sort
from .intro_sort     import intro_sort

# key  →  (display name, generator function)
ALGO_MAP = {
    "bubble":    ("Bubble Sort",    bubble_sort),
    "selection": ("Selection Sort", selection_sort),
    "insertion": ("Insertion Sort", insertion_sort),
    "merge":     ("Merge Sort",     merge_sort),
    "quick":     ("Quick Sort",     quick_sort),
    "heap":      ("Heap Sort",      heap_sort),
    "shell":     ("Shell Sort",     shell_sort),
    "tree":      ("Tree Sort",      tree_sort),
    "tim":       ("TimSort",        tim_sort),
    "intro":     ("IntroSort",      intro_sort),
}

ALL_ALGORITHMS = list(ALGO_MAP.values())
