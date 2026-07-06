import pygame
import random
import numpy as np
import math

# ── Layout ───────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1000, 560
VIZ_H  = 470
MENU_H = HEIGHT - VIZ_H   # 90px (2 rows × 45px)

NUM_BARS = 80
MAX_VAL  = 280

# ── Palette ──────────────────────────────────────────────────────────────────
BG            = (10,  12,  16)
BAR_COLOR     = (239, 71,  111)
COMPARE_CLR   = (255, 209, 102)
SWAP_CLR      = (6,   214, 160)
OVERWRITE_CLR = (17,  138, 178)
DONE_CLR      = (100, 200, 120)
MENU_BG       = (16,  18,  24)
DIVIDER       = (38,  42,  54)
TEXT_DIM      = (110, 115, 135)
TEXT_BRIGHT   = (220, 225, 235)
ACTIVE_BG     = (45,  15,  25)
ACTIVE_BORDER = (239, 71,  111)

ALGORITHMS = [
    "Bubble Sort", "Selection Sort", "Insertion Sort",
    "Merge Sort",  "Quick Sort",     "Heap Sort",
    "Shell Sort",  "Tree Sort",      "TimSort",  "IntroSort",
]
KEY_MAP = {
    pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
    pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
    pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8,
    pygame.K_0: 9,
}
SPEED_LEVELS = [1, 2, 4, 8, 16, 32, 64]

# ── Sound ─────────────────────────────────────────────────────────────────────
_SOUND_CACHE: dict = {}

def make_tone(freq: int, duration: float = 0.015, volume: float = 0.35):
    freq = int(freq)
    if freq in _SOUND_CACHE:
        return _SOUND_CACHE[freq]
    sr = 44100
    t    = np.linspace(0, duration, int(sr * duration), endpoint=False)
    wave = 2 * np.abs(2 * (freq * t - np.floor(freq * t + 0.5))) - 1
    fade = int(sr * 0.002)
    env  = np.ones_like(wave)
    env[:fade]  = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    audio = ((wave * env) * volume * 32767).astype(np.int16)
    audio = np.column_stack((audio, audio))
    _SOUND_CACHE[freq] = pygame.sndarray.make_sound(audio)
    return _SOUND_CACHE[freq]

def beep(value: float):
    make_tone(int(1000 + (max(0, min(value, MAX_VAL)) / MAX_VAL) * 700)).play()


# ── Shared generator building-blocks ─────────────────────────────────────────
# All mutate `arr` in-place and yield event dicts.

def _ins_sort(arr, lo, hi):
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


def _merge(arr, lo, mid, hi):
    """Merge arr[lo..mid] and arr[mid+1..hi] in-place."""
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


def _heapify(arr, size, i, offset=0):
    """Iterative max-heapify for arr[offset .. offset+size-1], rooted at i."""
    while True:
        lg, l, r = i, 2*i + 1, 2*i + 2
        if l < size:
            yield {"type": "compare", "idx": (offset + lg, offset + l)}
            if arr[offset + l] > arr[offset + lg]: lg = l
        if r < size:
            yield {"type": "compare", "idx": (offset + lg, offset + r)}
            if arr[offset + r] > arr[offset + lg]: lg = r
        if lg != i:
            arr[offset + i], arr[offset + lg] = arr[offset + lg], arr[offset + i]
            yield {"type": "swap", "idx": (offset + i, offset + lg)}
            i = lg
        else:
            break


