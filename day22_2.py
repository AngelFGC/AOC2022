from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

import itertools

Position = Tuple[int, int]

@dataclass
class Face(object):
    name: Position
    neighbors: List[Face] = field(default_factory=lambda: [None]*4, init=False, hash=False, repr=False)
    chksum: int = field(default=None, init=False)

    @property
    def left(self):
        return self.neighbors[2]
    @left.setter
    def left(self, x:Position):
        self.neighbors[2] = x
    
    @property
    def right(self):
        return self.neighbors[0]
    @right.setter
    def right(self, x:Position):
        self.neighbors[0] = x
    
    @property
    def down(self):
        return self.neighbors[1]
    @down.setter
    def down(self, x:Position):
        self.neighbors[1] = x
    
    @property
    def up(self):
        return self.neighbors[3]
    @up.setter
    def up(self, x:Position):
        self.neighbors[3] = x


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

def getcubesize(mapd: Dict):
    start_y = 0
    start_x = min(x for (x, y) in mapd if y == start_y)
    x, y = start_x, start_y

    while (x, y) in mapd and (x, start_y) in mapd and (start_x, y) in mapd:
        x += 1
        y += 1

    return y

def generate_graph(mapd: Dict[Tuple, str], side: int, maxx: int, maxy: int):
    faces = {
        (x,y):[
            (x + dx, y + dy) if (x + dx, y + dy) in mapd else None
            for (dx, dy) in [(side, 0), (0, side), (-side, 0), (0, -side)]
        ]
        for x in range(0, maxx, side) for y in range(0, maxy, side) if (x,y) in mapd
    }
    return faces

def generate_graph2(mapd: Dict[Position, str], side: int, maxx: int, maxy: int) -> Dict[Position,Face]:
    faces:Dict[Position,Face] = {}
    for x,y in itertools.product(range(0, maxx, side), range(0, maxy, side)):
        if (x,y) in mapd:
            f = Face((x,y))
            faces[f.name] = f
    for x,y in faces:
        faces[(x,y)].neighbors = [
            faces[(x + dx, y + dy)] if (x + dx, y + dy) in faces else None
            for (dx, dy) in [(side, 0), (0, side), (-side, 0), (0, -side)]
        ]
    return faces

def get_checksums(faces:Dict[Position,Face]):
    faces_sums = [None]*6

    for t in faces:
        if None not in faces_sums:
            break
        face = faces[t]
        if face in faces_sums:
            continue
        next_idx = faces_sums.index(None)
        face.chksum = next_idx
        faces_sums[next_idx] = face
        for i in range(4):
            if face.neighbors[i] is not None and face.neighbors[i].neighbors[i] is not None:
                face.neighbors[i].neighbors[i].chksum = 5 - next_idx
                faces_sums[5 - next_idx] = face.neighbors[i].neighbors[i]
    
    for i, face in enumerate(faces_sums):
        print(f"{i}: {face.name if face is not None else None}")

def day22_2():
    mapd, start, instrset = day22_read()
    side = getcubesize(mapd)
    limit_x, limit_y = max(x for (x, _) in mapd), max(y for (_, y) in mapd)
    c_x = (limit_x + 1) // side
    c_y = (limit_y + 1) // side

    print(f"limits: {limit_x + 1}, {limit_y + 1} ({side})")

    graph = generate_graph2(mapd, side, limit_x, limit_y)
    get_checksums(graph)

if __name__ == "__main__":
    day22_2()
