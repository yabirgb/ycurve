from ycurve.ecc.point import Point, PointCoordinates, AffinePoint

class LDPointChar2(Point):

    def __init__(self, x: PointCoordinates, y: PointCoordinates, z: PointCoordinates):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, Q: 'LDPointChar2') -> bool:
        if isinstance(Q, AffinePoint):
            return (
                self.x == Q.x,
                self.y == Q.y,
                self.z == 1,
            )
        elif not isinstance(Q, LDPointChar2):
            raise NotImplementedError()

        
        return (
            self.x == Q.x,
            self.y == Q.y,
            self.z == Q.z,
        )

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def is_inf(self):
        return self.x == 1 and self.y == 0 and self.z == 0