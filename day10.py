import itertools
from operator import __add__ as add_two, __mul__ as mul_two
from queue import SimpleQueue as Queue
from typing import List,Set, Tuple

def read_day10():
    with open("inputs/day10.txt", mode="r+", encoding="utf-8") as f:
        return [line.strip() for line in f]

def day10_dummy(x:int, _):
    return x

def advance_clock(cpu_q:List[Set]):
    # each oper is:
    # [name, clock, function, Y]
    zeros = []
    for i, oper in enumerate(cpu_q):
        oper[1] -= 1
        if oper[1] == 0:
            zeros.append(i)
    
    return zeros

def generate_queue(instructions:List[str]) -> Queue:
    ops_set = {"noop":(1, day10_dummy), "addx":(2, add_two)}
    op_queue = Queue()
    for instr in instructions:
        instr = instr.split()
        oper = instr[0]

        if len(instr) == 1:
            Y = 0
        else:
            Y = int(instr[1])
        
        op_queue.put([oper, ops_set[oper][0],
                ops_set[oper][1], Y])
    return op_queue

def simulate_cpu_simpler(instructions:List[str]) -> int:
    X = 1
    Y = 0

    op_queue = generate_queue(instructions)
    
    interest_sum = 0

    next_check = 20
    check_leap = 40
    cpu_clock = 1
    while not op_queue.empty():
        [_, clock, fn, Y] = op_queue.get()
        next_clock = cpu_clock + clock
        
        if cpu_clock <= next_check < next_clock:
            interest_sum += X * next_check
            next_check += check_leap
            X = fn(X, Y)
        elif next_check == next_clock:
            X = fn(X, Y)
            interest_sum += X * next_check
            next_check += check_leap
        else:
            X = fn(X, Y)
        
        cpu_clock = next_clock

    return interest_sum

def simulate_cpu(instructions:List[str]) -> int:
    X = 1
    Y = 0

    op_queue = generate_queue(instructions)
    
    all_instr = list()
    interest_sum = 0
    for c in itertools.count(1):
        # [instr, clock, fn, Y]
        if not op_queue.empty():
            next_instr = op_queue.get()
            all_instr.append(next_instr)
        
        zeros = advance_clock(all_instr)

        for i in zeros:
            [_, _, fn, Y] = all_instr[i]
            X = fn(X, Y)
        
        for i in zeros[::-1]:
            del all_instr[i]
        
        if c % 40 == 20:
            interest_sum += c * X

        if not all_instr and op_queue.empty():
            break
        
    return interest_sum

def simulate_crt(instructions:List[str]) -> int:
    X = 1
    Y = 0

    op_queue = generate_queue(instructions)
    
    crt_display = [[" " for i in range(40)] for i in range(6)]

    cpu_clock = 1
    row = 0
    max_clock = 6 * 40
    [_, clock, fn, Y] = op_queue.get()
    while cpu_clock <= max_clock:
        idx = cpu_clock - 1
        row, col = idx // 40, idx % 40

        # Print, if possible
        if X-1 <= col <= X+1:
            crt_display[row][col] = "#"
        else:
            crt_display[row][col] = "."
        
        cpu_clock += 1
        clock -= 1

        if clock == 0:
            X = fn(X, Y)
            if not op_queue.empty():
                [_, clock, fn, Y] = op_queue.get()

    print("\n".join("".join(c for c in line) for line in crt_display))
        
def day10():
    instr = read_day10()
    simulate_crt(instr)

if __name__ == "__main__":
    day10()