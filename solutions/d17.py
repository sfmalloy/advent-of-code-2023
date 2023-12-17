from .lib.advent import advent
from .lib.util import Point, Dir
from io import TextIOWrapper
from collections import deque, defaultdict
from dataclasses import dataclass, field
from queue import PriorityQueue

INF = 2**31-1

@dataclass
class Crucible:
    pos: Point
    dir: Dir
    dist: int
    dir_dist: int = 0
    path: list = field(default_factory=list)

    def __lt__(self, other):
        return self.dist < other.dist


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
    all_dirs = {Dir.N, Dir.S, Dir.E, Dir.W}
    opposite = {
        Dir.N: Dir.S,
        Dir.S: Dir.N,
        Dir.W: Dir.E,
        Dir.E: Dir.W
    }
    
    start = Crucible(Point(0, 0), Dir.E, 0)
    # q = deque([start])
    q: PriorityQueue[Crucible] = PriorityQueue()
    q.put(start)
    dists = defaultdict(lambda: INF)

    goal = grid[-1][-1].pos
    min_heat_loss = INF

    # while len(q) > 0:
    while not q.empty():
        # crucible = q.popleft()
        crucible = q.get()
        if crucible.pos == goal:
            min_heat_loss = min(crucible.dist, min_heat_loss)
            continue
        if dists[(crucible.pos, crucible.dir, crucible.dir_dist)] < crucible.dist:
            continue

        for dir in all_dirs - {opposite[crucible.dir]}:
            if (dir == crucible.dir and crucible.dir_dist < 3) or dir != crucible.dir:
                pos = crucible.pos + dir
                if pos.in_bounds(grid):
                    next_block = grid[pos.r][pos.c]
                    if crucible.dist + next_block.cost < dists[(pos, dir, crucible.dir_dist)]:
                        dists[(pos, dir, crucible.dir_dist)] = crucible.dist + next_block.cost
                        q.put(Crucible(
                            pos,
                            dir,
                            crucible.dist + next_block.cost,
                            (crucible.dir_dist + 1) if crucible.dir == dir else 1,
                            crucible.path + [pos]
                        ))
    return min_heat_loss

@advent.day(17, part=2)
def solve2(ipt):
    return 0


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
