# type: ignore
from abc import ABC, abstractmethod

from ycurve.ffields.ffield import F2m
from ycurve.ecc.ldpoint import LDPointChar2
from ycurve.ecc.point import AffinePoint, Point
from ycurve.errors import InvalidPoint


class Curve(ABC):

    @abstractmethod
    def double(self, p: Point) -> Point:
        pass

    @abstractmethod
    def add(self, p: Point, q: Point) -> Point:
        pass

    @abstractmethod
    def contains(self, p: Point) -> bool:
        pass

    def scalar_mul(self, k: int, p: Point) -> Point:
        if isinstance(p, AffinePoint):
            output = AffinePoint(None, F2m(0, 3))
        else:
            return AffinePoint(None, F2m(0, 3))
        #   while k > 0:
        #    if k % 2 == 1:
        #        output = self.add(output, p)
        #    p = self.double(p)
        #    k //= 2
        bin_k = "".join(bin(k)[2:])
        for i, ki in enumerate(bin_k):
            print(output, f'{i}/{len(bin_k)}')
            output = self.double(output)
            if ki == '1':
                output = self.add(p, output)
        return output


class Char2NonSupersingularCurve(Curve):

    def __init__(self, a: F2m, b: F2m):
        self.a = a
        self.b = b

    def contains(self, p: Point) -> bool:
        left = p.y * p.y + p.x * p.y
        rigth = p.x * p.x * p.x + self.a * p.x * p.x + self.b
        return left == rigth

    def add(self, p: AffinePoint, q: AffinePoint) -> AffinePoint:
        if p.x is None:
            return q
        if q.x is None:
            return p
        if not self.contains(q):
            raise InvalidPoint()
        if p == q:
            return self.double(p)
        t0 = p.y + q.y
        t1 = p.x + q.x
        if t1 == 0:
            # p = q o p = -q
            return AffinePoint(None, 0)
        t3 = t1.inverse()
        lmd = t0 * t3
        lmd_2 = lmd * lmd

        x3 = lmd_2 + lmd
        x3 = x3 + p.x + q.x + self.a
        y3 = lmd * (p.x + x3) + x3 + p.y
        assert self.contains(AffinePoint(x3, y3))
        return AffinePoint(x3, y3)

    def double(self, p: AffinePoint) -> AffinePoint:
        if p.x == 0:
            raise ZeroDivisionError
        elif p.x is None:
            return p
        if not self.contains(p):
            raise InvalidPoint(p)
        x1_inv = p.x.inverse()
        x1_2 = p.x * p.x
        t0 = p.y * x1_inv
        lmd = p.x + t0
        x3 = lmd * lmd + lmd + self.a
        y3 = x1_2 + x3 + x3 * lmd
        return AffinePoint(x3, y3)


class Char2Curve(Char2NonSupersingularCurve):

    def double(self, p: LDPointChar2):
        # If it is infinity point
        if p.is_inf():
            return LDPointChar2(F2m(3, 1), F2m(3, 1), F2m(3, 0))
        t1 = p.z * p.z
        t2 = p.z * p.x
        z3 = t1 * t2
        x3 = t2 * t2
        t1 = t1 * t1
        t2 = t1 * self.b
        x3 = x3 + t2
        t1 = p.y * p.y
        if self.a == 1:
            t1 = t1 + z3
        t1 = t1 + t2
        y3 = x3 * t1
        t1 = t2 * z3
        y3 = y3 + t1
        return LDPointChar2(x3, y3, z3)

    def add(self, p: LDPointChar2, q: AffinePoint) -> LDPointChar2:
        m = self.a.m
        if q.is_inf():
            return p
        if p.is_inf():
            return LDPointChar2(q.x, q.y, 1)
        t1 = p.z * q.x
        t2 = p.z * p.z
        x3 = p.x + t1
        t1 = p.z * x3
        t3 = t2 * q.y
        y3 = p.y + t3
        if x3 == 0:
            if y3 == 0:
                # case P == Q
                return self.double(
                    LDPointChar2(
                        F2m(q.x.n, m),
                        F2m(q.y.n, m),
                        F2m(1, m)
                    )
                )
            else:
                # case P == -Q
                return LDPointChar2(
                    F2m(1, m),
                    F2m(1, m),
                    F2m(0, m),
                )

        z3 = t1 * t1
        t3 = t1 * y3
        if self.a == 1:
            t1 = t1 + t2
        t2 = x3 * x3
        x3 = t2 * t1
        t2 = y3 * y3
        x3 = x3 + t2
        x3 = x3 + t3
        t2 = q.x * z3
        t2 = t2 + x3
        t1 = z3 * z3
        t3 = t3 + t2
        y3 = t3 * t2
        t2 = q.x + q.y
        t3 = t1 * t2
        y3 = y3 + t3
        return LDPointChar2(x3, y3, z3)


class Char2SupersingularCurve(Curve):

    def __init__(self, a: F2m, b: F2m, c: F2m):
        self.a = a
        self.b = b
        self.c = c

    def add(self, p: AffinePoint, q: AffinePoint) -> AffinePoint:
        if p.x is None:
            return q
        if q.x is None:
            return p
        y_12 = p.y + q.y
        x_12 = p.x + q.x
        t0 = x_12.inverse()
        t1 = y_12 * t0
        t2 = t1 * t1
        x3 = t2 + x_12
        x_31 = p.x + x3
        y3_pre = t1 * x_31
        t4 = p.y + self.c
        y3 = y3_pre + t4

        return AffinePoint(x3, y3)

    def double(self, p: AffinePoint) -> AffinePoint:
        if self.c == 0:
            raise ZeroDivisionError
        elif p.x is None:
            return p
        x_11 = p.x * p.x
        c_m1 = self.c.inverse()
        x_1a = x_11 + self.a
        t0 = x_1a * c_m1
        x3 = t0 * t0
        x_13 = p.x + x3
        y3_pre = t0 * x_13
        t1 = p.y + self.c
        y3 = y3_pre + t1

        return AffinePoint(x3, y3)
