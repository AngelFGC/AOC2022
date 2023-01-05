from __future__ import annotations
from typing import List

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
    
    def __init__(self, s:str) -> None:
        for c in s[::-1]:
            self.digits.append(SNAFUDIGITS[c])
    
    def __add__(self, other:SNAFU) -> SNAFU:
        pass

    def toDecimal(self):
        s = 0
        for i, d in enumerate(self.digits):
            s += d*(5**i)
        return s
    
    def toSNAFUstr(self):
        s = ""
        for d in self.digits[::-1]:
            s += DIGITSNAFU[d]
        return s
    
    def __repr__(self) -> str:
        return repr(self.digits)
    
    def __str__(self) -> str:
        return f"{self.toSNAFUstr()} >> {str(self.toDecimal())}"

def day24_read():
    with open("inputs/day24.txt", mode="r+", encoding="utf-8") as f:
        return f.readlines()
    

def day25():
    pass

if __name__ == "__main__":
    day25()
