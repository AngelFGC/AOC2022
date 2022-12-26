from typing import List, Set, Tuple

def read_day18():
    with open("inputs/day18.txt", mode="r+", encoding="utf-8") as f:
        return [tuple(int(c) for c in s.strip().split(",")) for s in f]

def generate_contiguous(cube:Tuple):
    for d in [-1, 1]:
        for i in range(3):
            yield tuple((cube[k] + d if k == i else cube[k])
                     for k in range(3))

def day18_p1():
    cubes = read_day18()
    total_surfaces = len(cubes) * 6

    for pivot in cubes:
        for neighbor in generate_contiguous(pivot):
            if neighbor in cubes:
                total_surfaces -= 1

    print(total_surfaces)

def find_max(cubes:Set[Tuple]):
    max = [-1] * 3

    for cube in cubes:
        max[:] = (cube[i] if max[i] < cube[i] else max[i] for i in range(3))
    
    return tuple(i+1 for i in max)

def in_bounds(cube:Tuple, boundaries:List):
    return all(boundaries[0][i] <= cube[i] <= boundaries[1][i] for i in range(3))

def day18_p2():
    cubes = set(read_day18())
    
    boundaries = [(-1, -1, -1), find_max(cubes)]

    air = set()
    latest_air = set()
    latest_air.add((0,0,0))

    while latest_air:
        air_to_gen = latest_air.copy()
        latest_air.clear()
        for cube in air_to_gen:
            latest_air.update(c for c in generate_contiguous(cube)
                if in_bounds(c, boundaries) and c not in air and 
                    c not in latest_air and c not in cubes)
        air.update(air_to_gen)
    
    all_cubes = set(
        (x,y,z) for x in range(boundaries[0][0], boundaries[1][0]+1)
            for y in range(boundaries[0][1], boundaries[1][1]+1)
            for z in range(boundaries[0][2], boundaries[1][2]+1)
    )

    all_cubes.difference_update(air)

    total_surfaces = len(all_cubes) * 6

    for pivot in all_cubes:
        for neighbor in generate_contiguous(pivot):
            if neighbor in all_cubes:
                total_surfaces -= 1

    print(total_surfaces)
    

if __name__ == "__main__":
    #day18_p1()
    day18_p2()