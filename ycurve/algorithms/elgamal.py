import random
from typing import Tuple, Optional

from ycurve.ecc.ecc import Curve
from ycurve.ecc.point import Point


class ElGamal:

    def __init__(self, curve: Curve):
        self.curve = curve

    def encrypt_point(
        self,
        msg: Point,
        publickey: Point,
        seed: Optional[int] = None,
    ) -> Tuple[Point, Point]:

        g = self.curve.base
        m = msg

        if seed:
            random.seed(seed)
        k = random.randint(1, self.curve.order)

        c1 = self.curve.scalar_mul(k, g)
        c2 = self.curve.add(m, self.curve.scalar_mul(k, publickey))
        return c1, c2

    def decrypt_point(
        self,
        private_key: int,
        c1: Point,
        c2: Point,
    ) -> Point:
        p = self.curve.scalar_mul(self.curve.order - private_key, c1)
        return self.curve.add(c2, p)
