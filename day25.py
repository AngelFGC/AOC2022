from __future__ import annotations
from typing import Any, List

SNAFUDIGITS = {
    "=":-2,
    "-":-1,
    "0": 0,
    "1": 1,
    "2": 2
}

DIGITSNAFU = {SNAFUDIGITS[k]:k for k in SNAFUDIGITS}

class SNAFU(object):
    digits:List[int]

    def __init__(self, s:Any) -> None:
        self.digits = list()
        if isinstance(s, str):
            for c in s[::-1]:
                self.digits.append(SNAFUDIGITS[c])
        elif isinstance(s, list):
            for c in s:
                if not isinstance(c, int) or not (-2 <= c <= 2):
                    raise ValueError()
                self.digits.append(c)
        else:
            raise ValueError()
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __len__(self):
        return len(self.digits)

    def __add__(self, other:SNAFU) -> SNAFU:
        left = self.digits[:] + ([0] * (len(other) - len(self))) + [0]
        right = other.digits[:] + ([0] * (len(self) - len(other))) + [0]
        rplusl = [0]*len(right)
        for i,(x,y) in enumerate(zip(left, right)):
            rplusl[i] = x + y

        swapped = True
        while swapped:
            swapped = False
            for i, c in enumerate(rplusl):
                if c < -2:
                    swapped = True
                    rplusl[i] = 5 + c
                    rplusl[i+1] -= 1
                elif c > 2:
                    swapped = True
                    rplusl[i] = c - 5
                    rplusl[i+1] += 1

        for i in range(len(rplusl)-1, -1, -1):
            if rplusl[i] == 0:
                del rplusl[i]
            else:
                break

        return SNAFU(rplusl)


    def toDecimal(self):
        return sum(d*(5**i) for i, d in enumerate(self.digits))
    
    def toSNAFUstr(self):
        return "".join(DIGITSNAFU[d] for d in self.digits[::-1])
    
    def __repr__(self) -> str:
        return repr(self.digits)
    
    def __str__(self) -> str:
        return f"{self.toSNAFUstr()} >> {str(self.toDecimal())}"

def day25_read() -> List[SNAFU]:
    with open("inputs/day25.txt", mode="r+", encoding="utf-8") as f:
        return [SNAFU(line.strip()) for line in f]
    

def day25():
    # x = SNAFU("1=-0-2")
    # y = SNAFU("12111")
    # z = x + y
    # print(str(z))

    # x, y  = 1747, 906
    # z = x + y
    # z = str(z)
    # print(z)
    numbers = day25_read()
    s = sum(numbers)
    print(s)


if __name__ == "__main__":
    day25()
