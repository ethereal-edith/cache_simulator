"""
case_study.py — Q16: Integrated Case Study

Workload: linked-list traversal.

A singly linked list with 16 nodes, each 32 bytes, allocated non-contiguously
across the heap. Traversing the list touches each node in order of the next
pointer — which means consecutive accesses land in unrelated blocks.

Because the addresses are scattered and each node is visited once, the workload
has no locality.
"""

from main import run_simulation
from functions import calculate_rates

BLOCK_SIZE = 32   # one node per block

# 16 node addresses, Each address is the start of a distinct 32-byte block.
SINGLE_PASS = [0, 512, 256, 768, 384, 128, 640, 896,
               64, 576, 320, 832, 192, 704, 448, 960]

# Two traversals of the same list — the second pass gives the cache a chance
# to reuse blocks loaded during the first pass.
DOUBLE_PASS = SINGLE_PASS + SINGLE_PASS

# Experiment 1: single traversal 

def run_baseline():
    hits, misses = run_simulation(
        cache_size=4096,
        block_size=BLOCK_SIZE,
        associativity=1,
        policy="LRU",
        requests=SINGLE_PASS,
        verbose=True,          # for the report
    )
    hit_rate, miss_rate = calculate_rates(hits, misses)
    print(f"\nBaseline (4 KB, 1-way, LRU): "
          f"{hits} hits, {misses} misses, hit rate {hit_rate}%")

# Experiment 2: single traversal, across cache size and associativity

def run_sweep(requests, label):
    """Vary cache size and associativity for a given reference string."""
    print(f"\n=== Sweep: {label} ===")
    header = f"{'Size':>6} {'Assoc':>6} {'Hits':>6} {'Miss':>6} {'Hit%':>8}"
    print(header)
    print("-" * len(header))

    for cache_size in [1024, 4096, 16384]:
        for associativity in [1, 2, 4]:
            slots = cache_size // BLOCK_SIZE
            if associativity > slots:
                continue
            hits, misses = run_simulation(
                cache_size, BLOCK_SIZE, associativity,
                "LRU", requests, verbose=False
            )
            hit_rate, _ = calculate_rates(hits, misses)
            print(f"{cache_size:>6} {associativity:>6} "
                  f"{hits:>6} {misses:>6} {hit_rate:>8.2f}")

# Main
if __name__ == "__main__":
    run_baseline()
    run_sweep(SINGLE_PASS, "single traversal")
    run_sweep(DOUBLE_PASS, "double traversal")