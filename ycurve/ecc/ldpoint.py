from ycurve.ecc.point import Point, PointCoordinates, AffinePoint


class LDPointChar2(Point):

    def __init__(
        self,
        x: PointCoordinates,
        y: PointCoordinates,
        z: PointCoordinates,
    ):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, q: object) -> bool:
        if isinstance(q, AffinePoint):
            return (
                self.x == q.x and
                self.y == q.y and
                self.z == 1
            )
        elif not isinstance(q, LDPointChar2):
            raise NotImplementedError()

        return (
            self.x == q.x and
            self.y == q.y and
            self.z == q.z
        )

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def is_inf(self):
        return self.x == 1 and self.y == 0 and self.z == 0

    def is_base(self) -> bool:
        return any([a is None for a in [self.x, self.y, self.z]])

    def base_point(self):
        return None
