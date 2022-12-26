import re
from typing import List

def read_puzzle():
    stacks = []
    instructions = []
    with open("inputs/day5.txt", mode="r+", encoding="utf-8") as f:    
        in_header = True
        for line in f:
            if in_header:
                if line == "\n": in_header = False
                else: stacks.append(line)
            else: instructions.append(line.strip())
    return stacks, instructions

def format_stacks(original_stacks:List) -> List[List]:
    original_stacks.reverse()
    num_stacks = len(original_stacks[0].split())
    new_stacks = [list() for i in range(num_stacks)]

    for stack_lvl in original_stacks[1:]:
        for i in range(num_stacks):
            str_idx = 4*i + 1
            if stack_lvl[str_idx] != " ":
                new_stacks[i].append(stack_lvl[str_idx])
    
    return new_stacks

def run_instructions_9000(stacks:List[List], instructions:List[str]):
    re_patt = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for instr in instructions:
        match = re_patt.fullmatch(instr)
        if match:
            amount = int(match.group(1))
            source = int(match.group(2)) - 1
            destin = int(match.group(3)) - 1
            for i in range(amount):
                stacks[destin].append(stacks[source].pop())
        else:
            raise RuntimeError("Input was in incorrect format")

def run_instructions_9001(stacks:List[List], instructions:List[str]):
    re_patt = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for instr in instructions:
        match = re_patt.fullmatch(instr)
        if match:
            amount = int(match.group(1))
            source = int(match.group(2)) - 1
            destin = int(match.group(3)) - 1

            crane = stacks[source][-amount:]
            del stacks[source][-amount:]
            stacks[destin].extend(crane)
        else:
            raise RuntimeError("Input was in incorrect format")

def day5_1():
    stacks, instructions = read_puzzle()
    stacks = format_stacks(stacks)
    run_instructions_9000(stacks, instructions)

    print("\n".join(str(stack) for stack in stacks))
    print("".join(stack[-1] for stack in stacks))

def day5_2():
    stacks, instructions = read_puzzle()
    stacks = format_stacks(stacks)
    run_instructions_9001(stacks, instructions)

    print("\n".join(str(stack) for stack in stacks))
    print("".join(stack[-1] for stack in stacks))

if __name__ == "__main__":
    day5_1()
    day5_2()