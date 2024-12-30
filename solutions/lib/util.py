from dataclasses import dataclass
from typing import Self
from math import sqrt


@dataclass(frozen=True, eq=True, order=True)
class Point:
    r: int
    c: int

    def __add__(self, other: Self):
        return Point(self.r + other.r, self.c + other.c)
    
    def __sub__(self, other: Self):
        return Point(self.r - other.r, self.c - other.c)
        
    def in_bounds(self, grid: list[list]):
        return self.r >= 0 and self.c >= 0 and self.r < len(grid) and self.c < len(grid[self.r])

    def dist(self, other: Self) -> float:
        return sqrt((self.r - other.r)**2 + (self.c - other.c)**2)

    def mdist(self, other: Self):
        return abs(self.r - other.r) + abs(self.c - other.c)
    
    def __repr__(self) -> str:
        return f'({self.r}, {self.c})'


@dataclass(frozen=True, eq=True, order=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: Self):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Self):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)
    
    def __rmul__(self, other: int):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __floordiv__(self, other: int):
        return Vec2(self.x // other, self.y // other)

    def dot(self, other: Self):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: Self):
        return self.x*other.y - self.y*other.x
    
    def dist(self, other: Self) -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def mdist(self, other: Self):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def magnitude(self):
        return sqrt(self.dot(self))

    def normalized(self):
        return self / self.magnitude()

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


@dataclass(frozen=True, eq=True, order=True)
class Vec3:
    x: int
    y: int
    z: int

    def __add__(self, other: Self):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Self):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, val):
        return Vec3(self.x * val, self.y * val, self.z * val)
    
    def __rmul__(self, val: int):
        return self.__mul__(val)
    
    def __truediv__(self, val):
        return Vec3(self.x / val, self.y / val, self.z / val)

    def __floordiv__(self, val: int):
        return Vec3(self.x // val, self.y // val, self.z // val)

    def dot(self, other: Self):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def dist(self, other: Self) -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    def mdist(self, other: Self):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def magnitude(self):
        return sqrt(self.dot(self))

    def normalized(self):
        return self / self.magnitude()

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'



class PointDir:
    N = Point(-1, 0)
    S = Point(1, 0)
    E = Point(0, 1)
    W = Point(0, -1)

    L = W
    R = E
    U = N
    D = S

    _opposite = {
        N: S,
        S: N,
        E: W,
        W: E
    }

    _all = {N, S, E, W}

    @staticmethod
    def opposite(d: Self):
        return PointDir._opposite[d]
    
    @staticmethod
    def all():
        return PointDir._all


class Vec2Dir:
    N = Vec2(0, 1)
    S = Vec2(0, -1)
    E = Vec2(1, 0)
    W = Vec2(-1, 0)

    L = W
    R = E
    U = N
    D = S

    _opposite = {
        N: S,
        S: N,
        E: W,
        W: E
    }

    _all = {N, S, E, W}

    @staticmethod
    def opposite(d: Self):
        return Vec2._opposite[d]
    
    @staticmethod
    def all():
        return Vec2._all

def print_grid(grid: list[list]) -> None:
    for row in grid:
        for col in row:
            print(col, end='')
        print()
