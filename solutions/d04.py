import re
from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(4)
def parse(file: TextIOWrapper):
    my_winners = []
    for line in file.readlines():
        groups = re.search(r'((\d+ +)+)\| +((\d+ *)+)\n', line).groups()
        winners = set(map(int, groups[0].split()))
        mine = set(map(int, groups[2].split()))
        my_winners.append(len(winners & mine))
    return my_winners


@advent.day(4, part=1)
def solve1(ipt: list[int]):
    return sum(2**(num_winners-1) for num_winners in ipt if num_winners > 0)


@advent.day(4, part=2)
def solve2(ipt: list[int]):
    counts = [1 for _ in range(len(ipt))]
    total = 0
    for i, num_winners in enumerate(ipt):
        for c in range(i+1, i+num_winners+1):
            counts[c] += counts[i]
        total += counts[c]
    return total
