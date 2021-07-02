from abc import ABC, abstractmethod
from typing import Optional


from ycurve.ffields.ffield import F2m
from ycurve.ecc.ldpoint import LDPointChar2
from ycurve.ecc.point import AffinePoint, Point


class Curve(ABC):

    @abstractmethod
    def double(self, P: Point) -> Point:
        pass

    @abstractmethod
    def add(self, P: Point, Q: Point) -> Point:
        pass

    @abstractmethod
    def multiply(self, k: int, P: Point) -> Point:
        pass


class FqCurve(Curve):

    def __init__(self, a: F2m, b: F2m, p: int, n: int, irreducible: int):
        pass


class Char2Curve(Curve):
    def __init__(self, a: F2m, b: F2m, m:int, irreducible: Optional[int] = None):
        """
        Represents a point in Elliptic curve over F2m with equation
        y^2 + x y = x^3 + a x^2 + b

        a: Coefficient of x^2 in the equation of the curve
        b: Indpendt term in the equation of the curve
        m: Power of the field F2m
        irreducible: Irreducible polynom of the field F2m
        """

        self.a = a
        self.b = b
        self.m = m
        self.irreducible = irreducible

    def double(self, P: LDPointChar2):
        # If it is infinity point
        if P.is_inf():
            return LDPointChar2(1, 0, 0)
        t1 = P.z * P.z
        t2 = P.z * P.x
        z3 = t1 * t2
        x3 = t2 * t2
        t1 = t1 * t1
        t2 = t1 * self.b
        x3 = x3 + t2
        t1 = P.y * P.y
        if self.a == 1:
            t1 = t1 + z3
        t1 = t1 + t2
        y3 = x3 * t1
        t1 = t2 * z3
        y3 = y3 + t1
        return LDPointChar2(x3, y3, z3)

    def add(self, P: LDPointChar2, Q: AffinePoint) -> LDPointChar2:
        if Q.is_inf():
            return P
        if P.is_inf():
            return LDPointChar2(Q.x, Q.y, 1)
        t1 = P.z * Q.x
        t2 = P.z * P.z
        x3 = P.x + t1
        t1 = P.z * x3
        t3 = t2 * Q.y
        y3 = P.y + t3
        if x3 == 0:
            if y3 == 0:
                # case P == Q
                return self.double(
                    LDPointChar2(
                        F2m(Q.x.n, self.m),
                        F2m(Q.y.n, self.m),
                        F2m(1, self.m)
                    )
                )
            else:
                # case P == -Q
                return LDPointChar2(F2m(1, self.m), F2m(1, self.m), F2m(0, self.m))

        z3 = t1 * t1
        t3 = t1 * y3
        if self.a == 1:
            t1 = t1 + t2
        t2 = x3 * x3
        x3 = t2 * t1
        y2 = y3 * y3
        x3 = x3 + t2
        x3 = x3 + t3
        t2 = Q.x * z3
        t2 = t2 + x3
        t1 = z3 * z3
        t3 = t3 + t2
        y3 = t3 * t2
        t2 = Q.x + Q.y
        t3 = t1 * t2
        y3 = y3 + t3
        return LDPointChar2(x3, y3, z3)

    def multiply(self, k: int, P: Point) -> Point:
        pass