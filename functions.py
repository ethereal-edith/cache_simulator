# calculating block number function
def get_block_number(address, block_size):
    block_number = address // block_size #using floor division to account for any remainder
    return block_number

# calculate the number of sets (mod)
def get_num_of_set(cache_size, block_size, associativity):
    slots = cache_size // block_size
    sets = slots // associativity
    return sets

# NOTE: associativity is an input. It determines the type of cache,
# and the number of sets is calculated from it.
# For example, if associativity is 1, then it is a direct-mapped cache. 
# If associativity is equal to the number of slots, then it is a fully associative cache. 
# If associativity is greater than 1 but less than the number of slots, then it is a set-associative cache.

def get_set_index(block_number, num_of_sets):
    set_index = block_number % num_of_sets
    return set_index

def get_tag(block_number, num_of_sets):
    tag = block_number // num_of_sets
    return tag

def create_cache(num_of_sets, associativity):
    cache = []
    for i in range(num_of_sets):
        cache_set = []
        for j in range(associativity):
            cache_set.append(None) # initialize each slot in the cache_set to None
        cache.append(cache_set)
    return cache

def is_hit(cache_set, tag):
    for slot in cache_set:
        if slot is not None and slot['tag'] == tag:
            return True
    return False

def find_empty_slot(cache_set):
    for i in range(len(cache_set)):
        if cache_set[i] is None:
            return i
    return -1

def insert_block(cache_set, slot_index, tag, time):
    cache_set[slot_index] = {
        'tag': tag,
        'insertion_time': time,
        'last_access_time': time
    }

def update_on_hit(cache_set, tag, time):
    for slot in cache_set:
        if slot is not None and slot['tag'] == tag:
            slot['last_access_time'] = time
            break

def find_victim(cache_set, policy):
    if policy == 'LRU':
        oldest_time = float('inf')
        victim_index = -1
        for i, slot in enumerate(cache_set):
            if slot is not None and slot['last_access_time'] < oldest_time:
                oldest_time = slot['last_access_time']
                victim_index = i
        return victim_index
    elif policy == 'FIFO':
        oldest_time = float('inf')
        victim_index = -1
        for i, slot in enumerate(cache_set):
            if slot is not None and slot['insertion_time'] < oldest_time:
                oldest_time = slot['insertion_time']
                victim_index = i
        return victim_index
    else:
        raise ValueError("Invalid replacement policy. Use 'LRU' or 'FIFO'.")

#Access function 
def access_cache(cache, address, block_size, associativity, policy, time):
    block_number = get_block_number(address, block_size)
    num_of_sets = get_num_of_set(len(cache) * associativity * block_size, block_size, associativity)
    set_index = get_set_index(block_number, num_of_sets)
    tag = get_tag(block_number, num_of_sets)

    cache_set = cache[set_index]

    if is_hit(cache_set, tag):
        update_on_hit(cache_set, tag, time)
        return "Hit"
    else:
        empty_slot_index = find_empty_slot(cache_set)
        if empty_slot_index != -1:
            insert_block(cache_set, empty_slot_index, tag, time)
            return "Miss - Inserted"
        else:
            victim_index = find_victim(cache_set, policy)
            insert_block(cache_set, victim_index, tag, time)
            return "Miss - Replaced"

def calculate_rates(hits, misses):
    total_accesses = hits + misses
    if total_accesses == 0:
        hit_rate = 0.0
        miss_rate = 0.0 
    else:
        hit_rate = round(((hits / total_accesses)*100),2)
        miss_rate = round(((misses / total_accesses)*100),2)
    return hit_rate, miss_rate
