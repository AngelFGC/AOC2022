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

def generate_all_states(blizzards:Tuple[Blizzard]) ->List[Tuple[Pos]]:
    all_states:List[Tuple[Pos]] = list()
    curr = tuple((b.x, b.y) for b in blizzards)
    while curr not in all_states:
        all_states.append(curr)
        for b in blizzards:
            b.move()
        curr = tuple((b.x, b.y) for b in blizzards)

    return all_states

@dataclass(eq=True, order=True)
class PosPrioritized(object):
    priority:int
    data:Any = field(compare=False)

def day24():
    x_max, y_max, start, end, blizzards = day24_read()
    all_states = generate_all_states(blizzards)
    n = len(all_states)
    print(n)

    pos = start
    visited = set()
    distances = dict()
    t = 0
    distances[pos] = 0
    base = (t, pos)

    xyz = PosPrioritized(t, pos)

    pq = [xyz]
    allpos = {pos:xyz}
    heapq.heapify(pq)

    while pq:
        heapobj = heapq.heappop(pq)
        t, pos = heapobj.priority, heapobj.data
        t = t+1
        bs = all_states[t % n]
        neighbors = [
            (pos[0] + dx, pos[1] + dy)
            for dx,dy in ((0,0),(0,-1),(1,0),(0,1),(-1,0))
            if (pos[0] + dx, pos[1] + dy) == start or
            (pos[0] + dx, pos[1] + dy) == end or
            (0 < pos[0] + dx < x_max and 0 < pos[1] + dy < y_max
            and pos not in bs)
        ]
        for pos_ns in neighbors:
            if pos_ns not in distances:
                distances[pos_ns] = t
            else:
                distances[pos_ns] = min(distances[pos_ns], t)
            if pos_ns in allpos:
                allpos[pos_ns].priority = min(allpos[pos_ns].priority, t)

        


    



    # x_max, y_max, start, end, blizzards = day24_read()
    # depth = 0
    # q = deque()
    # q.append((depth + 1, start))

    # while len(q) > 0:
    #     d2, p = q.popleft()
    #     if d2 > depth:
    #         for b in blizzards:
    #             b.move()
    #         depth = d2
    #     nextmoves = generate_moves(p, (x_max, y_max), start, end, blizzards)
    #     if end in nextmoves:
    #         break
    #     q.extend((depth + 1, p2) for p2 in nextmoves)

    # print(depth + 1)

if __name__ == "__main__":
    day24()
