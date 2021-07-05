from ycurve.ecc.ecc import Char2NonSupersingularCurve
from ycurve.ffields.ffield import F2m, coefs_pos_to_int
from ycurve.ecc.ldpoint import LDPointChar2
from ycurve.ecc.point import AffinePoint
from ycurve.tests.fixtures.curves import fixture_k409

def test_addition(curve_K409):
    e, power, irreducible = curve_K409
    p0 = F2m(0xbb211afe3cd3b8dd09d7eebe164ec4c7545644f8fc77b8717a68780275415f2164dbdfa68c68c9b31da7f6cd6bcc6ca3fe24ea, power, irreducible)
    p1 = F2m(0x1ee223ed628c39a048205b69bb9c39d772479507a409188400690932e36527dde84c85dbef10a7097a0026083786881fe778049, power, irreducible)
    
    q0 = F2m(0x171b03b1ba0e13d12269bae50ba74a124934b3c0f40da1ee2191154b391e95a9159cdf54cd76bd9cf37fdee5fc16a3b186a0078, power, irreducible)
    q1 = F2m(0x1dfefc3b383f261f3c53e651aa97748ec837e0e5c90af39e249707a726ad6f449c6488d55e50089a60000cc89053051486e7aa3, power, irreducible)
    
    p = AffinePoint(p0, p1)
    q = AffinePoint(q0, q1)

    pq = e.add(p, q)
    assert pq.x == 0x18def7e87e321eae941cab93855a99d2cfcfcf453b9acee13a0286ce064eb5dec735043badd55145fa60cf30578462c564ca966
    assert pq.y == 0x1ee927c846f6f215ce2f659153d68efcabf0f116618e3c395519787171e9314d092b01dafeea3503817ed7537649964636481a8

def test_double(curve_K409):
    e, power, irreducible = curve_K409
    p0 = F2m(0xbb211afe3cd3b8dd09d7eebe164ec4c7545644f8fc77b8717a68780275415f2164dbdfa68c68c9b31da7f6cd6bcc6ca3fe24ea, power, irreducible)
    p1 = F2m(0x1ee223ed628c39a048205b69bb9c39d772479507a409188400690932e36527dde84c85dbef10a7097a0026083786881fe778049, power, irreducible)

    p = AffinePoint(p0, p1)
    pq_double = e.double(p)
    assert pq_double.x == 0x1574f7c0c67af8ae69ea928f7c29be520a729a3bca47cfbc5f2f3d748a959a4238697361029233b82c36e58dd141d84dab87b42
    assert pq_double.y == 0x1e26bdee445c0955ee91c4fca385016db6d03f852a4cb1bf0e4f68f38cd6580ff22b2b9b47efe6c99af7483027e45af9adf981

def test_scalar_mul_2(curve_K409):
    e, power, irreducible = curve_K409
    p0 = F2m(0xbb211afe3cd3b8dd09d7eebe164ec4c7545644f8fc77b8717a68780275415f2164dbdfa68c68c9b31da7f6cd6bcc6ca3fe24ea, power, irreducible)
    p1 = F2m(0x1ee223ed628c39a048205b69bb9c39d772479507a409188400690932e36527dde84c85dbef10a7097a0026083786881fe778049, power, irreducible)

    p = AffinePoint(p0, p1)
    product = e.scalar_mul(2, p)
    assert product == e.double(p)

    product = e.scalar_mul(3, p)
    assert product == e.add(e.double(p), p)

def test_scalar_mul(curve_K409):
    e, power, irreducible = curve_K409
    p0 = F2m(0xbb211afe3cd3b8dd09d7eebe164ec4c7545644f8fc77b8717a68780275415f2164dbdfa68c68c9b31da7f6cd6bcc6ca3fe24ea, power, irreducible)
    p1 = F2m(0x1ee223ed628c39a048205b69bb9c39d772479507a409188400690932e36527dde84c85dbef10a7097a0026083786881fe778049, power, irreducible)

    p = AffinePoint(p0, p1)
    product = e.scalar_mul(0xfffffe213213478555676765756342323442353523454534534534534534213, p)
    # print(product)
    # assert product.x == 0xe8e95ecca5b663f2fd176c959dd78626eb2c190b099462a753b5ae6f35e5304a1c41d7754e6050bee264b28e05285da1e77430
    # assert product.y == 0x834d99db2167b8f9c44c59457e29ef3eeac72e94763552bc1909116ea26173f0ec75c55ab359d830990e0e3fd2e6a86c38ce0a
