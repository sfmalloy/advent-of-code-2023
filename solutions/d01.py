from .lib.advent import advent
from io import TextIOWrapper
import heapq


@advent.parser(1)
def day1_parser(file: TextIOWrapper) -> list[str]:
    return [list(map(int, block.split())) for block in file.read().split('\n\n')]


@advent.day(1)
def day1(nums: list[str]):
    largest = heapq.nlargest(3, [sum(block) for block in nums])
    return largest[0], sum(largest)
