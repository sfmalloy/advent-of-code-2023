from .lib.advent import advent
from .lib.util import Point, Dir
from io import TextIOWrapper
from dataclasses import dataclass, field
from collections import deque


@dataclass(frozen=True, eq=True)
class Beam:
    pos: Point
    dir: Dir


@dataclass
class Tile:
    type: str
    visited_by: set[int] = field(default_factory=set)

    def reset(self):
        if len(self.visited_by) > 0:
            self.visited_by.clear()


@advent.parser(16)
def parse(file: TextIOWrapper) -> list[list[Tile]]:
    return [list(map(Tile, line.strip())) for line in file.readlines()]


@advent.day(16, part=1)
def solve1(grid: list[list[Tile]]) -> int:
    return energize(grid, Beam(Point(0, 0), Dir.E))


@advent.day(16, part=2)
def solve2(grid: list[list[Tile]]) -> int:
    max_energy = 0
    for r in range(len(grid)):
        lhs = energize(grid, Beam(Point(r, 0), Dir.E))
        rhs = energize(grid, Beam(Point(r, len(grid)-1), Dir.W))
        max_energy = max(max_energy, lhs, rhs)

    for c in range(len(grid[0])):
        top = energize(grid, Beam(Point(0, c), Dir.S))
        bot = energize(grid, Beam(Point(len(grid[0])-1, c), Dir.N))
        max_energy = max(max_energy, top, bot)

    return max_energy


def reset_grid(grid: list[list[Tile]]):
    for row in grid:
        for tile in row:
            tile.reset()


def energize(grid: list[list[Tile]], start: Beam) -> int:
    q = deque([start])
    num_energized = 0
    while len(q) > 0:
        beam = q.pop()
        if not beam.pos.in_bounds(grid):
            continue

        tile = grid[beam.pos.r][beam.pos.c]
        if len(tile.visited_by) == 0:
            num_energized += 1
        elif beam in tile.visited_by:
            continue
        tile.visited_by.add(beam)

        match [tile.type, beam.dir]:
            case ['|', Dir.E] | ['|', Dir.W]:
                # split into 2 beams N and S
                q.append(Beam(beam.pos + Dir.N, Dir.N))
                q.append(Beam(beam.pos + Dir.S, Dir.S))
            case ['-', Dir.N] | ['-', Dir.S]:
                # split into 2 beams E and W
                q.append(Beam(beam.pos + Dir.E, Dir.E))
                q.append(Beam(beam.pos + Dir.W, Dir.W))
            case ['/', Dir.N]:
                # bounce E
                q.append(Beam(beam.pos + Dir.E, Dir.E))
            case ['/', Dir.S]:
                # bounce W
                q.append(Beam(beam.pos + Dir.W, Dir.W))
            case ['/', Dir.E]:
                # bounce N
                q.append(Beam(beam.pos + Dir.N, Dir.N))
            case ['/', Dir.W]:
                # bounce S
                q.append(Beam(beam.pos + Dir.S, Dir.S))
            case ['\\', Dir.N]:
                # bounce W
                q.append(Beam(beam.pos + Dir.W, Dir.W))
            case ['\\', Dir.S]:
                # bounce E
                q.append(Beam(beam.pos + Dir.E, Dir.E))
            case ['\\', Dir.E]:
                # bounce S
                q.append(Beam(beam.pos + Dir.S, Dir.S))
            case ['\\', Dir.W]:
                # bounce N
                q.append(Beam(beam.pos + Dir.N, Dir.N))
            case [_, _]:
                # otherwise keep going in current direction
                q.append(Beam(beam.pos + beam.dir, beam.dir))
    
    reset_grid(grid)
    return num_energized
