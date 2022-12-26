import re
from tqdm import tqdm
from typing import List, Tuple

def read_day15() -> List[Tuple]:
    re_obj = re.compile(r"Sensor at x=(\-?\d+), y=(\-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)")
    sensors = list()
    with open("inputs/day15.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            matched = re_obj.fullmatch(line.strip())
            
            if matched:
                sensors.append(tuple(int(c) for c in matched.groups()))
    return sensors

def range_in_row(y:int, sensor:Tuple):
    (xs, ys, xb, yb) = sensor
    sensor_range = abs(xs - xb) + abs(ys - yb)

    # Check if we can use this sensor
    if abs(ys - y) <= sensor_range:
        dist = abs(ys - y)
        return (xs - (sensor_range - dist),
                 xs + (sensor_range - dist))
    return None

def intersect_ranges(s_range:Tuple, s_ranges:List[Tuple]):
    not_done = True
    s_ranges.append(s_range)
    s_ranges.sort()
    while not_done:
        not_done = False
        for i in range(len(s_ranges) - 1):
            left = s_ranges[i]
            right = s_ranges[i+1]
            if (left[0] <= right[0] <= left[1] or
                right[0] <= left[0] <= right[1] or
                left[1] + 1 == right[0] or
                right[1] + 1 == left[0]):
                s_ranges[i] = (min(left + right), max(left + right))
                del s_ranges[i+1]
                not_done = True
                break

def find_ranges_in_row(row:int, sensors:List[Tuple]):
    ranges = []
    for sensor in sensors:
        row_range = range_in_row(row, sensor)
        if row_range is not None:
            intersect_ranges(row_range, ranges)
    print(sum(y-x for x,y in ranges))

def find_isolated_point(dx:int, dy:int, sensors:List[Tuple]) -> int:
    ranges = [[] for i in range(dy)]
    for y_i in tqdm(range(dy)):
        for sensor in sensors:
            row_range = range_in_row(y_i, sensor)
            if row_range is not None:
                row_range = (max(0, row_range[0]), min(dx, row_range[1]))
                intersect_ranges(row_range, ranges[y_i])
    points = list()
    for i,r in tqdm(enumerate(ranges)):
        for j in range(len(r)-1):
            if r[j+1][0] - r[j][1] == 2:
                points.append((r[j][1]+1, i))
            else:
                assert(r[j+1][0] - r[j][1] <= 1)
    assert(len(points) == 1)

    return points[0][0]*4000000 + points[0][1]

def day15():
    sensors = read_day15()
    #find_ranges_in_row(10, sensors)
    #find_ranges_in_row(2000000, sensors)
    #print(find_isolated_point(20, 20, sensors))
    print(find_isolated_point(4000000, 4000000, sensors))

if __name__ == "__main__":
    day15()