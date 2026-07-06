"""
Visualizer engine.

    run_visualizer(algos)           – switch between algos with menu / number keys
    run_parallel(algos)             – all algos race side-by-side, same array
    run_series(algos)               – algos play sequentially, auto-advances

Keys that work in every mode
----------------------------
  ↑ / ↓        speed up / slow down  (SPEED_LEVELS in constants.py)
  [ / ]        fewer / more bars     (20 – 200, restart with new array)
  T            cycle colour theme    (Color → B&W → …)
  R            new random array, restart
  SPACE        pause / resume  (or restart when finished)

Where to tune defaults
----------------------
  core/constants.py  →  SPEED_LEVELS   change the available speed steps
  core/constants.py  →  THEMES         edit / add colour themes
  core/engine.py     →  speed_idx=2    default speed (index into SPEED_LEVELS)
  core/engine.py     →  num_bars=…     default bar count
"""

import pygame
import random
from .constants import (
    WIDTH, HEIGHT, NUM_BARS, MAX_VAL,
    BG, MENU_BG, DIVIDER, TEXT_DIM, TEXT_BRIGHT, ACTIVE_BG, ACTIVE_BORDER,
    SPEED_LEVELS, THEMES, THEME_NAMES,
)
from .sound import beep as _beep

_KEY_MAP = {
    pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
    pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
    pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8,
    pygame.K_0: 9,
}

# ── layout ────────────────────────────────────────────────────────────────────

def _menu_layout(n: int):
    """(menu_h, cols, rows, btn_w, btn_h) for n algorithm buttons."""
    if   n == 1: cols, rows, menu_h = 1, 1, 40
    elif n <= 5: cols, rows, menu_h = n, 1, 50
    else:        cols, rows, menu_h = 5, 2, 90
    return menu_h, cols, rows, WIDTH // cols, menu_h // rows


# ── drawing primitives ────────────────────────────────────────────────────────

def _bars(screen, arr, cmp, swp, ovw, done, theme, x_off, col_w, viz_h):
    """Draw bars for one algorithm column."""
    bw = col_w / len(arr)
    for i, v in enumerate(arr):
        if done:        color = theme["done"]
        elif i in swp:  color = theme["swap"]
        elif i in ovw:  color = theme["overwrite"]
        elif i in cmp:  color = theme["compare"]
        else:           color = theme["bar"]
        bh = (v / MAX_VAL) * viz_h
        pygame.draw.rect(screen, color,
                         (x_off + i * bw, viz_h - bh, max(bw - 1, 1), bh))


def _hud(screen, font, text: str):
    """Transparent overlay in top-left corner of the viz area."""
    surf = font.render(text, True, TEXT_DIM)
    bg   = pygame.Surface((surf.get_width() + 4, surf.get_height() + 4), pygame.SRCALPHA)
    bg.fill((10, 12, 16, 200))
    screen.blit(bg,   (4, 4))
    screen.blit(surf, (6, 6))


