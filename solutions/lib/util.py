from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True, eq=True)
class Point:
    r: int
    c: int

    def __add__(self, other: Self):
        return Point(self.r + other.r, self.c + other.c)
    
    def __sub__(self, other: Self):
        return Point(self.r - other.r, self.c - other.c)
    
    def in_bounds(self, grid: list[list]):
        return self.r >= 0 and self.c >= 0 and self.r < len(grid) and self.c < len(grid[self.r])

    def mdist(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)


class Dir:
    N = Point(-1, 0)
    S = Point(1, 0)
    E = Point(0, 1)
    W = Point(0, -1)


def print_grid(grid: list[list]) -> None:
    for row in grid:
        for col in row:
            print(col, end='')
        print()
