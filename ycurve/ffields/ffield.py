# Implementation for finity fields
from __future__ import annotations

from ycurve.errors import IncompatibleBaseOperation
from ycurve.ffields.utils import bits

class F2p:
    """
    Representation of fields of order 2**n
    """

    def __init__(self, n:int):
        """
        n: Power of the field. For example 5 would be F(2^5)
        """
        self.n = n

    def __str__(self) -> str:
        return f'F_2**{self.p}({self.n})'

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, y: F2p) -> F2p:
        if y.p != self.p:
            raise IncompatibleBaseOperation(f'Adding numbers with bases {self.p} and {y.p}')
        return F2p(self.n ^ y.n, self.p)

    def __eq__(self, y: F2p) -> bool:
        return self.p == y.p and self.n == y.n
            
    def add(self, x: int, y: int):
        return x^y

    def substract(self, x:int, y:int):
        return self.add(x,y)

    def mul_without_reduction(self, x: int, y: int):
        """
        Right to left comb method for pol multiplication
        Algorithm 2.34
        """
        result = 0
        mask = 1
        i = 0
        while i <= self.n:
            if mask & y:
                result = result ^ x
            x = x << 1
            mask = mask << 1
            i = i + 1

        return result