from functions import *
from main import *

# test
print("--block number test--")
print(get_block_number(16, 4)) # print 4
print(get_block_number(65, 8)) # print 8

# test
print("--number of sets test--")
print(get_num_of_set(64, 16, 1)) # print 4
print(get_num_of_set(128, 16, 1)) # print 8

# test
print("--set index test--")
print(get_set_index(5, 4)) # print 1
print(get_set_index(9, 1)) # print 0     

# test
print("--tag test--")
print(get_tag(6, 3)) # print 2
print(get_tag(9, 4)) # print 2

# test
print("--create cache test--")
print(create_cache(4, 2)) # print [[None, None], [None, None], [None, None], [None, None]]
print(create_cache(1, 4)) # print [[None, None, None, None]]

# test
tests = [
    ([None, None], 3),
    ([{'tag': 3}, None], 3),
    ([{'tag': 2}, {'tag': 5}], 3),
    ([{'tag': 2}, {'tag': 3}], 3)
]

print("--is_hit test results--")
for cache_set, tag in tests:
    print(f"cache_set: {cache_set}, tag: {tag} -> Output: {is_hit(cache_set, tag)}")

# test
print("--find empty slot test--")
print(find_empty_slot([None, None])) # print 0  
print(find_empty_slot([{'tag': 3}, None])) # print 1
print(find_empty_slot([{'tag': 2}, {'tag': 5}])) # print -1

# test
print("--update on hit test--")
test_set = [
    {'tag': 2, 'insertion_time': 1, 'last_access_time': 1},
    {'tag': 3, 'insertion_time': 2, 'last_access_time': 2}
]
update_on_hit(test_set, 2, 7)
print(test_set)

# test
print("--find victim test--")   
test_set = [
    {'tag': 2, 'insertion_time': 1, 'last_access_time': 7},
    {'tag': 3, 'insertion_time': 2, 'last_access_time': 2}
]
print(find_victim(test_set, "LRU"))   # print 1
print(find_victim(test_set, "FIFO"))  # print 0

print("--invalid policy test--")
try:
    find_victim(test_set, "LIFO")
except ValueError as e:
    print("The error is:", e)

# test
print("--access cache test--")
cache = create_cache(4, 1)
requests = [0, 1, 0, 1, 4, 0]
time = 1
for address in requests:
    result = access_cache(cache, address, 1, 1, "LRU", time)
    print(address, result)
    time += 1

# test
sim_tests = [
    ((64, 16, 2, "LRU", [0, 4, 8, 0, 16, 4, 20, 0]), (6, 2)),
    ((64, 16, 1, "LRU", [0, 64, 0, 64]), (0, 4)),
    ((64, 16, 2, "LRU", [0, 64, 0, 64]), (2, 2)),
    ((64, 16, 4, "LRU", [0, 16, 32, 48, 0, 64, 16]), (1, 6)),
    ((64, 16, 4, "FIFO", [0, 16, 32, 48, 0, 64, 16]), (2, 5)),
]

print("--simulation test results--")
for inputs, expected in sim_tests:
    result = run_simulation(*inputs)
    print("PASS" if result == expected else "FAIL", expected, result)

# test
rate_tests = [
    # (hits, misses), expected_(hit_rate, miss_rate), description
    ((6, 2), (75.0, 25.0), "Standard case"),
    ((0, 4), (0.0, 100.0), "All misses"),
    ((1, 6), (14.29, 85.71), "Rounding check"),
    ((0, 0), (0.0, 0.0), "Zero accesses edge case"),
]

print("--rate calculation test results--")
for (hits, misses), expected, description in rate_tests:
    result = calculate_rates(hits, misses)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status} | {description} -> Expected: {expected}, Got: {result}")

print(run_simulation(64, 16, 2, "LRU", [0, 4, 8, 0, 16, 4, 20, 0], verbose=False))