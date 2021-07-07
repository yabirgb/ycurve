from typing import Tuple

from pytest_cases import fixture

from ycurve.ecc.ecc import Char2NonSupersingularCurve
from ycurve.ecc.point import AffinePoint
from ycurve.ffields.ffield import F2m, coefs_pos_to_int

k409_b_x = 0x060f05f658f49c1ad3ab1890f7184210efd0987e307c84c27accfb8f9f67cc2c460189eb5aaaa62ee222eb1b35540cfe9023746  # noqa: E501
k409_b_y = 0x1e369050b7c4e42acba1dacbf04299c3460782f918ea427e6325165e9ea10e3da5f6c42e9c55215aa9ca27a5863ec48d8e0286b  # noqa: E501


@fixture(name='curve_k409')
def fixture_k409() -> Tuple[Char2NonSupersingularCurve, int, int]:
    power = 409
    irreducible = coefs_pos_to_int([409, 87, 0])

    a = F2m(0, power, irreducible)
    b = F2m(1, power, irreducible)

    gx = F2m(k409_b_x, power, irreducible)
    gy = F2m(k409_b_y, power, irreducible)

    g = AffinePoint(gx, gy)
    c = Char2NonSupersingularCurve(a, b)
    c.set_order(0x7ffffffffffffffffffffffffffffffffffffffffffffffffffe5f83b2d4ea20400ec4557d5ed3e3e7ca5b4b5c83b8e01e5fcf)  # noqa: E501
    c.set_base_point(g)

    return (c, power, irreducible)
