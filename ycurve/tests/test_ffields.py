import pytest

from ycurve.ffields.ffield import F2p
from ycurve.errors import IncompatibleBaseOperation

def test_sum_correct():
    a = F2p(11, 4)
    b = F2p(10, 4)
    assert F2p(1, 4) == a + b

def test_sum_incompatible_base():
    a = F2p(11, 2)
    b = F2p(10, 4)

    with pytest.raises(IncompatibleBaseOperation):
        a + b

def test_euclides():
    GF16 = F2p(4)

    a = GF16.inverse(7)
    print(a)
    a = GF16.inverse(5)
    print(a)
    assert False