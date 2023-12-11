from .lib.advent import advent
from .lib.util import Point, Dir
from io import TextIOWrapper
from collections import deque
from dataclasses import dataclass

@dataclass
class CosmicData:
    grid: list[str]
    galaxies: list[Point]


@advent.parser(11)
def parse(file: TextIOWrapper):
    grid = [list(map(str, line.strip())) for line in file.readlines()]
    galaxies = []
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == '#':
                galaxies.append(Point(r, c))
    return CosmicData(grid, galaxies)

INF = 2**31-1

@advent.day(11, part=1)
def solve1(data: CosmicData):
    return total_dists(expand(data, 2))


@advent.day(11, part=2, reparse=False)
def solve2(data: CosmicData):
    return total_dists(expand(data, 1000000))


def total_dists(galaxies: list[Point]):
    dist = 0
    for i, src in enumerate(galaxies):
        for dst in galaxies[i+1:]:
            if src != dst:
                dist += src.mdist(dst)
    return dist


def expand(data: CosmicData, N: int):
    N -= 1

    row_expands = []
    for r, row in enumerate(data.grid):
        if row.count('.') == len(data.grid[r]):
            row_expands.append(r)
    
    col_expands = []
    for c, line in enumerate(zip(*data.grid)):
        if line.count('.') == len(data.grid):
            col_expands.append(c)

    row_deltas = [0]*len(data.galaxies)
    for r in reversed(row_expands):
        for g, galaxy in enumerate(data.galaxies):
            if galaxy.r > r:
                row_deltas[g] += N
    
    col_deltas = [0]*len(data.galaxies)
    for c in reversed(col_expands):
        for g, galaxy in enumerate(data.galaxies):
            if galaxy.c > c:
                col_deltas[g] += N
    
    expanded = []
    for g,dr,dc in zip(data.galaxies, row_deltas, col_deltas):
        expanded.append(Point(g.r + dr, g.c + dc))

    return expanded
