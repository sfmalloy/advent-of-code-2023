from .lib.advent import advent
from io import TextIOWrapper

NAME_TO_DIGIT = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


REVERSED_NAME_TO_DIGIT = {k[::-1]:v for k,v in NAME_TO_DIGIT.items()}


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
                break
        for c in reversed(line):
            if c.isdigit():
                dsum += c
                break
        s += int(dsum)
    return s


@advent.day(1, part=2)
def solve2(lines: list[str]):
    s = 0
    for line in lines:
        s += int(find_first_digit(line) + find_last_digit(line))
    return s


def find_first_digit(line: str):
    for i,c in enumerate(line):
        if c.isdigit():
            return c
        l = 3
        word = line[i:i+l]
        while l < 6:
            if word in NAME_TO_DIGIT:
                return NAME_TO_DIGIT[word]
            l += 1
            word = line[i:i+l]


def find_last_digit(line: str):
    rev = line[::-1]
    for i,c in enumerate(rev):
        if c.isdigit():
            return c
        l = 3
        word = rev[i:i+l]
        while l < 6:
            if word in REVERSED_NAME_TO_DIGIT:
                return REVERSED_NAME_TO_DIGIT[word]
            l += 1
            word = rev[i:i+l]
