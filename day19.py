import math
import re
from tqdm import tqdm
from typing import List

def read_day19():
    blueprints = list()
    with open("aoc2022/day19.txt", mode="r+", encoding="utf-8") as f:
        blueprints = [[int(s) for s in re.findall("\d+", line)] for line in f]
    return blueprints

def build_geode_robot(res:List, robs:List, blue:List, t:int):
    mat_ore, mat_clay, mat_obsi = res[:]
    bot_ore, bot_clay, bot_obsi = robs[:]
    ore_needed = max(0, blue[5] - mat_ore)
    obsi_needed = max(0, blue[6] - mat_obsi)
    ore_cycles = int(math.ceil(ore_needed / bot_ore))
    obsi_cycles = int(math.ceil(obsi_needed / bot_obsi))
    tot_cycles = max(ore_cycles, obsi_cycles)
    if t > tot_cycles + 1:
        # We have time. We'll build it next.
        tot_cycles = tot_cycles + 1
        new_mat_ore = mat_ore + bot_ore * tot_cycles - blue[5]
        new_mat_clay = mat_clay + bot_clay * tot_cycles
        new_mat_obsi = mat_obsi + bot_obsi * tot_cycles - blue[6]
        new_t = t - tot_cycles

        return ([new_mat_ore, new_mat_clay, new_mat_obsi], new_t)
    else:
        return None

def build_obsidian_robot(res:List, robs:List, blue:List, t:int):
    mat_ore, mat_clay, mat_obsi = res[:]
    bot_ore, bot_clay, bot_obsi = robs[:]
    ore_needed = max(0, blue[3] - mat_ore)
    clay_needed = max(0, blue[4] - mat_clay)
    ore_cycles = int(math.ceil(ore_needed / bot_ore))
    clay_cycles = int(math.ceil(clay_needed / bot_clay))
    tot_cycles = max(ore_cycles, clay_cycles)
    if t > tot_cycles + 1:
        # We have time. We'll build it next.
        tot_cycles = tot_cycles + 1
        new_mat_ore = mat_ore + bot_ore * tot_cycles - blue[3]
        new_mat_clay = mat_clay + bot_clay * tot_cycles - blue[4]
        new_mat_obsi = mat_obsi + bot_obsi * tot_cycles 
        new_t = t - tot_cycles

        return ([new_mat_ore, new_mat_clay, new_mat_obsi], new_t)
    else:
        return None

def build_clay_robot(res:List, robs:List, blue:List, t:int):
    mat_ore, mat_clay, mat_obsi = res[:]
    bot_ore, bot_clay, bot_obsi = robs[:]
    ore_needed = max(0, blue[2] - mat_ore)
    ore_cycles = int(math.ceil(ore_needed / bot_ore))
    tot_cycles = ore_cycles
    if t > tot_cycles + 1:
        # We have time. We'll build it next.
        tot_cycles = tot_cycles + 1
        new_mat_ore = mat_ore + bot_ore * tot_cycles - blue[2]
        new_mat_clay = mat_clay + bot_clay * tot_cycles
        new_mat_obsi = mat_obsi + bot_obsi * tot_cycles 
        new_t = t - tot_cycles

        return ([new_mat_ore, new_mat_clay, new_mat_obsi], new_t)
    else:
        return None

def build_ore_robot(res:List, robs:List, blue:List, t:int):
    mat_ore, mat_clay, mat_obsi = res[:]
    bot_ore, bot_clay, bot_obsi = robs[:]
    ore_needed = max(0, blue[1] - mat_ore)
    ore_cycles = int(math.ceil(ore_needed / bot_ore))
    tot_cycles = ore_cycles
    if t > tot_cycles + 1:
        # We have time. We'll build it next.
        tot_cycles = tot_cycles + 1
        new_mat_ore = mat_ore + bot_ore * tot_cycles - blue[1]
        new_mat_clay = mat_clay + bot_clay * tot_cycles
        new_mat_obsi = mat_obsi + bot_obsi * tot_cycles 
        new_t = t - tot_cycles

        return ([new_mat_ore, new_mat_clay, new_mat_obsi], new_t)
    else:
        return None

def simulate(res:List, robs:List, blue:List, t:int, max_ore):
    obsi_cap = blue[6] - (res[2] + robs[2])
    if t <= 1:
        # There's no point if t < the time it'd take to build a geode robot
        return 0
    else:
        scores = list()
        bot_ore, bot_clay, bot_obsi = robs[:]
        
        # Need to define criterion for building bots of each given type
        # NOTE: Bots are built in order
        if bot_obsi >= 1:
            # Let's build an Geode Robot next
            build_results = build_geode_robot(res, robs, blue, t)
            if build_results is not None:
                this_score = (build_results[1]) + simulate(
                    build_results[0], robs, blue, 
                    build_results[1], max_ore
                )
                scores.append(this_score)

        if 1 <= bot_clay and bot_obsi < blue[6]:
            # Let's build an Obsidian Robot next
            build_results = build_obsidian_robot(res, robs, blue, t)
            if build_results is not None:
                this_score = simulate(
                    build_results[0], 
                    [bot_ore, bot_clay, bot_obsi + 1], 
                    blue, build_results[1], max_ore
                )
                scores.append(this_score)
        
        ore_ratio = max(
            [blue[1], blue[2], blue[3] if blue[3] >= blue[4] else 0,
            blue[5], blue[6] if blue[6] >= blue[5] else 0]
        )

        if bot_clay < blue[4]:
             # Let's build a Clay Robot next
            build_results = build_clay_robot(res, robs, blue, t)
            if build_results is not None:
                this_score = simulate(
                    build_results[0], 
                    [bot_ore, bot_clay + 1, bot_obsi], 
                    blue, build_results[1], max_ore
                )
                scores.append(this_score)

        if bot_ore < max_ore:
            # Let's build an Ore Robot next
            build_results = build_ore_robot(res, robs, blue, t)
            if build_results is not None:
                this_score = simulate(
                    build_results[0], 
                    [bot_ore + 1, bot_clay, bot_obsi], 
                    blue, build_results[1], max_ore
                )
                scores.append(this_score)
        
        return max(scores, default=0)

def day19_p1():
    blueprints = read_day19()
    MAX_TIME = 24
    quality_sum = 0
    for b in blueprints:
        max_ore = max(b[1], b[2], b[3], b[5])
        best_score = simulate([0,0,0], [1,0,0], b, MAX_TIME, max_ore)
        print(best_score)
        quality_sum += best_score * b[0]

    print(quality_sum)

def day19_p2():
    blueprints = read_day19()
    MAX_TIME = 32
    quality_mult = 1
    for b in tqdm(blueprints[:3]):
        max_ore = max(b[1], b[2], b[3], b[5])
        best_score = simulate([0,0,0], [1,0,0], b, MAX_TIME, max_ore)
        print(best_score)
        quality_mult *= best_score

    print(quality_mult)
    

if __name__ == "__main__":
    #day19_p1()
    day19_p2()