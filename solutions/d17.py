from .lib.advent import advent
from .lib.util import Point, Dir
from io import TextIOWrapper
from collections import defaultdict
from dataclasses import dataclass, field
from queue import PriorityQueue

INF = 2**31-1

@dataclass
class Crucible:
    pos: Point
    dir: Dir
    heat_loss: int
    dir_dist: int = 0

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss


@dataclass
class Block:
    cost: int
    pos: Point

    def __repr__(self):
        return f'{self.cost}'


@advent.parser(17)
def parse(file: TextIOWrapper) -> list[list[Block]]:
    return [[Block(int(digit), Point(row, col)) for col, digit in enumerate(line.strip())] for row, line in enumerate(file.readlines())]


@advent.day(17, part=1)
def solve1(grid: list[list[Block]]):
    start = Crucible(Point(0, 0), Dir.E, 0)
    q: PriorityQueue[Crucible] = PriorityQueue()
    q.put(start)
    
    dists = defaultdict(lambda: INF)
    goal = grid[-1][-1].pos

    while not q.empty():
        crucible = q.get()
        if crucible.pos == goal:
            return crucible.heat_loss
        for dir in Dir.all() - {Dir.opposite(crucible.dir)}:
            if (dir == crucible.dir and crucible.dir_dist < 3) or dir != crucible.dir:
                pos = crucible.pos + dir
                if pos.in_bounds(grid):
                    dir_dist = (crucible.dir_dist + 1) if crucible.dir == dir else 1
                    heat_loss = crucible.heat_loss + grid[pos.r][pos.c].cost
                    if heat_loss < dists[(pos, dir, dir_dist)]:
                        dists[(pos, dir, dir_dist)] = heat_loss
                        q.put(Crucible(pos, dir, heat_loss, dir_dist))

@advent.day(17, part=2)
def solve2(grid: list[list[Block]]):
    start = Crucible(Point(0, 0), Dir.E, 0)
    q: PriorityQueue[Crucible] = PriorityQueue()
    q.put(start)
    
    dists = defaultdict(lambda: INF)
    goal = grid[-1][-1].pos

    while not q.empty():
        crucible = q.get()
        if crucible.pos == goal:
            return crucible.heat_loss
        for dir in Dir.all() - {Dir.opposite(crucible.dir)}:
            if (dir == crucible.dir and crucible.dir_dist < 10) or (dir != crucible.dir and crucible.dir_dist >= 4):
                pos = crucible.pos + dir
                if pos.in_bounds(grid):
                    dir_dist = (crucible.dir_dist + 1) if crucible.dir == dir else 1
                    heat_loss = crucible.heat_loss + grid[pos.r][pos.c].cost
                    if heat_loss < dists[(pos, dir, dir_dist)]:
                        dists[(pos, dir, dir_dist)] = heat_loss
                        q.put(Crucible(pos, dir, heat_loss, dir_dist))


def print_path(grid: list[list[Block]], path: list[Point]):
    symbols = {
        Dir.N: '^',
        Dir.S: 'v',
        Dir.E: '>',
        Dir.W: '<'
    }
    prev = Point(0, 0)
    # printed = [[block.cost for block in row] for row in grid]
    total = 0
    printed = [['.' for _ in row] for row in grid]
    for p in path:
        printed[p.r][p.c] = symbols[p - prev]
        prev = p
        total += grid[p.r][p.c].cost
    for r in printed:
        for c in r:
            print(c, end='')
        print()
    print(f'Total = {total}')
# 1110 too high
