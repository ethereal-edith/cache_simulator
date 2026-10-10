from functions import *

def run_simulation(cache_size, block_size, associativity, policy, requests, verbose=True):
    num_of_sets = get_num_of_set(cache_size, block_size, associativity)
    cache = create_cache(num_of_sets, associativity)
    time = 1
    hits = 0
    misses = 0

    if verbose:
        print(f"Cache Size: {cache_size}, Block Size: {block_size}, Associativity: {associativity}, Policy: {policy}")
        print(f"Number of Sets: {num_of_sets}")
        print("Initial Cache State:")
        for i, cache_set in enumerate(cache):
            print(f"Set {i}: {cache_set}")
        print("\nProcessing Requests:")

    for address in requests:
        result = access_cache(cache, address, block_size, associativity, policy, time)
        if result == "Hit":
            hits += 1
        else:
            misses += 1
        if verbose:
            print(f"Address: {address}, Result: {result}")
            for i, cache_set in enumerate(cache):
                print(f"  Set {i}: {cache_set}")
        time += 1

    if verbose:
        print("\nFinal Cache State:")
        for i, cache_set in enumerate(cache):
            print(f"Set {i}: {cache_set}")

        hit_rate, miss_rate = calculate_rates(hits, misses)
        print(f"\nSimulation Results:")
        print(f"Total References: {len(requests)}")
        print(f"Total Hits: {hits}, Total Misses: {misses}")
        print(f"Hit Rate: {hit_rate:.2f}%, Miss Rate: {miss_rate:.2f}%")

    return hits, misses