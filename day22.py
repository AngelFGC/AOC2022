from __future__ import annotations
from copy import deepcopy
from typing import Dict, List, Set, Tuple

def generateinstructions(instrset):
    innumber = True
    c:str
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

def day22_read():
    with open("inputs/day22.txt", mode="r+", encoding="utf-8") as f:
        ftext = f.read().split("\n\n")
        start = None
        ground = set()
        walls = set()
        
        for y,line in enumerate(ftext[0]):
            for x,c in enumerate(line):
                if c == ".":
                    ground.add((x,y))
                    if start is None:
                        start = (x,y)
                elif c == "#":
                    walls.add((x,y))

        return ground, walls, start, ftext[1]

def move(x:int, y:int, dx:int, dy:int, steps:int, mapstr:List[str]):
    new_x, new_y = x, y
    for _ in range(steps):
        new_x += dx
        new_y += dy
        if mapstr[new_x][new_y] != ".":
            new_x -= dx
            new_y -= dy
            break
    return new_x, new_y

def move_mark(x:int, y:int, dx:int, dy:int, steps:int, mapstr:List[str], mark:List[str]):
    marks = {
        (1,0):">",
        (0,1):"V",
        (-1,0):"<",
        (0,-1):"^"
    }
    new_x, new_y = x, y
    for _ in range(steps):
        new_x += dx
        new_y += dy
        if mapstr[new_y][new_x] == "#":
            new_x -= dx
            new_y -= dy
            break
        else:
            mark[new_y] = mark[new_y][:new_x] + marks[(dx, dy)] + mark[new_y][new_x+1:]

    return new_x, new_y

def movewmark(pos:Tuple[int,int], d:Tuple[int,int], steps:int, ground:Set, walls:Set) -> Dict:
    marks = {
        (1,0):">",
        (0,1):"V",
        (-1,0):"<",
        (0,-1):"^"
    }
    x,y = pos
    dx,dy = d
    dir = marks[d]
    the_moves = dict()
    for _ in range(steps):
        x += dx
        y += dy
        if (x,y) in walls:
            x -= dx
            y -= dy
            break
        elif (x,y) in ground:
            the_moves[(x,y)] = dir
        else:
            pass


def day22():
    ground, walls, start, instrset = day22_read()

    x = list()
    
    start_x = mapstr[0].index(".")
    start_y = 0
    directions = [
        [1,0],
        [0,1],
        [-1,0],
        [0,-1]
    ]
    rots = {"R":1,"L":-1}
    facing = 0
    x, y = start_x, start_y

    for instr in generateinstructions(instrset):
        if instr.isnumeric():
            # Move fwd code
            dx, dy = directions[facing]
            x, y = move_mark(x, y, dx, dy, int(instr), mapstr, mark_map)
        else:
            facing = (facing + rots[instr]) % 4

    if mark_map is not None:
        print("\n".join(mapstr))

if __name__ == "__main__":
    day22()
