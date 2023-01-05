from __future__ import annotations
from copy import deepcopy
from typing import Dict, List, Set, Tuple, Iterable, Any

import itertools

Elf = Tuple[int, int]
directions = {"N": (0,-1), "S": (0,1), "W": (-1,0), "E": (1,0)}
areacheck = {
    "N": [(0,-1),(1,-1),(-1,-1)],
    "S": [(0,1),(1,1),(-1,1)],
    "W": [(-1,0),(-1,1),(-1,-1)],
    "E": [(1,0),(1,1),(1,-1)]
}

def minmnax(it:Iterable[Any]) -> Tuple[Any, Any]:
    mn = mx = None
    for u in it:
        if mn is None:
            mn = mx = u
        else:
            mn = min(mn, u)
            mx = max(mx, u)
    return mn, mx

def day23_read() -> List[Elf]:
    elves: List[Elf] = list()
    with open("inputs/day23.txt", mode="r+", encoding="utf-8") as f:
        for row, line in enumerate(f.readlines()):
            for col, c in enumerate(line.strip()):
                if c == "#":
                    elves.append((col, row))
    return elves

def proposedirection(elf:Elf, elves:List[Elf], order:List[str]) -> Elf:
    elves_set = set(elves)
    x,y = elf
    alone = True
    for dx,dy in itertools.product((-1,0,1), repeat=2):
        if dx == dy == 0:
            continue
        else:
            if (x + dx, y + dy) in elves_set:
                alone = False
                break
    
    if alone:
        return elf

    for d in order:
        d_has_elf = False
        for dx, dy in areacheck[d]:
            if (x + dx, y + dy) in elves_set:
                d_has_elf = True
                break
        if not d_has_elf:
            return (x + directions[d][0], y + directions[d][1])
    return elf

def resolvecollisions(oldelves:List[Elf], newelves:List[Elf]):
    reverse_elves = dict()

    for i,e in enumerate(newelves):
        if e not in reverse_elves:
            reverse_elves[e] = [i]
        else:
            reverse_elves[e].append(i)
    
    for i,e in enumerate(newelves):
        test = reverse_elves[e]
        if len(test) > 1:
            newelves[i] = oldelves[i]

def printmap(elves):
    xlb, xub = minmnax(x for x, _ in elves)
    ylb, yub = minmnax(y for _, y in elves)
    e_set = set(elves)
    s = ""
    for y in range(ylb, yub + 1):
        for x in range(xlb, xub + 1):
            if (x,y) in e_set:
                s += "#"
            else:
                s += "."
        s += "\n"
    print(s)

def day23():
    elves = day23_read()
    # printmap(elves)
    # print()
    order = [c for c in "NSWE"]
    new_elves = None

    #while elves != new_elves:
    for _ in range(10):
        if new_elves is not None:
            elves = new_elves
        # First stage: Propose
        new_elves = [
            proposedirection(elf, elves, order)
            for elf in elves
        ]
        # Second half:
        resolvecollisions(elves, new_elves)
        # Get Rotated
        order[:] = order[1:] + order[:1]
        #printmap(new_elves)
        #print()
    elves = new_elves

    xlb, xub = minmnax(x for x, _ in elves)
    ylb, yub = minmnax(y for _, y in elves)

    area = (xub - xlb + 1) * (yub - ylb + 1)
    
    #print(elves)
    print(area - len(elves))
    printmap(elves)

def day23():
    elves = day23_read()
    # printmap(elves)
    # print()
    order = [c for c in "NSWE"]
    new_elves = None

    #while elves != new_elves:
    for i in itertools.count(1):
        if new_elves is not None:
            elves = new_elves
        # First stage: Propose
        new_elves = [
            proposedirection(elf, elves, order)
            for elf in elves
        ]
        # Second half:
        resolvecollisions(elves, new_elves)
        # Get Rotated
        order[:] = order[1:] + order[:1]
        #printmap(new_elves)
        #print()
        if new_elves == elves:
            break
    
    print(i)

if __name__ == "__main__":
    day23()
