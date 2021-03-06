# -*- coding: utf-8 -*-
"""Aritmética en cuerpos finitos de característica dos

Este módulo permite trabajar con cuerpos binarios. Para usar esta
parte de la biblioteca se debe usar: ::

    from ycurce.ffields import F2m

Para trabjar con :class: F2m debe hacerse de la siguiente manera:

    >>> a, b = F2m(4, 7), F2m(3, 7)
    >>> a + b
    F[2**7](7)
    >>> a * b
    F[2**7](12)
    >>> a.degree()
    3
"""
# Implementation for finity fields
from __future__ import annotations

from functools import reduce
import logging
from typing import List, Tuple

from ycurve.errors import UnknownPrimitivePolynom


log = logging.getLogger(__name__)


# Polynoms from
# http://www.math.rwth-aachen.de/~Frank.Luebeck/data/ConwayPol/CP2.html
PRIMITIVE_CONWAY_POLS = {
    1: [1, 1],
    2: [1, 1, 1],
    3: [1, 0, 1, 1],
    4: [1, 0, 0, 1, 1],
    5: [1, 0, 0, 1, 0, 1],
    6: [1, 0, 1, 1, 0, 1, 1],
    7: [1, 0, 0, 0, 0, 0, 1, 1],
    8: [1, 0, 0, 0, 1, 1, 1, 0, 1],
    9: [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    10: [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
    11: [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    12: [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1],
    13: [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
    14: [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    15: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    16: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    17: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    18: [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    19: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
    20: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    21: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
}


class F2m:
    """
    Representation de elementos en cuerpos de característica dos.
    En esta clase se utilizan enteros para representar polinomios
    binarios. Para ello se utilizan los bits que representan al número
    como coeficientes del polinomio.

    Además interviene un polinomio respecto al que se hacen reducciones módulo.
    La manera de instanciar la clase es por ejemploe::

        F2m(3, 7)

    En este caso se esta instanciando una clase que representa al polinomio
    tres en F_2^7. El polinomio que se utiliza para reducir es tomado de una
    lista precalculada.

    Adevertencia: Esta lista tiene polinomios hasta grado 21. Si se supera este
    grado el usuario está encargado de proveer a la clase con un polinomio
    irreduble válido.
    """

    def __init__(self, n: int, m: int, gen: int = None):
        """
        :ivar n: Entero que representa al polinomio que se instancia.
        :ivar m: Potencia del cuerpo.
        :ivar gen: Polinomio respecto al que se realizan reducciones módulo.
        """
        self.n = n
        self.m = m
        if gen:
            self.generator = gen
        else:
            try:
                self.generator = coefs_to_int(PRIMITIVE_CONWAY_POLS[m])
            except KeyError as e:
                raise UnknownPrimitivePolynom() from e

    def __str__(self) -> str:
        return f'F[2**{self.m}]({self.n})'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, y: object) -> bool:
        if isinstance(y, int):
            return self.n == y
        if not isinstance(y, F2m):
            return NotImplemented
        return (
            self.generator == y.generator and
            self.n == y.n and
            self.m == y.m
        )

    def __add__(self, y: F2m):
        """Opración de suma"""
        return F2m(self.n ^ y.n, self.m, self.generator)

    def __sub__(self, y: F2m):
        """Operación de diferencia"""
        return self.__add__(y)

    def mul_without_reduction(self, x: int, y: int):
        """
        Right to left comb method for pol multiplication
        Algorithm 2.33
        """
        result = 0
        mask = 1
        i = 0
        while i <= self.m:
            if mask & y:
                result = result ^ x
            x = x << 1
            mask = mask << 1
            i = i + 1

        return result

    def __mul__(self, y: F2m):
        """Operador producto"""
        mul = self.mul_without_reduction(self.n, y.n)
        result = self.full_division(
            mul,
            self.generator,
            self.degree_of(mul),
            self.m,
        )[1]

        return F2m(result, self.m, self.generator)

    # pylint: disable=R0201
    def full_division(
        self,
        f: int,
        v: int,
        f_degree: int,
        v_degree: int
    ) -> Tuple[int, int]:
        """
        Computes f(x) = a(x) * v(x) + b(x)
        """
        result = 0
        i = f_degree
        mask = 1 << i
        while i >= v_degree:
            if mask & f:
                result ^= (1 << (i - v_degree))
                f = f ^ (v << (i - v_degree))
            i -= 1
            mask >>= 1
        return (result, f)

    def degree_of(self, f: int) -> int:
        return len(bin(f)[2:])

    def degree(self) -> int:
        """Obtiene el grado del polinomio asociado al entero de la instancia"""
        return len(bin(self.n)[2:])

    def inverse(self) -> F2m:
        """
        Calcula a ^ -1 mod f
        """
        if self.n == 0:
            raise ZeroDivisionError
        a = self.n
        u, v = a, self.generator
        g1, g2 = 1, 0
        while u != 1:
            j = self.degree_of(u) - self.degree_of(v)
            if j < 0:
                u, v = v, u
                g1, g2 = g2, g1
                j = -j
            u = u ^ (v << j)
            g1 = g1 ^ (g2 << j)

        return F2m(n=g1, m=self.m, gen=self.generator)

    def binary_inversion(self, a: int) -> F2m:
        u, v = a, self.generator
        g1, g2 = 1, 0
        while 1 not in (u, v):
            while 1 & u != 0:
                u >>= 1
                if 1 & g1 != 0:
                    g1 >>= 1
                else:
                    g1 = (g1 ^ self.generator) >> 1
            while 1 & v != 0:
                v >>= 1
                if 1 & g2 != 0:
                    g2 >>= 1
                else:
                    g2 = (g2 ^ self.generator) >> 1

            if self.degree_of(u) > self.degree_of(v):
                u = u ^ v
                g1 = g1 ^ g2
            else:
                v = u ^ v
                g2 = g1 ^ g2
        if u == 1:
            return F2m(n=g1, m=self.m, gen=self.generator)
        return F2m(n=g2, m=self.m, gen=self.generator)


def coefs_to_int(coefs: List[int]) -> int:
    c = [x << y for (x, y) in zip(coefs, range(len(coefs)-1, -1, -1))]
    return reduce(lambda x, y: x | y, c)


def coefs_pos_to_int(coefs: List[int]) -> int:
    return reduce(lambda x, y: x | y, [1 << coef for coef in coefs])
