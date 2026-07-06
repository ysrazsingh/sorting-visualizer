# Sorting Algorithm Visualizer

A pygame-based visualizer for 10 sorting algorithms. Watch them sort in real time — switch between algorithms, race them side-by-side, or let them run as a full series.

## Algorithms

| # | Algorithm | Complexity |
|---|-----------|------------|
| 1 | Bubble Sort | O(n²) |
| 2 | Selection Sort | O(n²) |
| 3 | Insertion Sort | O(n²) |
| 4 | Merge Sort | O(n log n) |
| 5 | Quick Sort | O(n log n) avg |
| 6 | Heap Sort | O(n log n) |
| 7 | Shell Sort | O(n log n) avg |
| 8 | Tree Sort | O(n log n) avg |
| 9 | TimSort | O(n log n) |
| 10 | IntroSort | O(n log n) |

## Install

```bash
pip install pygame numpy
```

## Run

```bash
# Single algorithm
python run.py bubble

# Pick any combination (switch with menu or 1–9 keys)
python run.py merge quick heap

# All 10 racing side-by-side on the same array
python run.py --parallel

# Subset in parallel
python run.py --parallel bubble merge quick

# Full series — auto-advances through all 10
python run.py --series

# Custom bar count
python run.py --bars 50 bubble

# Run an algorithm file directly
python algorithms/bubble_sort.py

# List all algorithm keys
python run.py --list
```

## Controls

| Key | Action |
|-----|--------|
| `↑` / `↓` | Speed up / slow down |
| `[` / `]` | Fewer / more bars (restarts) |
| `T` | Cycle colour theme (Color → B&W) |
| `R` | New random array, restart |
| `Space` | Pause / resume |
| `1`–`9`, `0` | Jump to algorithm (switch mode) |
| Click | Select algorithm from bottom menu |

## Color legend

| Color | Meaning |
|-------|---------|
| 🔴 Pink | Unsorted bar |
| 🟡 Yellow | Comparing |
| 🟢 Teal | Swapping |
| 🔵 Blue | Overwrite (merge / insertion) |
| ✅ Green | Sorted |

## Project structure

```
├── algorithms/
│   ├── bubble_sort.py
│   ├── selection_sort.py
│   ├── insertion_sort.py
│   ├── merge_sort.py
│   ├── quick_sort.py
│   ├── heap_sort.py
│   ├── shell_sort.py
│   ├── tree_sort.py
│   ├── tim_sort.py
│   └── intro_sort.py
├── core/
│   ├── constants.py   ← colours, speed levels, bar count
│   ├── sound.py       ← tone generation
│   ├── primitives.py  ← shared sort helpers (_merge, _heapify, …)
│   └── engine.py      ← pygame loop, run_visualizer / run_parallel / run_series
├── run.py             ← CLI entry point
└── run_all.py         ← shortcut for all 10
```

## Tuning

All defaults are in `core/constants.py` and `core/engine.py` — no magic numbers elsewhere.

| What | File | Line |
|------|------|------|
| Bar count default | `core/constants.py` | `NUM_BARS = 80` |
| Speed steps | `core/constants.py` | `SPEED_LEVELS = [2, 4, 8, ...]` |
| Bar colours | `core/constants.py` | `THEMES` list |
| Default speed index | `core/engine.py` | `speed_idx = 2` |
| Default theme | `core/engine.py` | `theme_idx = 0` |
| Sound pitch range | `core/sound.py` | `300 + (value / MAX_VAL) * 900` |
| Sound volume | `core/sound.py` | `0.30 * 32767` |
