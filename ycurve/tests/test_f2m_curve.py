from ycurve.ecc.ecc import Char2Curve
from ycurve.ffields.ffield import F2m
from ycurve.ecc.ldpoint import LDPointChar2
from ycurve.ecc.point import AffinePoint

def test_addition():
    a = F2m(1, 3)
    b = F2m(1, 3)

    E = Char2Curve(a, b, 3)

    inf = LDPointChar2(F2m(1, 3), F2m(1, 3), F2m(0, 3))
    Q = AffinePoint(F2m(2, 3), F2m(5, 3))
    # P is infinity
    assert E.add(inf, Q) == Q

    # Opposite points
    P = LDPointChar2(F2m(0, 3), F2m(1, 3), F2m(1, 3))
    minusP = LDPointChar2(F2m(0, 3), F2m(1, 3) + F2m(0, 3), F2m(1, 3))

    assert E.add(P, minusP) == inf

    # Doubling
    P = LDPointChar2(F2m(0, 3), F2m(1, 3), F2m(1, 3))
    Q = AffinePoint(F2m(2, 3), F2m(5, 3))
    double = E.double(P)
    add_double = E.add(P, P)
    assert double == add_double