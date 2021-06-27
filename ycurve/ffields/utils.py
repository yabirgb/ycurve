from typing import List


def bits(n: int) -> List[int]:
    return list(map(int, bin(n)[2:]))
