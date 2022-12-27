from __future__ import annotations
from copy import copy
from dataclasses import dataclass, field
from queue import SimpleQueue
from tqdm import tqdm
from typing import Iterable, Tuple


def read_day20():
    with open("inputs/day20.txt", mode="r+", encoding="utf-8") as f:
        return [int(s.strip()) for s in f]

@dataclass(unsafe_hash=True)
class DLLNode(object):
    data: int
    prev: DLLNode = field(init=False, repr=False, hash=False)
    next: DLLNode = field(init=False, repr=False, hash=False)

    @classmethod
    def fromiterable(cls, it: Iterable[int]) -> DLLNode:
        head = None
        for x in it:
            if head is None:
                head = DLLNode(x)
                head.prev = head.next = head
            else:
                tail = DLLNode(x)
                head.prev.linknext(tail)
                tail.linknext(head)
        return head

    def __iter__(self):
        yield self
        pivot = self.next
        while pivot != self:
            yield pivot
            pivot = pivot.next

    def linknext(self, right:DLLNode):
        self.next, right.prev = right, self

    def shift(self, x:int, n:int):
        pivot = self

        new_idx = x % (n-1)

        if new_idx == 0:
            return

        while new_idx > 0:
            pivot = pivot.next
            new_idx -= 1
       
        # Disconnect
        left, right = self.prev, self.next
        left.linknext(right)

        # Reconnect after pivot
        right = pivot.next
        pivot.linknext(self)
        self.linknext(right)
    
    def find_loop(self):
        s = set()
        for n in iter(self):
            if n in s:
                print(n.data)
                break
            else:
                s.add(n)

def day20_p1B():
    num_array = read_day20()
    n = len(num_array)
    q = SimpleQueue()

    head = DLLNode.fromiterable(num_array)

    for node in iter(head):
        q.put(node)
    i = 0
    while not q.empty():
        i += 1
        node:DLLNode = q.get()
        x = node.data
        if x == 0: head = node
        else: node.shift(x, n)
        #node.find_loop()

    #head.find_loop()

    new_list = [node.data for node in iter(head)]
    print(sum(new_list[c % n] for c in [1000, 2000, 3000]))

def duplicatequeue(q0:SimpleQueue) -> Tuple[SimpleQueue, SimpleQueue]:
    q1, q2 = SimpleQueue(), SimpleQueue()

    while not q0.empty():
        obj = q0.get()
        q1.put(obj)
        q2.put(obj)
    
    return q1, q2

def day20_p2():
    num_array = read_day20()
    n = len(num_array)
    for i in range(n):
        num_array[i] *= 811589153
    
    qbase = SimpleQueue()
    head = DLLNode.fromiterable(num_array)
    for node in iter(head):
        qbase.put(node)

    for _ in range(10):
        qbase, q = duplicatequeue(qbase)
        while not q.empty():
            node:DLLNode = q.get()
            x = node.data
            if x == 0: head = node
            else: node.shift(x, n)

    new_list = [node.data for node in iter(head)]
    print(sum(new_list[c % n] for c in [1000, 2000, 3000]))

if __name__ == "__main__":
    day20_p2()