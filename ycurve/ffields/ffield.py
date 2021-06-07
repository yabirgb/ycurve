# Implementation for finity fields
from __future__ import annotations

from functools import reduce
import logging
from typing import List

from ycurve.errors import IncompatibleBaseOperation, UnknownPrimitivePolynom
from ycurve.ffields.utils import bits

log = logging.getLogger(__name__)


# Polynoms from
# http://www.math.rwth-aachen.de/~Frank.Luebeck/data/ConwayPol/CP2.html
PRIMITIVE_CONWAY_POLS = {
    1: [1, 1],
    2: [1, 1, 1],
    3: [1, 0, 1, 1],
    4: [1, 0, 0, 1, 1],
    5: [1, 0, 0, 1, 0, 1],
    6: [1, 0, 1, 1, 0, 1, 1],
    7: [1, 0, 0, 0, 0, 0, 1, 1],
    8: [1, 0, 0, 0, 1, 1, 1, 0, 1],
    9: [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    10: [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
    11: [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    12: [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1],
    13: [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
    14: [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    15: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    16: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    17: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    18: [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    19: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
    20: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    21: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
}

class F2p:
    """
    Representation of fields of order 2**n
    """

    def __init__(self, n:int, gen:int = 0):
        """
        n: Power of the field. For example 5 would be F(2^5)
        """
        self.n = n
        if gen:
            self.generator = gen
        else:
            try:
                self.generator = self.coefs_to_int(PRIMITIVE_CONWAY_POLS[n])
            except KeyError:
                raise UnknownPrimitivePolynom()

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

    def coefs_to_int(self, coefs: List[int]) -> int:
        c = [ x << y for (x, y) in zip(coefs, range(len(coefs)-1, -1, -1))]
        return reduce(lambda x, y: x|y, c)
            
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

    def degree_of(self, f: int) -> int:
        if f == 0:
            return 0
        degree = -1
        while f:
            f >>= 1
            degree += 1
        return degree
        
    def inverse(self, a:int) -> int:
        """
        Computes a ^ -1 mod f
        """
        u, v = a, self.generator
        g1, g2 = 1, 0
        while u != 1:
            j = self.degree_of(u) - self.degree_of(v)
            if j < 0:
                u,v = v, u
                g1, g2 = g2, g1
                j = -j
            u = u ^ (v << j)
            g1 = g1 ^ (g2 << j)

        return g1

    def binary_inversion(self, a:int) -> int:
        u, v = a, self.generator
        g1, g2 = 1, 0
        while 1 not in (u, v):
            print(u, v)
            while 1 & u != 0:
                u >>= 1
                if 1 & g1 != 0:
                    g1 >>= 1
                else:
                    g1 = (g1 ^ self.generator) >> 1
            while 1 & v != 0:
                v >>= 1
                if 1 & g2 != 0:
                    g2 >>= 1
                else:
                    g2 = (g2 ^ self.generator) >> 1

            if self.degree_of(u) > self.degree_of(v):
                u = u ^ v
                g1 = g1 ^ g2
            else:
                v = u ^ v
                g2 = g1 ^ g2
        if u == 1:
            return g1
        return g2