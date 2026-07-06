"""
Run sorting algorithm visualizations.

Usage
-----
  python run.py                              # all 10 – switch with menu
  python run.py bubble                       # single algorithm
  python run.py merge quick heap             # three algorithms – switch with menu

  python run.py --parallel bubble merge quick   # race side-by-side, same array
  python run.py --parallel                       # all 10 in parallel

  python run.py --series                         # all 10 auto-advance in sequence
  python run.py --series bubble selection insertion  # subset in sequence

  python run.py --bars 50 bubble             # start with 50 bars
  python run.py --list                       # show available keys

Keys (all modes)
----------------
  ↑ / ↓    speed up / slow down
  [ / ]    fewer / more bars  (restarts sort)
  T        cycle colour theme  (Color → B&W)
  R        new random array, restart
  SPACE    pause / resume

  (switch-menu mode only)
  1–9, 0   jump to algorithm
  click    click bottom menu
"""

import sys
from algorithms import ALGO_MAP, ALL_ALGORITHMS
from core.engine import run_visualizer, run_parallel, run_series


def _parse(argv):
    """Return (mode, algos, bars)."""
    mode     = "switch"   # switch | parallel | series
    bars_arg = None
    keys     = []

    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--parallel": mode = "parallel"
        elif a == "--series":  mode = "series"
        elif a == "--list":
            print("Available algorithm keys:")
            for key, (name, _) in ALGO_MAP.items():
                print(f"  {key:<12}  →  {name}")
            sys.exit(0)
        elif a == "--bars":
            i += 1
            if i >= len(argv):
                print("--bars requires a number"); sys.exit(1)
            bars_arg = int(argv[i])
        elif a.startswith("--bars="):
            bars_arg = int(a.split("=", 1)[1])
        elif a.startswith("--"):
            print(f"Unknown flag: {a}"); sys.exit(1)
        else:
            keys.append(a)
        i += 1

    if not keys:
        algos = ALL_ALGORITHMS
    else:
        algos, unknown = [], []
        for k in keys:
            if k in ALGO_MAP: algos.append(ALGO_MAP[k])
            else:             unknown.append(k)
        if unknown:
            print(f"Unknown algorithm(s): {', '.join(unknown)}")
            print("Run  python run.py --list  to see valid keys.")
            sys.exit(1)

    return mode, algos, bars_arg


def main():
    mode, algos, bars = _parse(sys.argv[1:])
    kwargs = {"default_bars": bars} if bars else {}

    if   mode == "parallel": run_parallel(algos, **kwargs)
    elif mode == "series":   run_series(algos, **kwargs)
    else:                    run_visualizer(algos, **kwargs)


if __name__ == "__main__":
    main()
