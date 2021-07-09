# -*- coding: utf-8 -*-
"""
Implementación del sistema criptográfico de el Gamal.
"""
import random
from typing import Tuple, Optional

from ycurve.ecc.ecc import Curve
from ycurve.ecc.point import Point


class ElGamal:
    """
    Implementación del criptosistema del Gamal

    :ivar curve: Curva sobre la que se va a trabajar
    """

    def __init__(self, curve: Curve):
        self.curve = curve

    def encrypt_point(
        self,
        msg: Point,
        publickey: Point,
        seed: Optional[int] = None,
    ) -> Tuple[Point, Point]:
        """
        Dado un punto de la curva que representa un mensaje, cifra el contenido
        de acuerdo al algoritmo de el gamal.

        :ivar msg: Mensaje que se quiere cifrar
        :ivar publickey: Llave pública usada en el criptosistema
        :ivar seed: Semilla para la elección en procesos aleatorios
        """

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
        """
        Descifra un mensaje cifrado mediante el método del gamal

        :ivar private_key: Llave privada del sistma
        :ivar c1: primera componente resultado de cifrar el mensaje
        :ivar c2: segunda componente resultado de cifrar el mensaje
        """
        p = self.curve.scalar_mul(self.curve.order - private_key, c1)
        return self.curve.add(c2, p)
