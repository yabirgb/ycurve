import pytest

from ycurve.ffields.ffield import F2m
from ycurve.ecc.point import AffinePoint
from ycurve.errors import InvalidPoint
from ycurve.tests.fixtures.curves import fixture_k409  # noqa: F401

px = 0xbb211afe3cd3b8dd09d7eebe164ec4c7545644f8fc77b8717a68780275415f2164dbdfa68c68c9b31da7f6cd6bcc6ca3fe24ea  # noqa: E501
py = 0x1ee223ed628c39a048205b69bb9c39d772479507a409188400690932e36527dde84c85dbef10a7097a0026083786881fe778049  # noqa: E501
qx = 0x171b03b1ba0e13d12269bae50ba74a124934b3c0f40da1ee2191154b391e95a9159cdf54cd76bd9cf37fdee5fc16a3b186a0078  # noqa: E501
qy = 0x1dfefc3b383f261f3c53e651aa97748ec837e0e5c90af39e249707a726ad6f449c6488d55e50089a60000cc89053051486e7aa3  # noqa: E501


def test_addition(curve_k409):
    e, power, irreducible = curve_k409
    p0 = F2m(px, power, irreducible)
    p1 = F2m(py, power, irreducible)

    q0 = F2m(qx, power, irreducible)
    q1 = F2m(qy, power, irreducible)

    p = AffinePoint(p0, p1)
    q = AffinePoint(q0, q1)

    pq = e.add(p, q)
    assert pq.x == 0x18def7e87e321eae941cab93855a99d2cfcfcf453b9acee13a0286ce064eb5dec735043badd55145fa60cf30578462c564ca966  # noqa: E501
    assert pq.y == 0x1ee927c846f6f215ce2f659153d68efcabf0f116618e3c395519787171e9314d092b01dafeea3503817ed7537649964636481a8  # noqa: E501
    assert e.add(p, q) == e.add(q, p)


def test_double(curve_k409):
    e, power, irreducible = curve_k409
    p0 = F2m(px, power, irreducible)
    p1 = F2m(py, power, irreducible)

    p = AffinePoint(p0, p1)
    pq_double = e.double(p)
    assert pq_double.x == 0x1574f7c0c67af8ae69ea928f7c29be520a729a3bca47cfbc5f2f3d748a959a4238697361029233b82c36e58dd141d84dab87b42  # noqa: E501
    assert pq_double.y == 0x1e26bdee445c0955ee91c4fca385016db6d03f852a4cb1bf0e4f68f38cd6580ff22b2b9b47efe6c99af7483027e45af9adf981  # noqa: E501


def test_scalar_mul_2(curve_k409):
    e, power, irreducible = curve_k409
    p0 = F2m(px, power, irreducible)
    p1 = F2m(py, power, irreducible)

    p = AffinePoint(p0, p1)
    product = e.scalar_mul(2, p)
    assert product == e.double(p)

    product = e.scalar_mul(3, p)
    assert product == e.add(e.double(p), p)


def test_contains(curve_k409):
    e, power, irreducible = curve_k409
    p0 = F2m(px, power, irreducible)
    p1 = F2m(py, power, irreducible)

    p = AffinePoint(p0, p1)
    assert e.contains(p)

    p0 = F2m(2, power, irreducible)
    p1 = F2m(3, power, irreducible)
    pp = AffinePoint(p0, p1)
    assert not e.contains(pp)

    with pytest.raises(InvalidPoint):
        e.add(p, pp)


def test_scalar_mul(curve_k409):
    e, power, irreducible = curve_k409
    p0 = F2m(0x5748c255cdbd3c0eeea451185220053e2607f6cd3bd6926a9fa986e4bcb280577b75f8c5a64f258bb30d9d87599b01b3244a6e, power, irreducible)  # noqa: E501
    p1 = F2m(0x120da17e18447580a3aed9e6e56c527b092a77b832a1b2335545af916d13d3d198fb2434131c2c8f77475ab785480cde7139123, power, irreducible)  # noqa: E501

    p = AffinePoint(p0, p1)
    product = e.scalar_mul(0xff23423432, p)  # noqa: E501
    assert product.x == 0x1dc4a6cd7088b2fd3a6c340f1427c79589eae0246eb6106bd5f1ac32b941d398db4071cba20bdfb3c7ba795e9021c60bb16462  # noqa: E501
    assert product.y == 0x1139e507e111751ca49a85fb417eb86a89ea340e76bfab2d3a191c6ac1fb4fa7e8c98eccd654e85f96a0cb484cf72f41f1256be  # noqa: E501
