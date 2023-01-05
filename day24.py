from __future__ import annotations
from copy import deepcopy
from functools import cache
from typing import Dict, List, Set, Tuple, Iterable, Any
from dataclasses import dataclass, field
from collections import deque
import itertools

import heapq

dirfns = {
    ">": lambda self: (self.x+1, self.y),
    "<": lambda self: (self.x-1, self.y),
    "^": lambda self: (self.x, self.y-1),
    "v": lambda self: (self.x, self.y+1)
}

dirfnsC = {
    "E": lambda x,y: (x+1, y),
    "W": lambda x,y: (x-1, y),
    "N": lambda x,y: (x, y-1),
    "S": lambda x,y: (x, y+1),
    "-": lambda x,y: (x, y)
}

@dataclass(unsafe_hash=True)
class Blizzard(object):
    dir: str
    x: int
    y: int
    wallx: int
    wally: int

    def nextpos(self) -> Tuple[Pos]:
        nx, ny = dirfns[self.dir](self)
        if nx == 0:
            nx = self.wallx - 1
        if nx == self.wallx:
            nx = 1
        if ny == 0:
            ny = self.wally - 1
        if ny == self.wally:
            ny = 1
        return nx, ny

    def move(self):
        self.x, self.y = self.nextpos()


Pos = Tuple[int, int]

def day24_read() -> Tuple[int, int, Pos, Pos, Tuple[Blizzard]]:
    blizzards_raw = list()
    start = None
    end = None
    with open("inputs/day24.txt", mode="r+", encoding="utf-8") as f:
        for row, line in enumerate(f.readlines()):
            for col, c in enumerate(line.strip()):
                if c == ".":
                    end = (col, row)
                    if start is None:
                        start = end
                elif c != "#":
                    blizzards_raw.append((c, col, row))
    xub, yub = col, row
    blizzs = [Blizzard(c, col, row, xub, yub)
              for c, col, row in blizzards_raw]
    return xub, yub, start, end, tuple(blizzs)

@cache
def next_blizzards(blizz: Tuple[Blizzard]) -> Set[Pos]:
    return {p.nextpos() for p in blizz}

@cache
def generate_moves(me:Pos, lims:Pos, start:Pos, end:Pos, blizzards:Tuple[Blizzard]) -> List[Pos]:
    x,y = me
    limx, limy = lims
    newpos = [dirfnsC[d](x, y) for d in dirfnsC]
    newblizz = next_blizzards(blizzards)
    return [
        (x, y) for (x,y) in newpos 
        if (x,y) == start or (x,y) == end or
        ((x,y) not in newblizz and 
        x > 0 and x < limx and 
        y > 0 and y < limy)
    ]

def generate_all_states(blizzards:Tuple[Blizzard]) -> List[Set[Pos]]:
    all_states:List[Tuple[Pos]] = list()
    curr = set((b.x, b.y) for b in blizzards)
    while curr not in all_states:
        all_states.append(curr)
        for b in blizzards:
            b.move()
        curr = set((b.x, b.y) for b in blizzards)

    return all_states

@dataclass(eq=True, order=True, unsafe_hash=True)
class PosPrioritized(object):
    priority:int
    data:Any = field(compare=False, hash=True)

def createvertices(x_max:int, y_max:int) -> Set[Pos]:
    return {(x,y) for (x,y) in itertools.product(range(1, x_max), range(1, y_max))}

def day24():
    x_max, y_max, start, end, blizzards = day24_read()
    all_blizz = generate_all_states(blizzards)
    n = len(all_blizz)
    print(n)
    vertices = createvertices(x_max, y_max)

    v_set:Dict[Pos,PosPrioritized] = dict()
    pq = list()

    init_node = (start[0], start[1], 0)
    visited = set()

    init_ptzed = PosPrioritized(0, init_node)
    pq.append(init_ptzed)

    distances = dict()
    nodes = dict()

    while pq:
        ptzed = heapq.heappop(pq)
        dist = ptzed.priority
        node = ptzed.data
        x,y,t = node

        if (x,y) == end:
            print(t)
            break

        neighbors = [
            (x + dx, y + dy, t + 1)
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1), (0,0))
            if (x + dx, y + dy) == start
            or (x + dx, y + dy) == end
            or (
                0 < x + dx < x_max 
                and 0 < y + dy < y_max 
                and (x + dx, y + dy) not in all_blizz[(t + 1) % n]
            )
        ]
        for neigh in neighbors:
            new_dist = dist + 2
            if neigh not in visited:
                if neigh not in distances:
                    distances[neigh] = new_dist
                    nodes[neigh] = PosPrioritized(new_dist, neigh)
                    heapq.heappush(pq, nodes[neigh])
                else:
                    distances[neigh] = min(distances[neigh], new_dist)
                    nodes[neigh].priority = distances[neigh]
        heapq.heapify(pq)
        visited.add(node)


    # dist is based on t
    print(f"{x_max}, {y_max}")


def shortestpath(start:Pos, end:Pos, t0:int, x_max:int, y_max:int, all_blizz:List[Set[Pos]]):
    n = len(all_blizz)
    pq = list()
    init_node = (start[0], start[1], t0)
    visited = set()

    init_ptzed = PosPrioritized(0, init_node)
    pq.append(init_ptzed)

    distances = dict()
    nodes = dict()

    while pq:
        ptzed = heapq.heappop(pq)
        dist = ptzed.priority
        node = ptzed.data
        x,y,t = node

        if (x,y) == end:
            return t

        neighbors = [
            (x + dx, y + dy, t + 1)
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1), (0,0))
            if (x + dx, y + dy) == start
            or (x + dx, y + dy) == end
            or (
                0 < x + dx < x_max 
                and 0 < y + dy < y_max 
                and (x + dx, y + dy) not in all_blizz[(t + 1) % n]
            )
        ]
        for neigh in neighbors:
            new_dist = dist + 2
            if neigh not in visited:
                if neigh not in distances:
                    distances[neigh] = new_dist
                    nodes[neigh] = PosPrioritized(new_dist, neigh)
                    heapq.heappush(pq, nodes[neigh])
                else:
                    distances[neigh] = min(distances[neigh], new_dist)
                    nodes[neigh].priority = distances[neigh]
        heapq.heapify(pq)
        visited.add(node)

def day24_1():
    x_max, y_max, start, end, blizzards = day24_read()
    all_blizz = generate_all_states(blizzards)
    
    t0 = shortestpath(start, end, 0, x_max, y_max, all_blizz)

    print(t0)

def day24_2():
    x_max, y_max, start, end, blizzards = day24_read()
    all_blizz = generate_all_states(blizzards)
    t0 = 0
    print(t0)
    t1 = shortestpath(start, end, t0, x_max, y_max, all_blizz)
    print(t1)
    t2 = shortestpath(end, start, t1, x_max, y_max, all_blizz)
    print(t2)
    t3 = shortestpath(start, end, t2, x_max, y_max, all_blizz)
    print(t3)


if __name__ == "__main__":
    day24_2()
