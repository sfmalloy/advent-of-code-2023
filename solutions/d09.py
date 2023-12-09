from .lib.advent import advent
from io import TextIOWrapper
from collections import deque


@advent.parser(9)
def parse(file: TextIOWrapper):
    return [deque(map(int, line.strip().split())) for line in file.readlines()]


@advent.day(9)
def solve(ipt: list[deque[int]]):
    fwd = 0
    bck = 0
    for row in ipt:
        history = expand(row)
        fwd += extrapolate_fwd(history)
        bck += extrapolate_bck(history)
    return fwd, bck


def expand(top: deque[int]):
    rows = [top]
    while any(rows[-1]):
        new = deque([])
        for i in range(len(rows[-1])-1):
            new.append(rows[-1][i+1] - rows[-1][i])
        rows.append(new)
    return rows


def extrapolate_fwd(history: list[deque[int]]):
    for r in history:
        r.append(0)
    for i in range(len(history)-2, -1, -1):
        history[i][-1] = history[i][-2] + history[i+1][-1]
    return history[0][-1]


def extrapolate_bck(history: list[deque[int]]):
    for r in history:
        r.appendleft(0)
    for i in range(len(history)-2, -1, -1):
        history[i][0] = history[i][1] - history[i+1][0]
    return history[0][0]