def _algo_buttons(screen, font, algos, active_idx, viz_h, menu_h, cols, btn_w, btn_h):
    pygame.draw.rect(screen, MENU_BG, (0, viz_h, WIDTH, menu_h))
    pygame.draw.line(screen, DIVIDER, (0, viz_h), (WIDTH, viz_h), 1)

    for i, (name, _) in enumerate(algos):
        row, col = divmod(i, cols)
        x, y     = col * btn_w, viz_h + row * btn_h
        active   = (i == active_idx)

        pygame.draw.rect(screen, ACTIVE_BG if active else MENU_BG, (x, y, btn_w, btn_h))
        if active:
            pygame.draw.rect(screen, ACTIVE_BORDER, (x, y, btn_w, btn_h), 2)

        key_str = str(i + 1) if i < 9 else "0"
        prefix  = f"{key_str}. " if len(algos) > 1 else ""
        label   = font.render(prefix + name, True, TEXT_BRIGHT if active else TEXT_DIM)
        screen.blit(label, (x + (btn_w - label.get_width())  // 2,
                             y + (btn_h - label.get_height()) // 2))
        if col > 0:
            pygame.draw.line(screen, DIVIDER, (x, y), (x, y + btn_h), 1)

    rows = (len(algos) + cols - 1) // cols
    for r in range(1, rows):
        pygame.draw.line(screen, DIVIDER,
                         (0, viz_h + r * btn_h), (WIDTH, viz_h + r * btn_h), 1)


def _status_bar(screen, font, text: str, y: int, h: int):
    """Centred single-line info row (used by parallel / series bottom bar)."""
    pygame.draw.rect(screen, MENU_BG, (0, y, WIDTH, h))
    pygame.draw.line(screen, DIVIDER, (0, y), (WIDTH, y), 1)
    surf = font.render(text, True, TEXT_DIM)
    screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2,
                        y + (h - surf.get_height()) // 2))


# ── shared helpers ────────────────────────────────────────────────────────────

def _new_array(n: int) -> list:
    return [random.randint(10, MAX_VAL - 10) for _ in range(n)]


def _advance(gen, arr, beep_on: bool):
    """
    Pull one step from gen.
    Returns (cmp, swp, ovw, done_flag).
    """
    step = next(gen, None)
    if step is None or step["type"] == "done":
        return frozenset(), frozenset(), frozenset(), True
    t = step["type"]
    if t == "compare":
        if beep_on: _beep(arr[step["idx"][0]])
        return frozenset(step["idx"]), frozenset(), frozenset(), False
    if t == "swap":
        if beep_on: _beep(arr[step["idx"][0]])
        return frozenset(), frozenset(step["idx"]), frozenset(), False
    if t == "overwrite":
        if beep_on: _beep(step["val"])
        return frozenset(), frozenset(), frozenset({step["idx"]}), False
    return frozenset(), frozenset(), frozenset(), False


def _fmt_time(ms: int) -> str:
    s = ms / 1000
    return f"{s:.2f}s" if s < 60 else f"{int(s)//60}m{int(s)%60:02d}s"


# ── mode 1 : standard (switch-menu) ──────────────────────────────────────────

def run_visualizer(algos: list, default_bars: int = NUM_BARS) -> None:
    """
    Switch between algorithms using the bottom menu / number keys.
    """
    if not algos:
        raise ValueError("algos must not be empty")

    n                             = len(algos)
    menu_h, cols, _, _, btn_h    = _menu_layout(n)
    viz_h                         = HEIGHT - menu_h
    multi                         = n > 1

    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(algos[0][0] if n == 1 else "Sorting Algorithms")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("monospace", 14)

    # ── tunable defaults ──────────────────────────────────────────────────────
    active_idx = 0
    speed_idx  = 2          # ← change default speed here (index into SPEED_LEVELS)
    theme_idx  = 0          # ← 0=Color, 1=B&W
    num_bars   = default_bars
    # ─────────────────────────────────────────────────────────────────────────

    paused = done = False
    start_ms = pygame.time.get_ticks()

    def new_sort(idx):
        a = _new_array(num_bars)
        return a, algos[idx][1](a), pygame.time.get_ticks()

    arr, gen, start_ms = new_sort(active_idx)
    cmp = swp = ovw = frozenset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                k = event.key

                if k == pygame.K_r:
                    arr, gen, start_ms = new_sort(active_idx)
                    cmp = swp = ovw = frozenset()
                    paused = done = False

                elif k == pygame.K_SPACE:
                    if done:
                        arr, gen, start_ms = new_sort(active_idx)
                        cmp = swp = ovw = frozenset(); done = False
                    else:
                        paused = not paused

                elif k == pygame.K_UP:
                    speed_idx = min(speed_idx + 1, len(SPEED_LEVELS) - 1)
                elif k == pygame.K_DOWN:
                    speed_idx = max(speed_idx - 1, 0)

                elif k == pygame.K_t:
                    theme_idx = (theme_idx + 1) % len(THEMES)

                elif k == pygame.K_LEFTBRACKET:
                    num_bars = max(20, num_bars - 10)
                    arr, gen, start_ms = new_sort(active_idx)
                    cmp = swp = ovw = frozenset(); paused = done = False

                elif k == pygame.K_RIGHTBRACKET:
                    num_bars = min(200, num_bars + 10)
                    arr, gen, start_ms = new_sort(active_idx)
                    cmp = swp = ovw = frozenset(); paused = done = False

                elif multi and k in _KEY_MAP:
                    idx = _KEY_MAP[k]
                    if idx < n:
                        active_idx = idx
                        arr, gen, start_ms = new_sort(active_idx)
                        cmp = swp = ovw = frozenset(); paused = done = False

            elif event.type == pygame.MOUSEBUTTONDOWN and multi:
                mx, my = event.pos
                if my >= viz_h:
                    col = mx // (WIDTH // cols)
                    row = (my - viz_h) // btn_h
                    idx = row * cols + col
                    if 0 <= idx < n:
                        active_idx = idx
                        arr, gen, start_ms = new_sort(active_idx)
                        cmp = swp = ovw = frozenset(); paused = done = False

        if not paused and not done:
            for _ in range(SPEED_LEVELS[speed_idx]):
                cmp, swp, ovw, done = _advance(gen, arr, beep_on=True)
                if done: break

        theme    = THEMES[theme_idx]
        elapsed  = pygame.time.get_ticks() - start_ms
        spd      = SPEED_LEVELS[speed_idx]

        screen.fill(BG, (0, 0, WIDTH, viz_h))
        _bars(screen, arr, cmp, swp, ovw, done, theme, 0, WIDTH, viz_h)
        _mh, _cols, _, _bw, _bh = _menu_layout(n)
        _algo_buttons(screen, font, algos, active_idx, viz_h,
                      _mh, _cols, _bw, _bh)
        _hud(screen, font,
             f"  {algos[active_idx][0]}  {spd}x [↑↓]  "
             f"Bars {num_bars} [[ ]]  T={THEME_NAMES[theme_idx]}  "
             f"R=restart  SPACE={'resume' if paused else 'pause'}  "
             f"{'✓ ' if done else ''}{_fmt_time(elapsed)}  ")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# ── mode 2 : parallel race ────────────────────────────────────────────────────

def run_parallel(algos: list, default_bars: int = NUM_BARS) -> None:
    """
    All algorithms sort the SAME shuffled array simultaneously, side-by-side.
    Only the leftmost column produces sound.
    """
    if not algos:
        raise ValueError("algos must not be empty")

    n        = len(algos)
    bar_h    = 50       # bottom info bar height
    viz_h    = HEIGHT - bar_h
    col_w    = WIDTH // n

    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Parallel Sort")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("monospace", 14)

    speed_idx = 2
    theme_idx = 0
    num_bars  = default_bars
    paused    = False

    def reset():
        base = _new_array(num_bars)
        arrs = [base[:] for _ in range(n)]
        gens = [algos[i][1](arrs[i]) for i in range(n)]
        st   = [{"cmp": frozenset(), "swp": frozenset(),
                 "ovw": frozenset(), "done": False} for _ in range(n)]
        return arrs, gens, st, pygame.time.get_ticks()

    arrs, gens, states, start_ms = reset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_r:
                    arrs, gens, states, start_ms = reset(); paused = False
                elif k == pygame.K_SPACE:
                    if all(s["done"] for s in states):
                        arrs, gens, states, start_ms = reset()
                    else:
                        paused = not paused
                elif k == pygame.K_UP:
                    speed_idx = min(speed_idx + 1, len(SPEED_LEVELS) - 1)
                elif k == pygame.K_DOWN:
                    speed_idx = max(speed_idx - 1, 0)
                elif k == pygame.K_t:
                    theme_idx = (theme_idx + 1) % len(THEMES)
                elif k == pygame.K_LEFTBRACKET:
                    num_bars = max(20, num_bars - 10)
                    arrs, gens, states, start_ms = reset(); paused = False
                elif k == pygame.K_RIGHTBRACKET:
                    num_bars = min(200, num_bars + 10)
                    arrs, gens, states, start_ms = reset(); paused = False

        if not paused:
            for i in range(n):
                if states[i]["done"]: continue
                for _ in range(SPEED_LEVELS[speed_idx]):
                    cmp, swp, ovw, done_flag = _advance(gens[i], arrs[i], beep_on=(i == 0))
                    states[i]["cmp"] = cmp
                    states[i]["swp"] = swp
                    states[i]["ovw"] = ovw
                    if done_flag:
                        states[i]["done"] = True; break

        theme   = THEMES[theme_idx]
        elapsed = pygame.time.get_ticks() - start_ms
        all_done = all(s["done"] for s in states)

        screen.fill(BG, (0, 0, WIDTH, viz_h))
        for i in range(n):
            s = states[i]
            _bars(screen, arrs[i], s["cmp"], s["swp"], s["ovw"],
                  s["done"], theme, i * col_w, col_w, viz_h)
            if i > 0:
                pygame.draw.line(screen, DIVIDER, (i * col_w, 0), (i * col_w, viz_h), 1)

        spd   = SPEED_LEVELS[speed_idx]
        names = "  |  ".join(
            f"{'✓ ' if states[i]['done'] else ''}{algos[i][0]}" for i in range(n))
        _status_bar(screen, font,
                    f"{names}    {spd}x [↑↓]  Bars {num_bars} [[ ]]  "
                    f"T={THEME_NAMES[theme_idx]}  R=restart  "
                    f"{'✓ all done  ' if all_done else ''}{_fmt_time(elapsed)}",
                    viz_h, bar_h)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# ── mode 3 : series (auto-advance) ───────────────────────────────────────────

def run_series(algos: list, default_bars: int = NUM_BARS) -> None:
    """
    Run all algorithms one after another automatically.
    After each finishes it pauses 1.5 s, then starts the next.
    """
    if not algos:
        raise ValueError("algos must not be empty")

    n      = len(algos)
    bar_h  = 50
    viz_h  = HEIGHT - bar_h

    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Series – All Algorithms")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("monospace", 14)

    speed_idx = 2
    theme_idx = 0
    num_bars  = default_bars
    paused    = False

    algo_idx  = 0
    done      = False
    done_at   = 0          # ms timestamp when current algo finished
    PAUSE_MS  = 1500       # wait before auto-advancing
    times     = {}         # algo_idx → elapsed ms

    def new_sort():
        a = _new_array(num_bars)
        return a, algos[algo_idx][1](a), pygame.time.get_ticks()

    arr, gen, start_ms = new_sort()
    cmp = swp = ovw = frozenset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_r:
                    arr, gen, start_ms = new_sort()
                    cmp = swp = ovw = frozenset(); paused = done = False
                elif k == pygame.K_SPACE:
                    paused = not paused
                elif k == pygame.K_UP:
                    speed_idx = min(speed_idx + 1, len(SPEED_LEVELS) - 1)
                elif k == pygame.K_DOWN:
                    speed_idx = max(speed_idx - 1, 0)
                elif k == pygame.K_t:
                    theme_idx = (theme_idx + 1) % len(THEMES)
                elif k == pygame.K_LEFTBRACKET:
                    num_bars = max(20, num_bars - 10)
                    arr, gen, start_ms = new_sort()
                    cmp = swp = ovw = frozenset(); paused = done = False
                elif k == pygame.K_RIGHTBRACKET:
                    num_bars = min(200, num_bars + 10)
                    arr, gen, start_ms = new_sort()
                    cmp = swp = ovw = frozenset(); paused = done = False

        now = pygame.time.get_ticks()

        if not paused and not done:
            for _ in range(SPEED_LEVELS[speed_idx]):
                cmp, swp, ovw, done = _advance(gen, arr, beep_on=True)
                if done:
                    times[algo_idx] = now - start_ms
                    done_at = now; break

        # auto-advance after pause
        if done and not paused and (now - done_at) >= PAUSE_MS:
            algo_idx = (algo_idx + 1) % n
            arr, gen, start_ms = new_sort()
            cmp = swp = ovw = frozenset(); done = False

        theme   = THEMES[theme_idx]
        elapsed = now - start_ms
        spd     = SPEED_LEVELS[speed_idx]
        name    = algos[algo_idx][0]
        prog    = f"{algo_idx + 1}/{n}"
        t_str   = _fmt_time(times.get(algo_idx, elapsed))

        screen.fill(BG, (0, 0, WIDTH, viz_h))
        _bars(screen, arr, cmp, swp, ovw, done, theme, 0, WIDTH, viz_h)
        _status_bar(screen, font,
                    f"{prog}  {name}  {t_str}    {spd}x [↑↓]  "
                    f"Bars {num_bars} [[ ]]  T={THEME_NAMES[theme_idx]}  "
                    f"R=restart  SPACE={'resume' if paused else 'pause'}",
                    viz_h, bar_h)
        _hud(screen, font, f"  {prog}  {name}  ")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
