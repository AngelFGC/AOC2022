
import re
from typing import List, Tuple

def get_ranges() -> List[Tuple]:
    ranges = []
    re_patt = re.compile(r"(\d+)\-(\d+),(\d+)\-(\d+)")
    with open("aoc2022/day4.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            match = re_patt.fullmatch(line.strip())
            full = tuple(int(match.group(i)) for i in range(1,5))
            ranges.append(full)
    return ranges

def check_range_inclusion(ranges:Tuple) -> int:
    cnt = 0
    for a, b, x, y in ranges:
        if (a <= x <= y <= b) or (x <= a <= b <= y):
            cnt += 1
    return cnt

def check_overlap(ranges:Tuple) -> int:
    cnt = 0
    for a, b, x, y in ranges:
        if (a <= x <= b) or (x <= a <= y):
            cnt += 1
    return cnt

def day4():
    ranges = get_ranges()
    print(check_range_inclusion(ranges))
    print(check_overlap(ranges))

if __name__ == "__main__":
    day4()