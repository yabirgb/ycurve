from typing import Union, Optional

from ycurve.errors import IncompatibleBaseOperation

class IntegerMod:

    def __init__(self, p: int, n:Optional[int] = None):
        self.p = p
        if n is not None:
            self.n = n % self.p

    def __call__(self, n: int):
        return IntegerMod(self.p, n)

    def __repr__(self):
        return f'Integers mod {self.p}'

    def __add__(self, y: 'IntegerMod'):
        if y.p != self.p:
            IncompatibleBaseOperation(f'Trying to add IntegerMod of different mod: {y.p} and {self.p}')
        return IntegerMod((self.n + y.n), self.p)

    def __eq__(self, y: Union['IntegerMod', int]):
        if isinstance(y, int):
            return self.n == y
        return self.n == y.n

    def __mul__(self, y: Union['IntegerMod', int]):
        return IntegerMod((self.n * y.n), self.p)

    def __sub__(self, y: 'IntegerMod'):
        return IntegerMod((self.n - y.n), self.p)


def Zp(p):
    return IntegerMod(p)