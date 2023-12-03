from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Data:
    range: defaultdict[int, list[tuple[int, int]]]
    grid: list[str]


@advent.parser(3)
def parse(file: TextIOWrapper):
    nums = {}
    pos_dict = defaultdict(list)
    lines = [line.strip() + '.' for line in file.readlines()]
    for row, line in enumerate(lines):
        num = ''
        pos = []
        for col, char in enumerate(line):
            if char.isdigit():
                num += char
                pos.append((row,col))
            elif num != '':
                for p in pos:
                    nums[p] = int(num)
                pos_dict[int(num)].append(pos)
                num = ''
                pos = []
    return Data(pos_dict, lines)


@advent.day(3)
def solve1(ipt: Data):
    total = 0
    gears = defaultdict(list)
    for num,pos in ipt.range.items():
        for plist in pos:
            parts = adj_parts(plist, ipt)
            if len(parts) > 0:
                total += num
            for r,c in parts:
                if ipt.grid[r][c] == '*':
                    gears[(r,c)].append(num)
    ratios = 0
    for nums in gears.values():
        if len(nums) == 2:
            ratios += nums[0] * nums[1]
    return total, ratios


def adj_parts(plist: list, ipt: Data):
    parts = set()
    for i,j in plist:
        adj = set()
        adj.add((i+1,j))
        adj.add((i-1,j))
        adj.add((i,j+1))
        adj.add((i,j-1))
        adj.add((i+1,j+1))
        adj.add((i-1,j+1))
        adj.add((i+1,j-1))
        adj.add((i-1,j-1))
        for r,c in adj:
            if r >= 0 and c >= 0 and r < len(ipt.grid) and c < len(ipt.grid[r]):
                if ipt.grid[r][c] != '.' and not ipt.grid[r][c].isdigit():
                    parts.add((r,c))
    return parts