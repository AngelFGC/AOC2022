from queue import SimpleQueue as Queue
from typing import List,Set, Tuple

def read_day9() -> Queue:
    with open("index/day9.txt", mode="r+", encoding="utf-8") as f:
        the_q = Queue()
        for line in f:
            the_q.put(line.strip())
    return the_q

def get_suggestion(head:List, tail:List) -> Tuple[int]:
    dx, dy = head[0] - tail[0], head[1] - tail[1]
    adx, ady = abs(dx), abs(dy)

    if adx <= 1 and ady <= 1:
        return (0, 0) # No need to move

    if adx == 0:
        # Only need to update y
        return (0, dy - dy//ady)
    elif ady == 0:
        # Only need to update x
        return (dx - dx//adx, 0)
    else:
        # We need to move diagonally
        return (dx//adx, dy//ady)

def move_tail(tail:List, suggestion:Tuple) -> List[Tuple]:
    # SUGGESTION is a delta already
    newx, newy = suggestion[0] + tail[0], suggestion[1] + tail[1]

    positions = []

    if suggestion[0] == 0:
        # Move across y
        if suggestion[1] > 0: positions = [(tail[0], y+1) for y in range(tail[1], newy)]
        else: positions = [(tail[0], y) for y in range(tail[1], newy, -1)]
    elif suggestion[1] == 0:
        # Move across x
        if suggestion[0] > 0: positions = [(x+1, tail[1])  for x in range(tail[0], newx)]
        else: positions = [(x, tail[1]) for x in range(tail[0], newx, -1)]
    # else:
    #     # Move diagonal (1)
    #     positions = []
    if (newx, newy) not in positions:
        positions.append((newx, newy))

    tail[0], tail[1] = newx, newy
    return positions

def execute_instruction(head:List, instruction:str) -> None:
    heading, steps = instruction.split()
    steps = int(steps)

    if heading == "U": head[1] += steps
    elif heading == "D": head[1] -= steps
    elif heading == "R": head[0] += steps
    elif heading == "L": head[0] -= steps
    else: raise ValueError("Invalid Heading Value")

def day9_part1(instructions:Queue):
    head_pos = [0,0]
    tail_pos = [0,0]
    visited = [(0,0)]

    while not instructions.empty():
        instruction = instructions.get()
        # print(instruction)
        execute_instruction(head_pos, instruction)

        suggestion = get_suggestion(head_pos, tail_pos)

        while suggestion != (0,0):
            visited.extend(move_tail(tail_pos, suggestion))
            #print(tail_pos)
            suggestion = get_suggestion(head_pos, tail_pos)
        
    print(len(set(visited)))

def move_tail_2(tail:List, suggestion:Tuple) -> None:
    # SUGGESTION is a delta already
    newx, newy = suggestion[0] + tail[0], suggestion[1] + tail[1]
    tail[0], tail[1] = newx, newy

def execute_instruction_stepwise(snake:List, instruction:str) -> List[Set]:
    visited_by_tail = [tuple(snake[-1])]
    heading, steps = instruction.split()
    steps = int(steps)

    dir_vector = [0,0]

    if heading == "U": dir_vector[1] = 1
    elif heading == "D": dir_vector[1] = -1
    elif heading == "R": dir_vector[0] = 1
    elif heading == "L": dir_vector[0] = -1
    else: raise ValueError("Invalid Heading Value")

    for _ in range(steps):
        snake[0][:] = [snake[0][0] + dir_vector[0],
                        snake[0][1] + dir_vector[1]]
        for j in range(1, len(snake)):
            suggestion = get_suggestion(snake[j - 1], snake[j])
            move_tail_2(snake[j], suggestion)
        
        visited_by_tail.append(tuple(snake[-1]))

    return visited_by_tail

def day9_part1_redux(instructions:Queue):
    snake = [[0,0] for i in range(2)]
    visited = []

    while not instructions.empty():
        instruction = instructions.get()
        new_visited = execute_instruction_stepwise(snake, instruction)
        visited.extend(new_visited)

    print(len(set(visited)))

def day9_part2(instructions:Queue):
    snake = [[0,0] for i in range(10)]
    visited = []

    while not instructions.empty():
        instruction = instructions.get()
        new_visited = execute_instruction_stepwise(snake, instruction)
        visited.extend(new_visited)

    print(len(set(visited)))

def day9():
    instructions = read_day9()
    day9_part1(instructions)
    instructions = read_day9()
    day9_part1_redux(instructions)
    instructions = read_day9()
    day9_part2(instructions)

if __name__ == "__main__":
    day9()