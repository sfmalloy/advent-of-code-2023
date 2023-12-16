from .lib.advent import advent
from io import TextIOWrapper
from typing import Sequence


@advent.parser(13)
def parse(file: TextIOWrapper) -> list[list[str]]:
    return [line.strip().splitlines() for line in file.read().split('\n\n')]


@advent.day(13, part=1)
def solve1(patterns: list[list[str]]) -> int:
    return find_reflection(patterns, 0)


@advent.day(13, part=2)
def solve2(patterns: list[list[str]]) -> int:
    return find_reflection(patterns, 1)


def find_reflection(patterns: list[list[str]], smudge_count: int) -> int:
    total = 0
    for pattern in patterns:
        horizontal_line = search_pattern(pattern, smudge_count)
        if horizontal_line == 0:
            pattern = [''.join(row) for row in zip(*pattern)]
            vertical_line = search_pattern(pattern, smudge_count)
            total += vertical_line
        else:
            total += 100 * horizontal_line
    return total


def search_pattern(pattern: list[list[str]], smudge_count: int) -> int:
    for row in range(0, len(pattern) - 1):
        if count_smudges(pattern, row, row + 1) == smudge_count:
            return row + 1
    return 0


def count_smudges(pattern: list[str], start: int, end: int) -> int:
    left = start
    right = end
    smudges = 0
    while left >= 0 and right < len(pattern):
        if pattern[left] != pattern[right]:
            for l, r in zip(pattern[left], pattern[right]):
                if l != r:
                    smudges += 1
        left -= 1
        right += 1
    return smudges
