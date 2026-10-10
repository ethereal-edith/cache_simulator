# Cache Simulator 🗂️

A small Python cache simulator for the Computer Architecture practical assignment (Q13). Give it a cache setup and a list of memory addresses, and it tells you how many were hits and how many were misses.

## What it does

It simulates a cache with direct-mapped, set-associative or fully associative layouts. It replaces blocks using LRU or FIFO and reports the hit rate and miss rate.

## Files

| File | What's inside |
|---|---|
| `functions.py` | The building blocks: block number, set index, tag, cache creation, hit check, replacement, rate calculation |
| `main.py` | `run_simulation()`, which runs a full simulation from start to finish |
| `test_cache.py` | Tests for every function, plus five full simulation cases |
| `experiments.py` | Empty for now |

## How to run the tests

```
python test_cache.py
```

Each simulation test prints `PASS` or `FAIL` next to the expected and actual result. Needs Python 3 only. No packages to install.

## How to run a simulation

```python
from main import run_simulation
from functions import calculate_rates

requests = [0, 4, 8, 0, 16, 4, 20, 0]

hits, misses = run_simulation(64, 16, 2, "LRU", requests, verbose=False)
hit_rate, miss_rate = calculate_rates(hits, misses)

print(hits, misses)          # 6 2
print(hit_rate, miss_rate)   # 75.0 25.0
```

Leave out `verbose=False` and the simulator prints the starting cache, then each request with its result and the cache contents after it, then the final cache and rates.`

## Parameters

| Parameter | Meaning |
|---|---|
| `cache_size` | Total size of the cache in bytes |
| `block_size` | Size of one block, in bytes |
| `associativity` | Number of slots in each set (see the next section) |
| `policy` | Replacement policy: `"LRU"` or `"FIFO"` (capital letters) |
| `requests` | List of memory addresses to access, in order |
| `verbose` | `True` prints every step. `False` prints nothing. Default is `True` |

`run_simulation` returns `(hits, misses)`.

## Cache types

The number of slots is `cache_size // block_size`. The cache type depends on `associativity`.

| `associativity` | Cache type |
|---|---|
| `1` | Direct mapped |
| Between 1 and the number of slots | Set-associative |
| Equal to the number of slots | Fully associative |

Example with `cache_size=64` and `block_size=16`, which gives 4 slots:

| `associativity` | Sets | Type |
|---|---|---|
| 1 | 4 | Direct mapped |
| 2 | 2 | Set-associative |
| 4 | 1 | Fully associative |