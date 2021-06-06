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

    def strip_powers_of_two(self, c, p, q, gamma, delta):
        c >>= 1
        if p & 1 == 0 and q & 1 == 0:
            p, q = p >> 1, q >> 1
        else:
            p, q = (p ^ delta), ((q ^ gamma) >> 2)

        return c, p, q


    def extended_euclid(self, a, b):
        inita, initb = a, b   # if a and b are given as base-10 ints
        x, prevx = 0, 1
        y, prevy = 1, 0
        while b != 0:
            q = a//b
            a, b = b, a%b
            x, prevx = prevx - q*x, x
            y, prevy = prevy - q*y, y
        print("Euclidean  %d * %d + %d * %d = %d" % (inita, prevx, initb, prevy, a))
        i2b = lambda n: int("{0:b}".format(n))  # convert decimal number to a binary value in a decimal number
        return i2b(a), i2b(prevx), i2b(prevy)  # returns gcd of (a,b), and factors s and t

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
        self.generator = 19
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