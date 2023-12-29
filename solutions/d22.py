from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass


@advent.parser(22)
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return lines


@advent.day(22, part=1)
def solve1(ipt):
    return 0


@advent.day(22, part=2)
def solve2(ipt):
    return 0
