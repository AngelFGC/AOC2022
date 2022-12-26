from typing import List

def get_priority(letter:str) -> int:
    l_value = ord(letter)
    if l_value >= 97:
        return l_value - 96
    else:
        return l_value - 38

def get_rucksacks_raw() -> List[str]:
    with open("aoc2022/day3.txt", mode="r+", encoding="utf-8") as f:
        return [x.strip() for x in f.readlines()]

def get_rucksack_diffs(rucksacks:List[str]) -> int:
    for r in rucksacks:
        i = len(r) // 2
        common = set(r[:i]) & set(r[i:])
        yield get_priority(common.pop())

def get_rucksack_badges(rucksacks:List[str]) -> int:
    for i in range(0,len(rucksacks),3):
        common = set(rucksacks[i]) & set(rucksacks[i+1]) & set(rucksacks[i+2])
        yield get_priority(common.pop())

def day3():
    rucksacks = get_rucksacks_raw()
    print(sum(d for d in get_rucksack_diffs(rucksacks)))
    print(sum(d for d in get_rucksack_badges(rucksacks)))

if __name__ == "__main__":
    day3()