import heapq
from typing import List, Tuple

def get_start_end(mtn_map:List[List[str]]) -> Tuple[int]:
    start, end = None, None
    for r in range(len(mtn_map)):
        for c in range(len(mtn_map[r])):
            if mtn_map[r][c] == "S":
                start = (r,c)
            elif mtn_map[r][c] == "E":
                end = (r,c)
    return start, end

def get_neighbors(r, c):
    return [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]

def check_if_in_pq(x:int, y:int, pq:List):
    for [_,r,c] in pq:
        if (x,y) == (r,c):
            return True
    return False

def get_val(c:str) -> int:
    if c == "S": c = "a"
    if c == "E": c = "z"
    return ord(c)

def shortest_path(mtn_map:List[List[str]]):
    src, dest = get_start_end(mtn_map)

    pq = []
    dist = [[0 for c in range(len(mtn_map[r]))] for r in range(len(mtn_map))]
    prev = [[None for c in range(len(mtn_map[r]))] for r in range(len(mtn_map))]
    for r in range(len(mtn_map)):
        for c in range(len(mtn_map[r])):
            if (r,c) != src:
                dist[r][c] = float("+inf")
                heapq.heappush(pq, [float("+inf"), r, c])
    heapq.heappush(pq, [0, src[0], src[1]])

    the_dict = {(t[1],t[2]):t for t in pq}

    while pq:
        (d, r, c) = heapq.heappop(pq)
        if (r,c) == dest:
            break
        for x,y in get_neighbors(r,c):
            if check_if_in_pq(x,y,pq):
                diff = get_val(mtn_map[r][c]) - get_val(mtn_map[x][y])
                if diff >= -1:
                    alt = dist[r][c] + 1
                    if alt < dist[x][y]:
                        dist[x][y] = alt
                        prev[x][y] = (r,c)
                        elem = the_dict[(x,y)]
                        elem[0] = alt
        heapq.heapify(pq)
    path = []
    u = dest
    if prev[u[0]][u[1]] is not None or u == src:
        while u is not None:
            path.append(u)
            u = prev[u[0]][u[1]]
    
    print(path)
    print(len(path)-1)

def shortest_path_to_a(mtn_map:List[List[str]]):
    dest, src = get_start_end(mtn_map)

    pq = []
    dist = [[0 for c in range(len(mtn_map[r]))] for r in range(len(mtn_map))]
    prev = [[None for c in range(len(mtn_map[r]))] for r in range(len(mtn_map))]
    for r in range(len(mtn_map)):
        for c in range(len(mtn_map[r])):
            if (r,c) != src:
                dist[r][c] = float("+inf")
                heapq.heappush(pq, [float("+inf"), r, c])
    heapq.heappush(pq, [0, src[0], src[1]])

    the_dict = {(t[1],t[2]):t for t in pq}

    while pq:
        (d, r, c) = heapq.heappop(pq)
        if mtn_map[r][c] == "a" or mtn_map[r][c] == "S":
            dest = (r,c)
            break
        for x,y in get_neighbors(r,c):
            if check_if_in_pq(x,y,pq):
                diff = get_val(mtn_map[r][c]) - get_val(mtn_map[x][y])
                if diff <= 1:
                    alt = dist[r][c] + 1
                    if alt < dist[x][y]:
                        dist[x][y] = alt
                        prev[x][y] = (r,c)
                        elem = the_dict[(x,y)]
                        elem[0] = alt
        heapq.heapify(pq)
    path = []
    u = dest
    if prev[u[0]][u[1]] is not None or u == src:
        while u is not None:
            path.append(u)
            u = prev[u[0]][u[1]]
    
    print(path)
    print(len(path)-1)

def read_day12() -> List[List[str]]:
    with open("inputs/day12.txt", mode="r+", encoding="utf-8") as f:
        return [[c for c in line.strip()] for line in f]

def day12_p1():
    mountain_map = read_day12()
    shortest_path(mountain_map)

def day12_p2():
    mountain_map = read_day12()
    shortest_path_to_a(mountain_map)

if __name__ == "__main__":
    day12_p1()
    day12_p2()