from ycurve.ecc.ecc import Char2Curve
from ycurve.ffields.ffield import F2m
from ycurve.ecc.ldpoint import LDPointChar2
from ycurve.ecc.point import AffinePoint


def test_addition():
    a = F2m(1, 3)
    b = F2m(1, 3)

    e = Char2Curve(a, b, 3)

    inf = LDPointChar2(F2m(1, 3), F2m(0, 3), F2m(0, 3))
    q = AffinePoint(F2m(2, 3), F2m(5, 3))
    # P is infinity
    assert e.add(inf, q) == q

    # Opposite points
    p = LDPointChar2(F2m(0, 3), F2m(1, 3), F2m(1, 3))
    minus_p = LDPointChar2(F2m(0, 3), F2m(1, 3) + F2m(0, 3), F2m(1, 3))

    assert e.add(p, minus_p) == inf

    # Doubling
    p = LDPointChar2(F2m(0, 3), F2m(1, 3), F2m(1, 3))
    q = AffinePoint(F2m(2, 3), F2m(5, 3))
    double = e.double(p)
    add_double = e.add(p, p)
    assert double == add_double

    #p_3 = e.scalar_mul(3, p, LDPointChar2(F2m(1, 3), F2m(0, 3), F2m(0, 3)))
    #assert p_3 == e.add(double, p)