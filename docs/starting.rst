Comenzando con ycurve
=====================

===========
Instalación
===========

ycurve es una librería escrita en python que permite trabajar con curvas elípticas en característica
dos. El proyecto es de código abierto y se encuentra disponible en https://github.com/yabirgb/ycurve .

Para instalar la librería localmente podemos hacer::

    git clone https://github.com/yabirgb/ycurve.git
    cd ycurve
    pip3 install -U .

O de manera directa::

    pip install git+https://github.com/yabirgb/ycurve.git

===
Uso
===

Una vez instalada la librería, para poder usarla solo tenemos que
importarla desde el interprete de python. Bien la librería completa
con::

    >>> import ycurve

O bien mediante algún módulo concreto::

    >>> from ycurce.ffields import F2m
    >>> a, b = F2m(4, 7), F2m(3, 7)
    >>> a + b
    F[2**7](7)
    >>> a * b
    F[2**7](12)
    >>> a.degree()
    3

Puede encontrar toda la documentación respecto al proyecto en

.. autosummary::
   ffield
   ecc
   elgamal