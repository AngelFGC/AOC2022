import itertools

from tqdm import tqdm
from typing import List, Set, Tuple

def generate_line(x1:int, y1:int, x2:int, y2:int) -> Set:
    line = set()
    if x1 == x2:
        if y1 > y2: y1, y2 = y2, y1
        line.update((x1, y) for y in range(y1, y2+1))
    else:
        if x1 > x2: x1, x2 = x2, x1
        line.update((x, y1) for x in range(x1, x2+1))
    return line

def read_day14() -> Set:
    maxdepth = 0

    all_surfaces = set()
    with open("inputs/day14.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            structure = line.split(" -> ")
            structure = [tuple(map(int,s.split(","))) for s in structure]
            
            for i in range(1, len(structure)):
                x1, y1 = structure[i - 1]
                x2, y2 = structure[i]

                maxdepth = max(maxdepth, y1, y2)

                all_surfaces.update(generate_line(x1, y1, x2, y2))
    
    return maxdepth, all_surfaces

def generate_new_pos(pos:List) -> List[Tuple]:
    x,y = pos
    return [[x + dx, y + 1] for dx in [-1, 0, 1]]

def falling_grain_into_abyss(start:Tuple, surfaces:Set, maxdepth:int) -> bool:
    grain = list(start)
    while True:
        # Always Size 5
        # new_pos[:2] are left diagonal
        # new_pos[2] is straight down
        # new_pos[3:] are right diagonal
        new_pos = generate_new_pos(grain)
        
        if new_pos[1][1] > maxdepth:
            # Falling into the Abyss
            return True
        else:
            updated = False
            for i in [1,0,2]:
                if tuple(new_pos[i]) not in surfaces:
                    grain[:], updated = new_pos[i][:], True
                    break
            if not updated:
                # All paths are blocked -> Stay
                surfaces.add(tuple(grain))
                return False

def simulate_sand_into_abyss(surfaces:Set, maxdepth:int) -> int:
    origin_point = (500, 0)
    
    for i in itertools.count(1):
        if falling_grain_into_abyss(origin_point, surfaces, maxdepth):
            break
    
    return i - 1

def falling_grain_into_ground(start:Tuple, surfaces:Set, maxdepth:int) -> None:
    grain = list(start)
    while True:
        # Always Size 5
        # new_pos[:2] are left diagonal
        # new_pos[2] is straight down
        # new_pos[3:] are right diagonal
        new_pos = generate_new_pos(grain)
        
        if new_pos[1][1] > maxdepth + 1:
            # Falling into the ground
            surfaces.add(tuple(grain))
            break
        else:
            updated = False
            for i in [1,0,2]:
                if tuple(new_pos[i]) not in surfaces:
                    grain[:], updated = new_pos[i][:], True
                    break
            if not updated:
                # All paths are blocked -> Stay
                surfaces.add(tuple(grain))
                break

def simulate_sand_into_ground(surfaces:Set, maxdepth:int) -> int:
    origin_point = (500, 0)
    
    for i in itertools.count(1):
        falling_grain_into_ground(origin_point, surfaces, maxdepth)
        if origin_point in surfaces:
            break
    
    return i

def generate_line_c(x1, y1, x2, y2) -> Set[complex]:
    line = set()
    if x1 == x2:
        if y1 > y2: y1, y2 = y2, y1
        line.update(complex(x1, y) for y in range(y1, y2+1))
    else:
        if x1 > x2: x1, x2 = x2, x1
        line.update(complex(x, y1) for x in range(x1, x2+1))
    return line

def read_day14_c() -> Set[complex]:
    maxdepth = 0

    all_surfaces = set()
    with open("inputs/day14.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            structure = line.split(" -> ")
            structure = [tuple(map(int,s.split(","))) for s in structure]
            
            for i in range(1, len(structure)):
                x1, y1 = structure[i - 1]
                x2, y2 = structure[i]

                all_surfaces.update(generate_line_c(x1, y1, x2, y2))
    
    return max(c.imag for c in all_surfaces), all_surfaces

def falling_grain_into_ground_c(start:complex, surfaces:Set, maxdepth:int) -> None:
    grain = start
    while True:
        if grain.imag == maxdepth + 1:
            # Falling into the ground
            surfaces.add(grain)
            break
        else:
            updated = False
            for npos in (grain + complex(dx, 1) for dx in [0, -1, 1]):
                if npos not in surfaces:
                    grain, updated = npos, True
                    break
            if not updated:
                # All paths are blocked -> Stay
                surfaces.add(grain)
                break

def simulate_sand_into_ground_c(surfaces:Set, maxdepth:int) -> int:
    origin_point = complex(500, 0)
    
    for i in itertools.count(1):
        falling_grain_into_ground_c(origin_point, surfaces, maxdepth)
        if origin_point in surfaces: break
    
    return i

def falling_grain_into_ground_m(path:List[Tuple], surfaces:Set, maxdepth:int) -> None:
    while True:
        new_pos = [[path[-1][0] + dx, path[-1][1] + 1] for dx in [0, -1, 1]]
        
        if new_pos[1][1] > maxdepth + 1:
            # Falling into the ground
            surfaces.add(tuple(path.pop()))
            break
        else:
            updated = False
            for pos in new_pos:
                if tuple(pos) not in surfaces:
                    path.append(pos)
                    updated = True
                    break
            if not updated:
                # All paths are blocked -> Stay
                surfaces.add(tuple(path.pop()))
                break

def simulate_sand_into_ground_m(surfaces:Set, maxdepth:int) -> int:
    origin_point = (500, 0)
    sand_path = [list(origin_point)]
    for i in itertools.count(1):
        falling_grain_into_ground_m(sand_path, surfaces, maxdepth)
        if origin_point in surfaces:
            break
    
    return i

def day14():
    maxdepth, surfaces = read_day14()
    simulate_sand_into_ground(surfaces, maxdepth)
    
def day14_c():
    maxdepth, surfaces = read_day14_c()
    simulate_sand_into_ground_c(surfaces, maxdepth)

def day14_m():
    maxdepth, surfaces = read_day14() # MUCH faster (memoization)
    simulate_sand_into_ground_m(surfaces, maxdepth)


if __name__ == "__main__":
    day14_m()