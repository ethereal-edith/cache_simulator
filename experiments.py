#investigating how cache size and associativity affect hit rate, across three workloads.
#constants = Block size(16 bytes), Replacement policy(LRU), string length
#variables = Cache size, Associativity, Workload (sequential (no reuse), locality(small hot working set), conflict(all blocks collide on one set))

import matplotlib.pyplot as plt
from main import run_simulation
from functions import calculate_rates

BLOCK_SIZE = 16
POLICY = "LRU"
#combination. 4 × 3 = 12 rows each.
CACHE_SIZES = [64, 128, 256, 512]     # bytes
ASSOCIATIVITIES = [1, 2, 4]           # 1 = direct, 2 = 2-way, 4 = 4-way

# Workloads (reference strings)
SEQUENTIAL = [0, 16, 32, 48, 64, 80, 96, 112,
              128, 144, 160, 176, 192, 208, 224, 240]

LOCALITY = [0, 16, 0, 16, 0, 16, 32, 32, 0, 16, 0, 16, 0, 16]

# Addresses->all blocks map to the same set(0)
CONFLICT = [0, 64, 128, 192, 0, 64, 128, 192, 0, 64, 128, 192]

# dictionary grouping the workloads with names. loops over the dict
#each iteration gives you a name (for output table) and an address list (for the simulator)
WORKLOADS = {
    "sequential": SEQUENTIAL,
    "locality":   LOCALITY,
    "conflict":   CONFLICT,
}


def run_experiment():
    # Starts with an empty result list. Every run will add one result dict to it. By the end, results will have 36 entries (3 workloads × 4 cache sizes × 3 associativities = 36 ).
    results = []
    # Outer loop. Runs 3 times, once per workload
    for workload_name, addresses in WORKLOADS.items():
        #Runs 4 times, once per cache size
        for cache_size in CACHE_SIZES:
            #Runs 3 times, once per associativity.
            for associativity in ASSOCIATIVITIES:

                slots = cache_size // BLOCK_SIZE
                if associativity > slots:
                    continue

                #run_simulation builds a fresh cache, iterates through addresses, and returns (hits, misses). 
                hits, misses = run_simulation(
                    cache_size, BLOCK_SIZE, associativity, POLICY,
                    addresses, verbose=False
                )
                hit_rate, _ = calculate_rates(hits, misses)

                #Record the run
                results.append({
                    "workload":      workload_name,
                    "cache_size":    cache_size,
                    "associativity": associativity,
                    "references":    len(addresses),
                    "hits":          hits,
                    "misses":        misses,
                    "hit_rate":      hit_rate,
                })

    return results

#f-string alignment formatting
def print_table(results):
    header = f"{'Workload':<12} {'Size':>5} {'Assoc':>5} {'Refs':>5} {'Hits':>5} {'Miss':>5} {'Hit%':>8}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['workload']:<12} {r['cache_size']:>5} {r['associativity']:>5} "
              f"{r['references']:>5} {r['hits']:>5} {r['misses']:>5} {r['hit_rate']:>8.2f}")

#graphing function
def plot_results(results):
    """One subplot per workload; one line per associativity."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
    workloads = ["sequential", "locality", "conflict"]

    colors = {1: "tab:blue", 2: "tab:orange", 4: "tab:green"}

    for ax, wl in zip(axes, workloads):
        for assoc in ASSOCIATIVITIES:
            rows = [r for r in results
                    if r["workload"] == wl and r["associativity"] == assoc]
            rows.sort(key=lambda r: r["cache_size"])

            sizes = [r["cache_size"] for r in rows]
            rates = [r["hit_rate"] for r in rows]
            ax.plot(sizes, rates,
                    marker="o",
                    color=colors[assoc],
                    alpha=0.6,
                    label=f"{assoc}-way")

        ax.set_title(wl)
        ax.set_xlabel("Cache size (bytes)")
        ax.set_xticks(CACHE_SIZES)
        ax.set_ylim(-5, 105)
        ax.grid(True, alpha=0.3)
        ax.legend()

    axes[0].set_ylabel("Hit rate (%)")
    fig.suptitle("Q14: Hit rate vs cache size and associativity")
    fig.tight_layout()
    fig.savefig("q14_graph.png", dpi=150)
    print("Saved q14_graph.png")


if __name__ == "__main__":
    results = run_experiment()
    print_table(results)
    plot_results(results)