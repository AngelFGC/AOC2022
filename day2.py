def day2():
    vals = {chr(65+i):i for i in range(3)}
    revals = {vals[k]:k for k in vals}
    vals.update({chr(88+i):i for i in range(3)})

    def result(p1:str, p2:str) -> int:
        """
        0 = rock
        1 = paper
        2 = scissors
        """
        diff = vals[p2] - vals[p1]
        if diff == 0:
            return vals[p2] + 1 + 3
        elif diff == 1 or (vals[p2] == 0 and diff == -2):
            return vals[p2] + 1 + 6
        else:
            return vals[p2] + 1
    
    def strategy_result(p1:str, s2:str) -> int:
        diff = 0
        winval = 0
        s2_val = vals[s2]
        if s2_val == 0:
            diff, winval = -1, 0
        elif s2_val == 1:
            diff, winval = 0, 3
        else:
            diff, winval = 1, 6
        p2_idx = (vals[p1] + diff + 3) % 3

        return p2_idx + 1 + winval


    points = 0
    strategy_pts = 0
    
    with open("inputs/day2.txt", mode="r+", encoding="utf-8") as f:
        for line in f:
            [opp, me] = line.split()
            points += result(opp, me)
            strategy_pts += strategy_result(opp, me)

    print(points)
    print(strategy_pts)

if __name__ == "__main__":
    day2()