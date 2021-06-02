from typing import List

def bits(n: int) -> List[bool]:
    return list(map(int, bin(n)[2:]))
