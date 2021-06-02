import pytest

from ycurve.rings.zp import Zp
from ycurve.errors import IncompatibleBaseOperation

def test_create_elements():
    Z7 = Zp(7)
    assert Z7(3) == Z7(10)
    assert Z7(5) == 5
    assert Z7(7) == 0

def test_addition():
    Z7 = Zp(7)

    assert Z7(3) + Z7(5) == 1
    assert Z7(3) + Z7(2) == 5