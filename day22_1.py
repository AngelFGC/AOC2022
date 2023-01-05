from __future__ import annotations
from copy import deepcopy
from typing import Dict, List, Set, Tuple


def generateinstructions(instrset):
    innumber = True
    c: str
    currstr = ""
    for c in instrset:
        if c.isnumeric():
            if not innumber:
                innumber = True
            currstr += c
        else:
            if innumber:
                yield currstr
                innumber = False
                currstr = ""
            yield c
    if len(currstr) > 0:
        yield currstr


def day22_read() -> Tuple[Dict[Tuple, str], Tuple, str]:
    with open("inputs/day22.txt", mode="r+", encoding="utf-8") as f:
        ftext = f.read().split("\n\n")
        start = None
        mapd = dict()

        for y, line in enumerate(ftext[0].splitlines()):
            for x, c in enumerate(line):
                if not c.isspace():
                    mapd[(x, y)] = c
                    if start is None and c == ".":
                        start = (x, y)

        return mapd, start, ftext[1]


def movewmark(pos: Tuple[int, int], d: Tuple[int, int], steps: int, mapd: Dict[Tuple, str]) -> Tuple[Tuple, Dict]:
    marks = {
        (1, 0): ">",
        (0, 1): "V",
        (-1, 0): "<",
        (0, -1): "^"
    }
    x, y = pos
    dx, dy = d
    dir = marks[d]
    the_moves = {(x, y): dir}

    for _ in range(steps):
        x += dx
        y += dy
        if (x, y) in mapd:
            if mapd[(x, y)] == "#":
                x -= dx
                y -= dy
                break
            elif mapd[(x, y)] == ".":
                the_moves[(x, y)] = dir
        else:
            src_x, src_y = x, y
            minx = maxx = miny = maxy = 0
            all_x = all_y = None
            if dy == 0:
                all_x = {i for (i, j) in mapd if y == j}
                minx, maxx = min(all_x), max(all_x)
            if dx == 0:
                all_y = {j for (i, j) in mapd if x == i}
                miny, maxy = min(all_y), max(all_y)

            while (x, y) not in mapd:
                x, y = x+dx, y+dy
                if dx == 0:
                    y = (maxy if y < miny else
                         miny if y > maxy else y)
                if dy == 0:
                    x = (maxx if x < minx else
                         minx if x > maxx else x)
            if mapd[(x, y)] != ".":
                x = src_x - dx
                y = src_y - dy
                break
            else:
                the_moves[(x, y)] = dir

    return (x, y), the_moves


def printmap(mapd: Dict, moves: Dict):
    maxx = max(x for (x, _) in mapd)
    maxy = max(y for (_, y) in mapd)

    for y in range(maxy+1):
        for x in range(maxx+1):
            if (x, y) in moves:
                print(moves[(x, y)], end="")
            elif (x, y) in mapd:
                print(mapd[(x, y)], end="")
            else:
                print(" ", end="")
        print("")


def day22():
    mapd, start, instrset = day22_read()

    x = list()

    directions = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1]
    ]
    rots = {"R": 1, "L": -1}
    facing = 0
    x, y = start

    the_moves = dict()

    for instr in generateinstructions(instrset):
        if instr.isnumeric():
            dx, dy = directions[facing]
            (x, y), newmoves = movewmark((x, y), (dx, dy), int(instr), mapd)
            the_moves.update(newmoves)
        else:
            facing = (facing + rots[instr]) % 4

    #printmap(mapd, the_moves)
    c, r, f = x+1, y+1, facing

    print(f"Row: {r}, Column: {c}, Facing: {f}")
    print(1000*r + 4*c + f)

if __name__ == "__main__":
    day22()
