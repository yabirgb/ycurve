from ycurve.ffields.utils import bits


def test_binary_conversion():
    assert bits(13) == [1, 1, 0, 1]
    assert bits(1) == [1]
    assert bits(0) == [0]
