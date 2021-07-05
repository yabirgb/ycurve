import pytest

from pytest_cases import fixture

from ycurve.ecc.ecc import Char2NonSupersingularCurve
from ycurve.ffields.ffield import F2m, coefs_pos_to_int


@fixture(name='curve_K409')
def fixture_k409() -> (Char2NonSupersingularCurve, int):
    power = 409
    irreducible = coefs_pos_to_int([409, 87, 0])

    a = F2m(0, power, irreducible)
    b = F2m(1, power, irreducible)

    return (Char2NonSupersingularCurve(a, b), power,irreducible)