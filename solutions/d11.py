from .lib.advent import advent
from .lib.util import Point
from io import TextIOWrapper
from dataclasses import dataclass

@dataclass
class CosmicData:
    galaxies: list[Point]
    empty_rows: list[int]
    empty_cols: list[int]


@advent.parser(11)
def parse(file: TextIOWrapper) -> CosmicData:
    grid = [list(map(str, line.strip())) for line in file.readlines()]

    galaxies = []
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == '#':
                galaxies.append(Point(r, c))
    
    return CosmicData(
        galaxies,
        [r for r, row in enumerate(grid) if row.count('#') == 0],
        [c for c, col in enumerate(zip(*grid)) if col.count('#') == 0]
    )


@advent.day(11, part=1)
def solve1(data: CosmicData) -> int:
    return total_dists(data, 2)


@advent.day(11, part=2, reparse=False)
def solve2(data: CosmicData) -> int:
    return total_dists(data, 1000000)


def total_dists(data: CosmicData, expand_factor: int) -> int:
    dist = 0
    galaxies = expand(data, expand_factor)
    for i, src in enumerate(galaxies):
        for dst in galaxies[i+1:]:
            if src != dst:
                dist += src.mdist(dst)
    return dist


def expand(data: CosmicData, factor: int) -> list[Point]:
    factor -= 1
    row_deltas = [0]*len(data.galaxies)
    for r in reversed(data.empty_rows):
        for g, galaxy in enumerate(data.galaxies):
            if galaxy.r > r:
                row_deltas[g] += factor
    
    col_deltas = [0]*len(data.galaxies)
    for c in reversed(data.empty_cols):
        for g, galaxy in enumerate(data.galaxies):
            if galaxy.c > c:
                col_deltas[g] += factor

    expanded = []
    for galaxy, dr, dc in zip(data.galaxies, row_deltas, col_deltas):
        expanded.append(Point(galaxy.r + dr, galaxy.c + dc))

    return expanded
