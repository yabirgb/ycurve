from abc import ABC, abstractmethod
from typing import Union, Any

from ycurve.ffields.ffield import F2m

PointCoordinates = Union[
    int,
    F2m,
]


class Point:
    
    @abstractmethod
    def is_inf(self) -> bool:
        pass

    @abstractmethod
    def double(self, a: Any, b: Any) -> 'Point':
        pass

class AffinePoint(Point):

    def __init__(self, x: PointCoordinates, y: PointCoordinates):
        self.x = x
        self.y = y