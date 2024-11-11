from math import inf
from constants import HEIGHT, WIDTH
from geometry.point import Point
from decimal import Decimal as D

EdgeTuple = tuple[tuple[D, ...], tuple[D, ...]]

class Edge:
    def __init__(self, a: Point, b: Point, finished: bool = False) -> None:
        self.a = a
        self.b = b
        self.finished = finished

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return False

        return self.a == other.a and self.b == other.b

    def __str__ (self) -> str:
        return f"Edge({self.a}, {self.b})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(repr(self))

    @property
    def border_edge(self) -> bool:
        return self.a.x == self.b.x == -inf or self.a.x == self.b.x == inf

    @property
    def point_edge(self) -> bool:
        return self.a == self.b

    @property
    def slope(self) -> D:
        if self.a == self.b:
            return D("nan")

        if self.a.x == self.b.x:
            return D("inf")

        return (self.a.y - self.b.y) / (self.a.x - self.b.x)

    def f(self, x: D | int | float) -> D:
        return self.slope * (D(x) - self.a.x) + self.a.y

    def to_tuple(self) -> EdgeTuple:
        return tuple(self.a), tuple(self.b)

    def extend(self) -> Edge:
        if self.slope == D("nan"):
            return self

        if self.slope == D("inf"):
            if self.a.y == D("inf"):
                self.a.y = HEIGHT

            self.b.y = -HEIGHT if self.b.y < self.a.y else HEIGHT

        elif self.b.x < self.a.x:
            self.b.x, self.b.y = -WIDTH, self.f(-WIDTH)

        elif self.b.x > self.a.x:
            self.b.x, self.b.y = WIDTH, self.f(WIDTH)

        return self

    def bound(self) -> Edge:
        for point in [self.a, self.b]:
            if point.x == D("inf"):
                point.x = WIDTH
            elif point.x == D("-inf"):
                point.x = -WIDTH

            if point.y == D("inf"):
                point.y = HEIGHT
            elif point.y == D("-inf"):
                point.y = -HEIGHT

        return self

    @staticmethod
    def center(edge: EdgeTuple) -> tuple[tuple[float, float], ...]:
        return Point.center(edge[0]), Point.center(edge[1])

    @staticmethod
    def uncenter(edge: EdgeTuple) -> tuple[tuple[float, float], ...]:
        return Point.uncenter(edge[0]), Point.uncenter(edge[1])