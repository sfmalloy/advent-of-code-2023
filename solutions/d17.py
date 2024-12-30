import heapq
from .lib.advent import advent
from .lib.util import Point, PointDir
from io import TextIOWrapper
from collections import defaultdict
from dataclasses import dataclass

INF = 2**31-1

@dataclass
class Crucible:
    pos: Point
    dir: PointDir
    heat_loss: int
    dir_dist: int = 0

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss


@dataclass
class Block:
    cost: int
    pos: Point


@advent.parser(17)
def parse(file: TextIOWrapper) -> list[list[Block]]:
    return [[Block(int(digit), Point(row, col)) for col, digit in enumerate(line.strip())] 
            for row, line in enumerate(file.readlines())]


@advent.day(17, part=1)
def solve1(grid: list[list[Block]]):
    return follow_path(grid, 3)


@advent.day(17, part=2)
def solve2(grid: list[list[Block]]):
    return follow_path(grid, 10, 4)


def follow_path(grid: list[list[Block]], max_dir_dist: int, min_dir_dist: int=1):
    start = Crucible(Point(0, 0), PointDir.E, 0)
    q: list[Crucible] = []
    heapq.heappush(q, start)

    dists = defaultdict(lambda: INF)
    goal = grid[-1][-1].pos

    while q:
        crucible = heapq.heappop(q)
        if crucible.pos == goal:
            return crucible.heat_loss
        for dir in PointDir.all - {PointDir.opposite(crucible.dir)}:
            if (dir != crucible.dir or crucible.dir_dist >= max_dir_dist) and (dir == crucible.dir or crucible.dir_dist < min_dir_dist):
                continue
            pos = crucible.pos + dir
            if not pos.in_bounds(grid):
                continue
            dir_dist = (crucible.dir_dist + 1) if crucible.dir == dir else 1
            heat_loss = crucible.heat_loss + grid[pos.r][pos.c].cost
            if heat_loss < dists[(pos, dir, dir_dist)]:
                dists[(pos, dir, dir_dist)] = heat_loss
                heapq.heappush(q, Crucible(pos, dir, heat_loss, dir_dist))
