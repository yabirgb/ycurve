from abc import ABC, abstractmethod
from typing import Union, Any

from ycurve.ffields.ffield import F2m

PointCoordinates = Union[
    int,
    F2m,
]


class Point(ABC):

    @abstractmethod
    def is_inf(self) -> bool:
        pass


    @abstractmethod
    def base_point() -> 'Point':
        return None


class AffinePoint(Point):

    def __init__(self, x: PointCoordinates, y: PointCoordinates):
        self.x = x
        self.y = y


    def is_base(self) -> bool:
        return any([a is None for a in [self.x, self.y]])

    def __eq__(self, other: 'AffinePoint') -> bool:
        return self.x == other.x and self.y == other.y

    def is_inf(self):
        return None

    def base_point(self) -> 'LDPointChar2':
        return None

    def __str__(self):
        if isinstance(self.x, F2m):
            x, y = self.x.n, self.y.n
        elif self.x is None:
            return '[ ]'
        else:
            x, y = self.x, self.y
        return f'({hex(x)},{hex(y)})' 