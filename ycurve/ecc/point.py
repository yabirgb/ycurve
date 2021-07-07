from abc import ABC, abstractmethod
from typing import Union, Optional

from ycurve.ffields.ffield import F2m

PointCoordinates = Union[F2m]


class Point(ABC):

    @abstractmethod
    def is_inf(self) -> bool:
        pass

    @abstractmethod
    def base_point(self) -> Optional['Point']:
        pass


class AffinePoint(Point):

    def __init__(self, x: Optional[PointCoordinates], y: PointCoordinates):
        self.x = x
        self.y = y

    def is_base(self) -> bool:
        return any([a is None for a in [self.x, self.y]])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AffinePoint):
            return False
        return self.x == other.x and self.y == other.y

    def is_inf(self):
        return None

    def base_point(self):
        return None

    def __str__(self):
        if isinstance(self.x, F2m):
            x, y = self.x.n, self.y.n
        elif self.x is None:
            return '[ ]'
        else:
            x, y = self.x, self.y
        return f'({hex(x)},{hex(y)})'
