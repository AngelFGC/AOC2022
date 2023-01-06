from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

import itertools

Pos = Tuple[int, int]

def day22_read() -> Tuple[Dict[Pos, str], Pos, str]:
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

def getcubesize(mapd: Dict):
    start_y = 0
    start_x = min(x for (x, y) in mapd if y == start_y)
    x, y = start_x, start_y

    while (x, y) in mapd and (x, start_y) in mapd and (start_x, y) in mapd:
        x += 1
        y += 1

    return y

def orthogonal_conv(dir:Pos) -> Pos:
    return (-dir[1], dir[0])

def orthogonal_conc(dir:Pos) -> Pos:
    return (dir[1], -dir[0])

def get_conv_checker(dir:Pos) -> Pos:
    x0,y0 = dir
    x1,y1 = orthogonal_conv(dir)
    x,y = x0 + x1, y0 + y1
    return (x,y)

def get_conc_checker(dir:Pos) -> Pos:
    x0,y0 = dir
    x1,y1 = orthogonal_conc(dir)
    x,y = x0 + x1, y0 + y1
    return (x,y)

def cw_walkgen(mapd:Dict[Pos, str], start:Pos, init_dir:Pos) -> Pos:
    dir = init_dir
    checker = get_conv_checker(dir)
    orthog = orthogonal_conc(dir)

    walker = [start[0] + orthog[0], start[1] + orthog[1]]
    #walker = [start[0], start[1]-1]

    wall = (walker[0] + dir[0], walker[1] + dir[1])
    ground = (walker[0] + checker[0], walker[1] + checker[1])
    while ground != start:
        yield tuple(walker)
        wall = (walker[0] + dir[0], walker[1] + dir[1])
        ground = (walker[0] + checker[0], walker[1] + checker[1])
        if wall in mapd:
            # Check for wall
            dir = orthogonal_conc(dir)
            checker = get_conv_checker(dir)
            walker[0] += dir[0]
            walker[1] += dir[1]
        elif ground not in mapd:
            # Else, check for cliff
            # Ground is our next position!
            walker[:] = ground[:]
            dir = orthogonal_conv(dir)
            checker = get_conv_checker(dir)
        else:
            # If no wall or cliff, we can move fwd
            walker[0] += dir[0]
            walker[1] += dir[1]
    yield tuple(walker)

def ccw_walkgen(mapd:Dict[Pos, str], start:Pos, init_dir:Pos) -> Pos:
    dir = init_dir
    checker = get_conc_checker(dir)
    orthog = orthogonal_conv(dir)

    walker = [start[0] + orthog[0], start[1] + orthog[1]]
    #walker = [start[0], start[1]-1]
    
    wall = (walker[0] + dir[0], walker[1] + dir[1])
    ground = (walker[0] + checker[0], walker[1] + checker[1])

    while ground != start:
        yield tuple(walker)
        wall = (walker[0] + dir[0], walker[1] + dir[1])
        ground = (walker[0] + checker[0], walker[1] + checker[1])
        if wall in mapd:
            # Check for wall
            dir = orthogonal_conv(dir)
            checker = get_conc_checker(dir)
            walker[0] += dir[0]
            walker[1] += dir[1]
        elif ground not in mapd:
            # Else, check for cliff
            # Ground is our next position!
            walker[:] = ground[:]
            dir = orthogonal_conc(dir)
            checker = get_conc_checker(dir)
        else:
            # If no wall or cliff, we can move fwd
            walker[0] += dir[0]
            walker[1] += dir[1]
    yield tuple(walker)

def walkcwalongedge(mapd: Dict[Pos, str]) -> Set[Pos]:
    start = (0,0)
    for i in itertools.count(0):
        if (i,0) in mapd:
            start = (i,0)
            break
    steps = set()
    dir = (1,0)

    return {t for t in cw_walkgen(mapd, start, dir)}

def walkccwalongedge(mapd: Dict[Pos, str]) -> Set[Pos]:
    start = (0,0)
    in_map = False
    for i in itertools.count(0):
        if (i,0) in mapd and not in_map:
            in_map = True
        elif in_map and (i,0) not in mapd:
            start = (i-1,0)
            break
    steps = set()
    dir = (-1,0)

    return {t for t in ccw_walkgen(mapd, start, dir)}

def concavecornergen(mapd:Dict[Pos, str]) -> Tuple[Pos,Pos]:
    posset = set(mapd.keys())
    start = (0,0)
    for i in itertools.count(0):
        if (i,0) in mapd:
            start = (i,0)
            break
    steps = set()
    dir = (1,0)

    for edge in cw_walkgen(mapd, start, dir):
        neighbors = {
            (edge[0] + x, edge[1] + y)
            for x,y in itertools.product((-1,1), repeat=2)
        }
        notshared = neighbors.difference(posset)
        if len(notshared) == 1:
            # We found a corner!
            external = notshared.pop()
            internal = (2*edge[0] - external[0], 2*edge[1] - external[1])
            yield internal, edge

def doublewalk(mapd:Dict[Pos, str], corner:Pos, edge:Pos):
    dx, dy = edge[0] - corner[0],  edge[1] - corner[1]
    dir1 = dir2 = tuple()
    if dx == dy:
        dir1 = (0, dy)
        dir2 = (dx, 0)
    else:
        dir1 = (dx, 0)
        dir2 = (0, dy)

    start1 = (corner[0] + dir1[0], corner[1] + dir1[1])
    start2 = (corner[0] + dir2[0], corner[1] + dir2[1])

    for walker1, walker2 in zip(
        cw_walkgen(mapd, start1, dir1),
        ccw_walkgen(mapd, start2, dir2)
    ):
        print(f"{walker1} + {walker2}")

def printwithedges(mapd:Dict[Pos, str], edges:Set[Pos], xub:int, yub:int) -> None:
    s = ""
    for row in range(-1, yub+2):
        for col in range(-1, xub+2):
            if (col,row) in edges:
                s += "@"
            elif (col,row) in mapd:
                s += mapd[(col,row)]
            else:
                s += " "
        s += "\n"
    print(s)

def day22_2():
    mapd, start, instrset = day22_read()
    side = getcubesize(mapd)
    limit_x, limit_y = max(x for (x, _) in mapd), max(y for (_, y) in mapd)
    c_x = (limit_x + 1) // side
    c_y = (limit_y + 1) // side

    print(f"limits: {limit_x + 1}, {limit_y + 1} ({side})")

    #outedges = walkcwalongedge(mapd)

    #outedges2 = walkccwalongedge(mapd)
    outedges = set()

    for internal,external in concavecornergen(mapd):
        doublewalk(mapd, internal, external)

    printwithedges(mapd, outedges, limit_x, limit_y)

if __name__ == "__main__":
    day22_2()
