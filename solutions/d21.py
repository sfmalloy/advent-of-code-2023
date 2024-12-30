from .lib.advent import advent
from .lib.util import Point, PointDir
from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque


@dataclass
class Garden:
    start: Point
    garden: list[list[str]]


@advent.parser(21)
def parse(file: TextIOWrapper):
    plots = []
    start = Point(0, 0)
    for r, row in enumerate(file.readlines()):
        plot_row = []
        for c, col in enumerate(row.strip()):
            if col != 'S':
                plot_row.append(col)
            else:
                plot_row.append('.')
                start = Point(r, c)
        plots.append(plot_row)
    return Garden(start, plots)


@advent.day(21, part=1)
def solve1(ipt: Garden):
    return len(exact_dist_points(ipt, 64))


@advent.day(21, part=2)
def solve2(ipt: Garden):
    S = 26501365
    Y = [len(exact_dist_points(ipt, 65)),
         len(exact_dist_points(ipt, 196)),
         len(exact_dist_points(ipt, 327))]
    X = [65, 196, 327]
    A = len(ipt.garden) * len(ipt.garden)

    v0 = lagrange(X[2], X[1], X[0], Y[0])
    v1 = lagrange(X[2], X[0], X[1], Y[1])
    v2 = lagrange(X[0], X[1], X[2], Y[2])

    a = round((v0[0] + v1[0] + v2[0]) * A)
    b = round((v0[1] + v1[1] + v2[1]) * A)
    c = round((v0[2] + v1[2] + v2[2]) * A)

    return (a*(S**2) + b*S + c) // A


def lagrange(a, b, c, y):
    D = (c-a) * (c-b)
    return (y / D, -y*(a+b) / D, y*(a*b) / D)


def exact_dist_points(ipt: Garden, S: int):
    L = len(ipt.garden)
    q = deque([(ipt.start, 0)])
    seen = set()
    final = set()
    is_even = S % 2
    while q:
        pos, steps = q.popleft()
        if pos in seen:
            continue
        if steps == S:
            final.add(pos)
            continue
        if steps % 2 == is_even:
            final.add(pos)
        seen.add(pos)
        for d in PointDir.all:
            new = pos + d
            if ipt.garden[new.r % L][new.c % L] == '.':
                q.append((new, steps + 1))
    return final
