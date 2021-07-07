from ycurve.algorithms.elgamal import ElGamal
from ycurve.ecc.point import AffinePoint
from ycurve.ffields.ffield import F2m
from ycurve.tests.fixtures.curves import fixture_k409  # noqa: F401

qx = 0x171b03b1ba0e13d12269bae50ba74a124934b3c0f40da1ee2191154b391e95a9159cdf54cd76bd9cf37fdee5fc16a3b186a0078  # noqa: E501
qy = 0x1dfefc3b383f261f3c53e651aa97748ec837e0e5c90af39e249707a726ad6f449c6488d55e50089a60000cc89053051486e7aa3  # noqa: E501


def test_elgamal(curve_k409):
    e, power, irreducible = curve_k409
    private_key = 0xf42354
    print(e.base)
    publickey = e.scalar_mul(private_key, e.base)

    m0 = F2m(qx, power, irreducible)
    m1 = F2m(qy, power, irreducible)
    m = AffinePoint(m0, m1)
    cipher = ElGamal(e)
    ciphered = cipher.encrypt_point(m, publickey)
    deciphered = cipher.decrypt_point(private_key, ciphered[0], ciphered[1])

    assert deciphered == m
