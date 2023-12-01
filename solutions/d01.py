from .lib.advent import advent
from io import TextIOWrapper

@advent.parser(1)
def parse(file: TextIOWrapper):
    return [line.strip() for line in file.readlines()]


@advent.day(1, part=1)
def day1(lines: list[str]):
    s = 0
    for line in lines:
        dsum = ''
        for c in line:
            if c.isdigit():
                dsum += c
        dsum = dsum[0] + dsum[-1]
        s += int(dsum)
    return s


@advent.day(1, part=2)
def solve2(lines: list[str]):
    nums = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }
    s = 0
    for line in lines:
        indices = {}
        for name, val in nums.items():
            found = line.find(name)
            while found != -1:
                indices[found] = str(val)
                found = line.find(name, found+1)
        for i in range(1,10):
            found = line.find(str(i))
            while found != -1:
                indices[found] = str(i)
                found = line.find(str(i), found+1)
        dsum = indices[min(indices)] + indices[max(indices)]
        s += int(dsum)
    return s
