# Sorting Algorithm Visualizer

A pygame-based visualizer for 15 sorting algorithms. Watch them sort in real time with live operation counts, seed-controlled arrays, and a post-sort verification sweep.

## Algorithms

| Key | Algorithm | Time Complexity | Space |
|-----|-----------|-----------------|-------|
| `1` | Bogo Sort | O((n+1)!) avg ⚠️ use ≤8 bars | O(1) |
| `2` | Bubble Sort | O(n²) | O(1) |
| `3` | Bucket Sort | O(n+k) avg | O(n) |
| `4` | Cocktail Sort | O(n²) | O(1) |
| `5` | Comb Sort | O(n log n) avg | O(1) |
| `6` | Counting Sort | O(n+k) | O(k) |
| `7` | Heap Sort | O(n log n) | O(1) |
| `8` | Insertion Sort | O(n²) | O(1) |
| `9` | Intro Sort | O(n log n) | O(log n) |
| `0` | Merge Sort | O(n log n) | O(n) |
| `Q` | Quick Sort | O(n log n) avg | O(log n) |
| `W` | Radix Sort (LSD) | O(nk) | O(n+k) |
| `E` | Selection Sort | O(n²) | O(1) |
| `A` | Shell Sort | O(n log n) avg | O(1) |
| `S` | Tim Sort | O(n log n) | O(n) |

## Install

```bash
pip install pygame numpy
```

## Run

```bash
# All 15 algorithms — switch with menu or keys (default)
python run.py

# Single algorithm
python run.py bubble

# Pick any combination
python run.py merge quick heap

# All algorithms racing side-by-side on the same array
python run.py --parallel

# Subset in parallel
python run.py --parallel bubble merge quick

# Full series — auto-advances through all algorithms
python run.py --series

# Start with a specific bar count
python run.py --bars 1000 bubble

# List all algorithm keys
python run.py --list
```

## Controls

| Key | Action |
|-----|--------|
| `R` | New random array, start sorting |
| `Space` | Pause / resume (or start after reset) |
| `↑` / `↓` | Speed up / slow down |
| `[` / `]` | Step through bar presets (resets, stays paused) |
| `,` / `.` | Seed − 1 / Seed + 1 (resets, stays paused) |
| `T` | Cycle colour theme (Color → B&W) |
| `H` | Toggle / hide bottom algorithm menu |
| `1`–`9`, `0` | Jump to algorithm 1–10 (resets, stays paused) |
| `Q` `W` `E` `A` `S` | Jump to algorithm 11–15 (resets, stays paused) |
| Click | Select algorithm from bottom menu |
| Click `Menu ▼` | Toggle bottom menu (bottom-right button) |

> **Note:** Changing bars, seed, or algorithm resets the array but keeps it **paused**. Press `R` or `Space` to start sorting.

## Bar count presets

Cycled with `[` / `]`:

`100 → 200 → 300 → 400 → 500 → 1k → 2k → 3k → 4k → 5k → 10k → 20k → 30k → 40k → 50k → 60k → 70k → 80k → 90k → 100k`

## Speed levels

Cycled with `↑` / `↓`:

`2 → 4 → 8 → 16 → 32 → 64 → 128 → 256 → 512 → 1024` steps per frame

## Seed control

Every run uses a **seeded random array** (default seed `42`). Same seed + same algorithm + same bar count = identical array and identical stats every time. Use `,` / `.` to try different arrays without losing reproducibility.

## Stats & verification

After sorting completes:
1. A **white scan sweeps left → right** verifying the array is sorted (with ascending sound)
2. A **stats card** appears in the centre showing:
   - Time taken (frozen at sort completion)
   - Comparisons (yellow)
   - Swaps (teal)
   - Writes / overwrites (blue)
   - Total operations (white)

Live counters (comparisons, swaps, writes, total ops) are always visible in the bottom-left corner during sorting.

## Colour legend

| Colour | Meaning |
|--------|---------|
| Pink | Unsorted bar |
| Yellow | Comparing |
| Teal | Swapping |
| Blue | Overwrite (merge / insertion / radix) |
| Green | Sorted / verified |
| White | Verification scan head |

## Project structure

```
├── algorithms/
│   ├── bogo_sort.py
│   ├── bubble_sort.py
│   ├── bucket_sort.py
│   ├── cocktail_shaker_sort.py
│   ├── comb_sort.py
│   ├── counting_sort.py
│   ├── heap_sort.py
│   ├── insertion_sort.py
│   ├── intro_sort.py
│   ├── merge_sort.py
│   ├── quick_sort.py
│   ├── radix_sort.py
│   ├── selection_sort.py
│   ├── shell_sort.py
│   └── tim_sort.py
├── core/
│   ├── constants.py   ← window size, colours, speed levels, bar presets
│   ├── sound.py       ← tone generation
│   ├── primitives.py  ← shared helpers (_merge, _heapify, _partition, …)
│   └── engine.py      ← pygame loop, run_visualizer / run_parallel / run_series
├── run.py             ← CLI entry point
└── run_all.py         ← shortcut to run all 15
```

## Tuning

| What | File | Setting |
|------|------|---------|
| Window size | `core/constants.py` | `WIDTH, HEIGHT = 1680, 900` |
| Default bar count | `core/constants.py` | `NUM_BARS = 100` |
| Bar presets | `core/constants.py` | `BAR_PRESETS` list |
| Speed steps | `core/constants.py` | `SPEED_LEVELS` list |
| Bar colours / themes | `core/constants.py` | `THEMES` list |
| Default speed index | `core/engine.py` | `speed_idx = 2` |
| Default seed | `core/engine.py` | `seed = 42` |
| Sound pitch range | `core/sound.py` | `300 + (value / MAX_VAL) * 900` |
| Sound volume | `core/sound.py` | `0.30 * 32767` |
