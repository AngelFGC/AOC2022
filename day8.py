from typing import List, Set


def read_map() -> List[List]:
    with open("inputs/day8.txt", mode="r+", encoding="utf-8") as f:
        line_gen = (s.strip() for s in f)
        return [[int(cr) for cr in line] for line in line_gen]

def eval_level_rows(forest_map:List[List], limit:int) -> Set:
    heatmap = set()
    for i, row in enumerate(forest_map):
        if i == 0 or i == len(forest_map) - 1:
            continue
        L, R = 0, len(row) - 1
        # From the Left
        while L < len(row) and row[L] < limit:
            L += 1
        # And from the Right
        while R >= 0 and row[R] < limit:
            R -= 1
        # Add if not on edge
        if L > 0 and L < len(row) - 1:
            heatmap.add((i, L))
        if L != R and R > 0 and R < len(row) - 1:
            heatmap.add((i, R))
            
    return heatmap

def eval_level_cols(forest_map:List[List], limit:int) -> Set:
    heatmap = set()
    for j in range(len(forest_map[0])):
        if j == 0 or j == len(forest_map[0]) - 1:
            continue
        U, D = 0, len(forest_map) - 1
        # From Up
        while U < len(forest_map) and forest_map[U][j] < limit:
            U += 1
        # And from Down
        while D >= 0 and forest_map[D][j] < limit: 
            D -= 1
        # Add if not on edge
        if U > 0 and U < len(forest_map) - 1:
            heatmap.add((U, j))
        if U != D and D > 0 and D < len(forest_map) - 1:
            heatmap.add((D, j))
            
    return heatmap

def get_vismap(forest_map:List[List]) -> Set:
    vismap = set()

    for limit in range(10):
        # Eval Rows
        vismap.update(eval_level_rows(forest_map, limit))
        vismap.update(eval_level_cols(forest_map, limit))

    return vismap
    
def part1(forest_map:List[List]) -> List[List]:
    vismap = get_vismap(forest_map)
    print(vismap)
    print(len(vismap))
    h,w = len(forest_map), len(forest_map[0])
    sides = (h + w)*2 - 4
    print(len(vismap) + sides)

def get_by_height(forest_map:List[List]) -> List[Set]:
    heightmap = [set() for _ in range(10)]
    for i, row in enumerate(forest_map):
        for j, tree in enumerate(row):
            heightmap[tree].add((i,j))
    return heightmap

def get_scenic_score(x:int, y:int, height:int,
                r:int, c:int, heightmap:List[Set]) -> int:
    # Horizontal distance first
    distances = [y, max(c-y-1, 0), 
            x, max(r-x-1, 0)]
    
    for i in range(height,10):
        gen = ((a,b) for a,b in heightmap[i] if a==x or b==y)
        for j,k in gen:
            if j == x and k < y:
                distances[0] = min(distances[0], y - k)
            elif j == x and k > y:
                distances[1] = min(distances[1], k - y)
            elif k == y and j < x:
                distances[2] = min(distances[2], x - j)
            elif k == y and j > x:
                distances[3] = min(distances[3], j - x)
    
    return distances[0]*distances[1]*distances[2]*distances[3]

def part2(forest_map:List[List]) -> List[List]:
    heightmap = get_by_height(forest_map)
    r = len(forest_map)
    c = len(forest_map[0])

    scores_tmp = [[0] * c for _ in range(r)]
    max_score = 0
    for i in range(r):
        for j in range(c):
            score = get_scenic_score(i, j, forest_map[i][j], r, c, heightmap)
            max_score = max(score, max_score)
            scores_tmp[i][j] = score

    print("\n".join("".join(f"{d:2d}" for d in row) for row in scores_tmp))
    print(max_score)

def day8_part1():
    forest_map = read_map()
    part1(forest_map)

def day8_part2():
    forest_map = read_map()
    part2(forest_map)

if __name__ == "__main__":
    day8_part1()