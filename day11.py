from collections.abc import Callable
from operator import __add__ as add_two, __mul__ as mul_two
from typing import Dict, List

class Monkey(object):
    items: List[int]
    op: Callable[[int],int]
    test: int
    if_true: int
    if_false: int
    inspections: int
    mod: int

    def __init__(self) -> None:
        self.items = list()
        self.op = add_two
        self.test = 2
        self.if_true = 0
        self.if_false = 0
        self.inspections = 0
        self.mod = 0

    def run_round(self) -> List:
        targets = list()
        new_items = list()
        
        self.inspections += len(self.items)
        
        for item in self.items:
            worry = self.op(item) 
            #worry = worry // 3
            if worry % self.test == 0:
                targets.append(self.if_true)
            else:
                targets.append(self.if_false)
            
            worry = worry % self.mod
            new_items.append(worry)

        self.items.clear()
        return list(zip(new_items, targets))

def get_operation(contents:List, ops:Dict) -> Callable:
    the_op = None
    this_op = ops[contents[1]]

    if contents[0] == contents[2] == "old":
        the_op = lambda x: int(this_op(x, x))
    elif contents[0] == "old":
        num = int(contents[2])
        the_op = lambda x: int(this_op(x, num))
    else:
        numL = int(contents[0])
        numR = int(contents[2])
        the_op = lambda x: int(this_op(numL, numR))
    return the_op

def read_day11() -> List:
    monkeys = list()
    ops = {"*":mul_two, "+":add_two}
    curr_monkey = None
    common_mod = 1
    with open("inputs/day11.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            if "Monkey" in line:
                if curr_monkey is not None:
                    monkeys.append(curr_monkey)
                curr_monkey = Monkey()
            elif "Starting" in line:
                contents = line[line.index(":")+2:].strip().split(", ")
                curr_monkey.items = [int(s) for s in contents]
            elif "Operation" in line:
                contents = line[line.index("=")+2:].strip().split(" ")
                curr_monkey.op = get_operation(contents, ops)
            else:
                contents = line.strip().split()
                if "Test" in line:
                    val = int(contents[-1])
                    curr_monkey.test = val
                    common_mod *= val
                elif "true" in line:
                    curr_monkey.if_true = int(contents[-1])
                elif "false" in line:
                    curr_monkey.if_false = int(contents[-1])
    monkeys.append(curr_monkey)
    for mon in monkeys:
        mon.mod = common_mod
    return monkeys

def day11_part1(monkeys:List[Monkey]):
    for i in range(10000):
        for mon in monkeys:
            result = mon.run_round()
            for item, targ in result:
                monkeys[targ].items.append(item)
    
    monkey_business = [mon.inspections for mon in monkeys]
    monkey_business.sort()
    
    print(monkey_business[-1] * monkey_business[-2])

def day11():
    monkeys = read_day11()
    day11_part1(monkeys)

if __name__ == "__main__":
    day11()