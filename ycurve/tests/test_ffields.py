from ycurve.ffields.ffield import F2m


def test_sum_correct():
    a_term = F2m(11, 4)
    b_term = F2m(10, 4)

    assert a_term + b_term == F2m(1, 4)
    assert a_term + b_term == a_term - b_term


def test_multiply_inversion():
    a_term = F2m(n=7, m=5)
    b_term = F2m(n=15, m=5)

    product_result = a_term * b_term
    assert product_result == F2m(n=8, m=5)
    assert product_result * a_term.inverse() == b_term
    assert product_result * b_term.inverse() == a_term
