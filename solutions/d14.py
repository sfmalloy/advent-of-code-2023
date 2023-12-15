from .lib.advent import advent
from io import TextIOWrapper
from math import lcm


@advent.parser(14)
def parse(file: TextIOWrapper) -> list[list[str]]:
    return [list(map(str, line.strip())) for line in file.readlines()]


@advent.day(14, part=1)
def solve1(grid: list[list[str]]) -> int:
    tilt_north(grid)
    return calculate_load(grid)


@advent.day(14, part=2)
def solve2(grid: list[list[str]]) -> int:
    start = get_cycle(grid)
    for _ in range(start):
        grid = spin(grid)
    period = get_cycle(grid)
    for _ in range((1_000_000_000 - start) % period):
        grid = spin(grid)
    return calculate_load(grid)


def get_cycle(grid: list[list[str]]):
    cycle = 0
    seen = set()
    while True:
        tgrid = tuple(map(tuple, grid))
        if tgrid in seen:
            return cycle
        seen.add(tgrid)
        cycle += 1
        grid = spin(grid)


def calculate_load(grid: list[list[str]]):
    load = 0
    for r, row in enumerate(grid):
        for col in row:
            if col == 'O':
                load += len(grid) - r
    return load


def spin(grid: list[list[str]]) -> list[list[str]]:
    rotated_grid = grid
    for _ in range(4):
        tilt_north(rotated_grid)
        rotated_grid = rotated(rotated_grid)
    return rotated_grid


def rotated(grid: list[list[str]]) -> list[list[str]]:
    return list(map(list, zip(*reversed(grid))))


def tilt_north(grid: list[list[str]]) -> None:
    prev_empty = [0]*len(grid[0])
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 'O':
                grid[r][c] = '.'
                grid[prev_empty[c]][c] = 'O'
                prev_empty[c] += 1
            elif col == '#':
                prev_empty[c] = r + 1