def _heap_sort_range(arr, lo, hi):
    """Heap sort over arr[lo..hi] inclusive (reuses _heapify)."""
    size = hi - lo + 1
    for i in range(size // 2 - 1, -1, -1):
        yield from _heapify(arr, size, i, lo)
    for i in range(size - 1, 0, -1):
        arr[lo], arr[lo + i] = arr[lo + i], arr[lo]
        yield {"type": "swap", "idx": (lo, lo + i)}
        yield from _heapify(arr, i, 0, lo)


def _partition(arr, lo, hi, out, median_of_three=False):
    """Lomuto partition. Writes pivot index into out[0]."""
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
    i = lo - 1
    for j in range(lo, hi):
        yield {"type": "compare", "idx": (j, hi)}
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield {"type": "swap", "idx": (i, j)}
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    yield {"type": "swap", "idx": (i + 1, hi)}
    out[0] = i + 1


# ── Sorting algorithms ────────────────────────────────────────────────────────

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            yield {"type": "compare", "idx": (j, j + 1)}
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield {"type": "swap", "idx": (j, j + 1)}
    yield {"type": "done"}


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            yield {"type": "compare", "idx": (m, j)}
            if arr[j] < arr[m]: m = j
        if m != i:
            arr[i], arr[m] = arr[m], arr[i]
            yield {"type": "swap", "idx": (i, m)}
    yield {"type": "done"}


def insertion_sort(arr):
    yield from _ins_sort(arr, 0, len(arr) - 1)
    yield {"type": "done"}


def merge_sort(arr):
    def sort(lo, hi):
        if lo < hi:
            mid = (lo + hi) // 2
            yield from sort(lo, mid)
            yield from sort(mid + 1, hi)
            yield from _merge(arr, lo, mid, hi)
    yield from sort(0, len(arr) - 1)
    yield {"type": "done"}


def quick_sort(arr):
    def sort(lo, hi):
        if lo < hi:
            out = [0]
            yield from _partition(arr, lo, hi, out)
            pi = out[0]
            yield from sort(lo, pi - 1)
            yield from sort(pi + 1, hi)
    yield from sort(0, len(arr) - 1)
    yield {"type": "done"}


def heap_sort(arr):
    yield from _heap_sort_range(arr, 0, len(arr) - 1)
    yield {"type": "done"}


def shell_sort(arr):
    n, gap = len(arr), len(arr) // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]; j = i
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


def tree_sort(arr):
    class Node:
        __slots__ = ("val", "idx", "left", "right")
        def __init__(self, val, idx):
            self.val = val; self.idx = idx
            self.left = self.right = None

    def insert(root_box, val, idx):
        if root_box[0] is None:
            root_box[0] = Node(val, idx); return
        node = root_box[0]
        while True:
            yield {"type": "compare", "idx": (idx, node.idx)}
            if val < node.val:
                if node.left  is None: node.left  = Node(val, idx); break
                node = node.left
            else:
                if node.right is None: node.right = Node(val, idx); break
                node = node.right

    root_box = [None]
    for i in range(len(arr)):
        yield from insert(root_box, arr[i], i)

    result, stack, cur = [], [], root_box[0]
    while stack or cur:
        while cur: stack.append(cur); cur = cur.left
        cur = stack.pop(); result.append(cur.val); cur = cur.right

    for i, v in enumerate(result):
        arr[i] = v
        yield {"type": "overwrite", "idx": i, "val": v}
    yield {"type": "done"}


def tim_sort(arr):
    RUN, n = 32, len(arr)
    for i in range(0, n, RUN):
        yield from _ins_sort(arr, i, min(i + RUN - 1, n - 1))
    size = RUN
    while size < n:
        for lo in range(0, n, 2 * size):
            mid = min(lo + size - 1,     n - 1)
            hi  = min(lo + 2 * size - 1, n - 1)
            if mid < hi:
                yield from _merge(arr, lo, mid, hi)
        size *= 2
    yield {"type": "done"}


def intro_sort(arr):
    n         = len(arr)
    max_depth = 2 * math.floor(math.log2(max(n, 2)))

    def introsort(lo, hi, depth):
        size = hi - lo + 1
        if size <= 1:
            return
        if size <= 16:
            yield from _ins_sort(arr, lo, hi)
        elif depth == 0:
            yield from _heap_sort_range(arr, lo, hi)
        else:
            out = [0]
            yield from _partition(arr, lo, hi, out, median_of_three=True)
            pi = out[0]
            yield from introsort(lo, pi - 1, depth - 1)
            yield from introsort(pi + 1, hi, depth - 1)

    yield from introsort(0, n - 1, max_depth)
    yield {"type": "done"}


SORTERS = [
    bubble_sort, selection_sort, insertion_sort,
    merge_sort,  quick_sort,     heap_sort,
    shell_sort,  tree_sort,      tim_sort,  intro_sort,
]


# ── Drawing ───────────────────────────────────────────────────────────────────

def draw_bars(screen, arr, cmp, swp, ovw, done):
    screen.fill(BG, (0, 0, WIDTH, VIZ_H))
    bw = WIDTH / len(arr)
    for i, v in enumerate(arr):
        if done:          color = DONE_CLR
        elif i in swp:    color = SWAP_CLR
        elif i in ovw:    color = OVERWRITE_CLR
        elif i in cmp:    color = COMPARE_CLR
        else:             color = BAR_COLOR
        pygame.draw.rect(screen, color,
                         (i * bw, VIZ_H - (v / MAX_VAL) * VIZ_H,
                          max(bw - 1, 1), (v / MAX_VAL) * VIZ_H))


def draw_menu(screen, font, active_idx, speed_idx, paused):
    pygame.draw.rect(screen, MENU_BG, (0, VIZ_H, WIDTH, MENU_H))
    pygame.draw.line(screen, DIVIDER, (0, VIZ_H), (WIDTH, VIZ_H), 1)

    bw, bh = WIDTH // 5, MENU_H // 2
    for i, name in enumerate(ALGORITHMS):
        row, col = divmod(i, 5)
        x, y     = col * bw, VIZ_H + row * bh
        active   = (i == active_idx)

        pygame.draw.rect(screen, ACTIVE_BG if active else MENU_BG, (x, y, bw, bh))
        if active:
            pygame.draw.rect(screen, ACTIVE_BORDER, (x, y, bw, bh), 2)

        key   = str(i + 1) if i < 9 else "0"
        label = font.render(f"{key}. {name}", True, TEXT_BRIGHT if active else TEXT_DIM)
        screen.blit(label, (x + (bw - label.get_width()) // 2,
                             y + (bh - label.get_height()) // 2))
        if col > 0:
            pygame.draw.line(screen, DIVIDER, (x, y), (x, y + bh), 1)

    pygame.draw.line(screen, DIVIDER, (0, VIZ_H + bh), (WIDTH, VIZ_H + bh), 1)

    hint = (f"  {ALGORITHMS[active_idx]}   "
            f"Speed {SPEED_LEVELS[speed_idx]}x [↑↓]   "
            f"R=restart   SPACE={'resume' if paused else 'pause'}  ")
    hsurf = font.render(hint, True, TEXT_DIM)
    bg    = pygame.Surface((hsurf.get_width() + 4, hsurf.get_height() + 4), pygame.SRCALPHA)
    bg.fill((10, 12, 16, 200))
    screen.blit(bg,    (4, 4))
    screen.blit(hsurf, (6, 6))


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Algorithms")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("monospace", 14)

    active_idx = 0
    speed_idx  = 0
    paused     = False
    done       = False

    def new_sort(idx):
        a = [random.randint(10, MAX_VAL - 10) for _ in range(NUM_BARS)]
        return a, SORTERS[idx](a)

    arr, gen = new_sort(active_idx)
    cmp = swp = ovw = frozenset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    arr, gen = new_sort(active_idx)
                    cmp = swp = ovw = frozenset()
                    paused = done = False

                elif event.key == pygame.K_SPACE:
                    if done:
                        arr, gen = new_sort(active_idx)
                        cmp = swp = ovw = frozenset()
                        done = False
                    else:
                        paused = not paused

                elif event.key == pygame.K_UP:
                    speed_idx = min(speed_idx + 1, len(SPEED_LEVELS) - 1)
                elif event.key == pygame.K_DOWN:
                    speed_idx = max(speed_idx - 1, 0)

                elif event.key in KEY_MAP:
                    active_idx = KEY_MAP[event.key]
                    arr, gen   = new_sort(active_idx)
                    cmp = swp = ovw = frozenset()
                    paused = done = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if my >= VIZ_H:
                    bw, bh = WIDTH // 5, MENU_H // 2
                    idx    = (my - VIZ_H) // bh * 5 + mx // bw
                    if 0 <= idx < len(ALGORITHMS):
                        active_idx = idx
                        arr, gen   = new_sort(active_idx)
                        cmp = swp = ovw = frozenset()
                        paused = done = False

        if not paused and not done:
            for _ in range(SPEED_LEVELS[speed_idx]):
                step = next(gen, None)
                if step is None or step["type"] == "done":
                    cmp = swp = ovw = frozenset()
                    done = True; break
                t = step["type"]
                if t == "compare":
                    cmp = frozenset(step["idx"]); swp = ovw = frozenset()
                    beep(arr[step["idx"][0]])
                elif t == "swap":
                    swp = frozenset(step["idx"]); cmp = ovw = frozenset()
                    beep(arr[step["idx"][0]])
                elif t == "overwrite":
                    ovw = frozenset({step["idx"]}); cmp = swp = frozenset()
                    beep(step["val"])

        draw_bars(screen, arr, cmp, swp, ovw, done)
        draw_menu(screen, font, active_idx, speed_idx, paused)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
