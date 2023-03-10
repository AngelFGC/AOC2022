from __future__ import annotations
from dataclasses import dataclass, field
from mimetypes import init
from pydoc import resolve
from typing import AnyStr


@dataclass
class BOpNode(object):
    name: str
    op: str = field(init=False, default=None)
    left: BOpNode = field(init=False, repr=False, hash=False, default=None)
    right: BOpNode = field(init=False, repr=False, hash=False, default=None)
    parent: BOpNode = field(init=False, repr=False, hash=False, default=None)
    fwdeval: int = field(init=False, repr=False, hash=False, default=None)

    def traverse(self):
        s = "("
        if self.left is not None:
            s += self.left.traverse()
        s += f"{self.op}"
        if self.right is not None:
            s += self.right.traverse()
        return s + ")"

    def operate(self):
        ops = {
            "+": lambda x, y: x+y,
            "-": lambda x, y: x-y,
            "*": lambda x, y: x*y,
            "/": lambda x, y: x//y,
        }
        if self.op.isnumeric():
            return int(self.op)
        else:
            l_result = 0 if self.left is None else self.left.operate()
            r_result = 0 if self.right is None else self.right.operate()
            fn = ops[self.op]
            return fn(l_result, r_result)
    
    def evalfwd(self):
        ops = {
            "+": lambda x, y: x+y,
            "-": lambda x, y: x-y,
            "*": lambda x, y: x*y,
            "/": lambda x, y: x//y,
        }
        if self.name == "humn":
            self.fwdeval = "humn"
        elif self.op.isnumeric():
            self.fwdeval = int(self.op)
        else:
            if self.left is not None: self.left.evalfwd()
            if self.right is not None: self.right.evalfwd()
            if self.left.fwdeval == "humn" or self.right.fwdeval == "humn":
                self.fwdeval = "humn"
            else:
                fn = ops[self.op]
                self.fwdeval = fn(self.left.fwdeval, self.right.fwdeval)
    
    def evalbwd(self):
        ops = {
            "+": lambda x, y: x+y,
            "-": lambda x, y: x-y,
            "*": lambda x, y: x*y,
            "/": lambda x, y: x//y,
        }
        if self.left is not None and self.left.fwdeval == "humn":
            if self.op == "+":
                self.left.fwdeval = self.fwdeval - self.right.fwdeval
            elif self.op == "-":
                self.left.fwdeval = self.fwdeval + self.right.fwdeval
            elif self.op == "*":
                self.left.fwdeval = self.fwdeval // self.right.fwdeval
            elif self.op == "/":
                self.left.fwdeval = self.fwdeval * self.right.fwdeval
            self.left.evalbwd()
        elif self.right is not None and self.right.fwdeval == "humn":
            if self.op == "+":
                self.right.fwdeval = self.fwdeval - self.left.fwdeval
            elif self.op == "-":
                self.right.fwdeval = self.left.fwdeval - self.fwdeval
            elif self.op == "*":
                self.right.fwdeval = self.fwdeval // self.left.fwdeval
            elif self.op == "/":
                self.right.fwdeval = self.left.fwdeval // self.fwdeval
            self.right.evalbwd()

def day21_1B():
    nodes = dict()
    with open("inputs/day21.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            left, right = line.strip().split(": ")

            if right.isnumeric():
                if left not in nodes:
                    bnode = BOpNode(left)
                    bnode.op = right
                    nodes[left] = bnode
                else:
                    nodes[left].op = right
            else:
                x, op_str, y = right.split()
                bnode = BOpNode(left) if left not in nodes else nodes[left]
                bnode.op = op_str
                nodeLeft = BOpNode(x) if x not in nodes else nodes[x]
                nodeRight = BOpNode(y) if y not in nodes else nodes[y]
                bnode.left, bnode.right = nodeLeft, nodeRight
                nodes[left] = bnode
                nodes[x] = nodeLeft
                nodes[y] = nodeRight
    # print(nodes["root"].traverse())
    print(nodes["root"].operate())


def day21_2():
    nodes = dict()
    with open("inputs/day21.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            left, right = line.strip().split(": ")

            if right.isnumeric():
                if left not in nodes:
                    bnode = BOpNode(left)
                    bnode.op = right
                    nodes[left] = bnode
                else:
                    nodes[left].op = right
            else:
                x, op_str, y = right.split()
                bnode = BOpNode(left) if left not in nodes else nodes[left]
                bnode.op = op_str
                nodeLeft = BOpNode(x) if x not in nodes else nodes[x]
                nodeRight = BOpNode(y) if y not in nodes else nodes[y]
                nodes[left] = nodeLeft.parent = nodeRight.parent = bnode
                nodes[x] = bnode.left = nodeLeft
                nodes[y] = bnode.right = nodeRight
                
    # nodes[""]
    #print(nodes["root"].traverse())
    # print(nodes["root"].operate())

    root: BOpNode = nodes["root"]
    root.left.evalfwd()
    root.right.evalfwd()

    if root.left.fwdeval == "humn":
        root.left.fwdeval = root.right.fwdeval
        root.left.evalbwd()
    elif root.right.fwdeval == "humn":
        root.right.fwdeval = root.left.fwdeval
        root.right.evalbwd
    print(nodes["humn"].fwdeval)
    


def resolvedependencies(left, found, deps, pending):
    for k in deps[left]:
        mnky = pending[k]
        if mnky[0] == left:
            mnky[0] = str(found[left])
        elif mnky[2] == left:
            mnky[2] = str(found[left])
        if mnky[0].isnumeric() and \
                mnky[2].isnumeric():
            x, op, y = mnky
            v = op(int(x), int(y))
            del pending[k]
            found[k] = v
            if k in deps:
                resolvedependencies(k, found, deps, pending)
    del deps[left]


def finddeps(k, left, found, deps):
    if k in found:
        return found[k]
    elif k in deps:
        deps[k].append(left)
    else:
        deps[k] = [left]
    return k


def day21_1():
    found = dict()
    deps = dict()
    ops = {
        "+": lambda x, y: x+y,
        "-": lambda x, y: x-y,
        "*": lambda x, y: x*y,
        "/": lambda x, y: x//y,
    }
    pending = dict()

    with open("inputs/day21.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            left, right = line.strip().split(": ")
            if right.isnumeric():
                found[left] = int(right)
                if left in deps:
                    resolvedependencies(left, found, deps, pending)
            else:
                x, op_str, y = right.split()
                op = ops[op_str]

                if x in found and y in found:
                    found[left] = op(found[x], found[y])
                    if left in deps:
                        resolvedependencies(left, found, deps, pending)
                    continue

                x = finddeps(x, left, found, deps)
                y = finddeps(y, left, found, deps)

                pending[left] = [str(x), op, str(y)]

    # if len(pending) >= 1:
    # x, op, y = pending["root"]
    # x, y = int(x), int(y)
    # print(op(x, y))

    print(found['root'])


if __name__ == "__main__":
    day21_2()
