def generate_directory_1():
    dir_sums = {"/":0}
    curr_path = ["/"]
    curr_path_str = "/"
    with open("inputs/day7.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            content = line.split()
            if content[0] == "$":
                if len(content) == 3 and content[1] == "cd":
                    if content[2] == "..":
                        old_path = curr_path_str
                        curr_path.pop()
                        curr_path_str = "/".join(curr_path)
                        dir_sums[curr_path_str] += dir_sums[old_path]
                    elif content[2] != "/":
                        curr_path.append(content[2])
                        curr_path_str = "/".join(curr_path)
                        if curr_path_str not in dir_sums:
                            dir_sums[curr_path_str] = 0
            else:
                if content[0] != "dir":
                    dir_sums[curr_path_str] += int(content[0])
    while len(curr_path) > 1:
        old_path = curr_path_str
        curr_path.pop()
        curr_path_str = "/".join(curr_path)
        dir_sums[curr_path_str] += dir_sums[old_path]

    part1_sum = sum(dir_sums[k] for k in dir_sums if dir_sums[k] <= 100000)

    available = 70000000 - dir_sums["/"]
    need = 30000000
    must_free = need - available

    candidates = [(dir_sums[k], k) for k in dir_sums if dir_sums[k] >= must_free]
    candidates.sort()

    return part1_sum, candidates[0][0]

def day7():
    print(generate_directory_1())

if __name__ == "__main__":
    day7()