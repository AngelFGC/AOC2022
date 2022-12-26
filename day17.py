from typing import List, Set, Tuple

def read_day17():
    with open("inputs/day17.txt", mode="r+", encoding="utf-8") as f:
        return f.readline().strip()

def horizontal_move(p:Tuple, disp:int, board:List[Set]) -> Tuple:
    new_p = list()
    for a, b in p:
        a2 = a + disp
        if 0 <= a2 < 7:
            if b in board[a2]:
                return p
            else: new_p.append((a2, b))
        else:
            return p
    return tuple(new_p)

def vertical_move(p:Tuple, board:List[Set]) -> Tuple[bool, Tuple]:
    new_p = list()
    for a, b in p:
        b2 = b - 1
        if b2 in board[a]:
            return True, p
        elif b2 < 0:
            return True, p
        else:
            new_p.append((a, b2))
    return False, tuple(new_p)

def spawn_piece(p:Tuple, y:int):
    return [(a + 2, b + y) for a,b in p]

def update_board(piece:Tuple, board:List[Set], heights:List[int]):
    for x,y in piece:
        board[x].add(y)
        heights[x] = max(heights[x], y + 1)

def get_height_differential(heights:List[int], maxheight:int):
    return [maxheight - y for y in heights]

def print_rocks(board:List[Set], maxheight:int):
    field = ""
    for y in range(maxheight, -1, -1):
        field += "|"
        for x in range(7):
            if y in board[x]: field += "#"
            else: field += "."
        field += "|\n"
    field += "+-------+\n\n"
    print(field)

def day17():
    jetstream = read_day17()
    jets_dir = {"<": -1, ">": 1}
    pieces = [
        ((0,0), (1,0), (2,0), (3,0)),
        ((1,0), (0,1), (1,1), (1,2), (2,1)),
        ((0,0), (1,0), (2,0), (2,1), (2,2)),
        ((0,0), (0,1), (0,2), (0,3)),
        ((0,0), (0,1), (1,0), (1,1))
    ]
    board = [set() for _ in range(7)]
    heights = [0 for _ in range(7)]
    #MAX_ROCKS = 2022
    MAX_ROCKS = 1000000000000
    rock = 1
    max_height = 0
    jet_idx = 0
    added_height = 0
    states = {}

    while rock <= MAX_ROCKS:
        p_idx = (rock - 1) % len(pieces)
        p = spawn_piece(pieces[p_idx], max_height + 3)
        
        stopping = False
        while not stopping:
            jet = jets_dir[jetstream[jet_idx]]
            #print(jetstream[jet_idx], end="")
            jet_idx = (jet_idx + 1) % len(jetstream)
            p = horizontal_move(p, jet, board)
            stopping, p = vertical_move(p, board)
        #print()
        update_board(p, board, heights)

        max_height = max(heights)
        
        h_diff = get_height_differential(heights, max_height)
        keyVal = (tuple(h_diff), p_idx, jet_idx)
        if keyVal in states:
            old_maxh, old_rock = states[keyVal]
            h_diff = max_height - old_maxh
            rock_diff = rock - old_rock
            # Cycles until Max Diff
            cycles = (MAX_ROCKS - rock) // rock_diff
            added_height += h_diff * cycles
            added_rocks = rock_diff * cycles
            rock += added_rocks

        states[keyVal] = (max_height, rock)

        rock += 1
        #print_rocks(board, max_height)

    print(max_height + added_height)


if __name__ == "__main__":
    day17()