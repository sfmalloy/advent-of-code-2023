from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class EngineData:
    num_pos: defaultdict[int, list[tuple[int, int]]]
    grid: list[str]


@advent.parser(3)
def parse(file: TextIOWrapper) -> EngineData:
    num_pos = defaultdict(list)
    # add a '.' to the end of each line to cover for if a number ends on an edge
    lines = [line.strip() + '.' for line in file.readlines()]
    for row, line in enumerate(lines):
        num = ''
        pos = []
        for col, char in enumerate(line):
            if char.isdigit():
                num += char
                pos.append((row,col))
            elif num != '':
                num_pos[int(num)].append(pos)
                num = ''
                pos = []
    return EngineData(num_pos, lines)


@advent.day(3)
def solve1(ipt: EngineData) -> int:
    total = 0
    gears = defaultdict(list)
    for num, pos in ipt.num_pos.items():
        for pos_range in pos:
            parts = adj_parts(pos_range, ipt)
            if len(parts) > 0:
                total += num
            for r, c in parts:
                if ipt.grid[r][c] == '*':
                    gears[(r, c)].append(num)
    return total, sum(nums[0] * nums[1] for nums in gears.values() if len(nums) == 2)


def adj_parts(pos_range: list[tuple[int, int]], ipt: EngineData) -> int:
    parts = set()
    for i, j in pos_range:
        for r in range(i-1,i+2):
            for c in range(j-1,j+2):
                if (r >= 0 and c >= 0 
                    and r < len(ipt.grid) and c < len(ipt.grid[r])
                    and ipt.grid[r][c] != '.' and not ipt.grid[r][c].isdigit()):
                    parts.add((r, c))
    return parts
