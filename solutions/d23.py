from .lib.advent import advent
from .lib.util import Point, PointDir, print_grid

from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque


@advent.parser(23)
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return lines


@advent.day(23, part=1)
def solve1(ipt: list[str]):
    q = deque([(set(), Point(0, 1))])
    R = len(ipt)
    C = len(ipt[0])
    best = 0

    n_tiles = '.^'
    e_tiles = '.>'
    s_tiles = '.v'
    w_tiles = '.<'

    while len(q) > 0:
        path, curr = q.pop()
        if curr.r == R-1 and curr.c == C-2:
            l = len(path)
            if l > best:
                best = l
            continue

        n = curr + PointDir.N
        if n.in_bounds(ipt) and n not in path and ipt[curr.r][curr.c] in n_tiles and ipt[n.r][n.c] != '#':
            q.append((path | {curr}, n))

        e = curr + PointDir.E
        if e.in_bounds(ipt) and e not in path and ipt[curr.r][curr.c] in e_tiles and ipt[e.r][e.c] != '#':
            q.append((path | {curr}, e))

        s = curr + PointDir.S
        if s.in_bounds(ipt) and s not in path and ipt[curr.r][curr.c] in s_tiles and ipt[s.r][s.c] != '#':
            q.append((path | {curr}, s))

        w = curr + PointDir.W
        if w.in_bounds(ipt) and w not in path and ipt[curr.r][curr.c] in w_tiles and ipt[w.r][w.c] != '#':
            q.append((path | {curr}, w))

    return best


@advent.day(23, part=2)
def solve2(ipt):
    return 0
