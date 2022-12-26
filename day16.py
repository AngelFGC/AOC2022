import itertools
import re

from tqdm import tqdm
from typing import Dict

def read_day16():
    re_ader = re.compile(r"Valve (.{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
    adjacency_list = dict()
    pressure_list = dict()
    with open("inputs/day16.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            matches = re_ader.fullmatch(line.strip())
            if matches:
                vname, frate, vlist = tuple(matches.groups())
                frate = int(frate)
                vlist = vlist.split(", ")
                adjacency_list[vname] = vlist
                pressure_list[vname] = frate

    return adjacency_list, pressure_list

def floydwarshall(adjacency_list:Dict):
    dist = {k1:{k2:float('inf') for k2 in adjacency_list} for k1 in adjacency_list}
    keys = list(adjacency_list.keys())
    
    for k in adjacency_list:
        dist[k][k] = 0

    for k1 in adjacency_list:
        dist[k1][k1] = 0
        for k2 in adjacency_list[k1]:
            dist[k1][k2] = 1
    
    for k in keys:
        for i in keys:
            for j in keys:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist

def generate_paths(adjacency_list:Dict, pressure_list:Dict):
    distances = floydwarshall(adjacency_list)
    stack = list()
    # Start Node, Remaining Time, Nodes Visited, Total Pressure
    stack.append(("AA", 30, ["AA"], 0))

    max_pressure = 0

    while stack:
        c_node, t, visited, pressure = stack.pop()
        if t < 0:
            continue

        next_caves = [k for k in pressure_list if k not in visited and pressure_list[k] != 0]
        traversal_distance = {k:distances[visited[-1]][k] for k in next_caves}

        max_pressure = max(pressure, max_pressure)

        for k in next_caves:
            t_time = traversal_distance[k]
            next_t = t - t_time - 1 # The 1 is from opening the valve
            next_visited = visited[:] + [k]
            next_pressure = pressure + pressure_list[k] * next_t
            stack.append((k, next_t, next_visited, next_pressure))

    return max_pressure

def generate_paths_2(adjacency_list:Dict, pressure_list:Dict):
    distances = floydwarshall(adjacency_list)
    stack = list()
    # Start Node, Remaining Time, Nodes Visited, Total Pressure
    stack.append(("AA", 26, ["AA"], 0))

    max_pressures = dict()

    while stack:
        c_node, t, visited, pressure = stack.pop()
        if t < 0:
            continue

        next_caves = [k for k in pressure_list if k not in visited and pressure_list[k] != 0]
        traversal_distance = {k:distances[visited[-1]][k] for k in next_caves}

        visited_set = frozenset(visited)
        if visited_set in max_pressures:
            max_pressures[visited_set] = max(max_pressures[visited_set], pressure)
        else:
            max_pressures[visited_set] = pressure

        for k in next_caves:
            t_time = traversal_distance[k]
            next_t = t - t_time - 1 # The 1 is from opening the valve
            next_visited = visited[:] + [k]
            next_pressure = pressure + pressure_list[k] * next_t
            stack.append((k, next_t, next_visited, next_pressure))

    return max(max_pressures[s1] + max_pressures[s2]
            for s1, s2 in itertools.combinations(max_pressures.keys(), 2) if s1.isdisjoint(s2 - set(["AA"])))

def day16():
    adjacency_list, pressure_list = read_day16()
    #print(generate_paths(adjacency_list, pressure_list))
    print(generate_paths_2(adjacency_list, pressure_list))

if __name__ == "__main__":
    day16()