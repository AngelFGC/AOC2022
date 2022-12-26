from queue import SimpleQueue

def read_day20():
    with open("aoc2022/day20.txt", mode="r+", encoding="utf-8") as f:
        return [int[s.strip()] for s in f]

def day20_p1():
    # *Very* Inefficient
    num_array = read_day20()
    n = len(num_array)

    arr2 = list()
    q = SimpleQueue()

    for i,x in enumerate(num_array):
        obj = [i,x]
        q.put(obj)
        arr2.append(obj)
    
    while q:
        obj = q.get()
        old_idx, x = obj
        new_idx = i + x
        new_idx_mod = new_idx % n

    


if __name__ == "__main__":
    day20_p1()