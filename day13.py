import functools

from tqdm import tqdm
from typing import List

def read_day13():
    pairs = []
    curr_pair_left = None
    with open("inputs/day13.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "":
                continue
            elif curr_pair_left is None:
                curr_pair_left = eval(line.strip())
            else:
                pairs.append((curr_pair_left, eval(line.strip())))
                curr_pair_left = None
    return pairs

def compare_pair(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left < right: return 1
        elif left > right: return -1
        else: return 0
    elif isinstance(left, int):
        return compare_pair([left], right)
    elif isinstance(right, int):
        return compare_pair(left, [right])
    else:
        i = 0
        for i in range(min(len(left), len(right))):
            comp = compare_pair(left[i], right[i])
            if comp == 1: return 1
            elif comp == -1: return -1
        
        if len(left) < len(right): return 1
        elif len(left) > len(right): return -1
        else: return 0

def compare_all_pairs(pairs:List):
    ordered = set()
    for i, (left, right) in enumerate(pairs):
        in_order = compare_pair(left, right)
        if in_order == 1:
            ordered.add(i+1)
    print(sum(ordered))

def sort_all_pairs(pairs:List):
    unpaired = []
    key1 = [[2]]
    key2 = [[6]]
    for L,R in pairs:
        unpaired.append(L)
        unpaired.append(R)
    unpaired.append(key1)
    unpaired.append(key2)
    sorted_unpaired = sorted(unpaired, reverse=True,
            key=functools.cmp_to_key(compare_pair))

    print("\n".join(str(line) for line in sorted_unpaired))

    idx1 = sorted_unpaired.index(key1) + 1
    idx2 = sorted_unpaired.index(key2) + 1

    print(f"{idx1} x {idx2} = {idx1*idx2}")

def day13():
    pairs = read_day13()
    # compare_all_pairs(pairs)
    sort_all_pairs(pairs)

if __name__ == "__main__":
    day13()