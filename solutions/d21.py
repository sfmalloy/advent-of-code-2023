from .lib.advent import advent
from .lib.util import Point, PointDir
from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque, defaultdict


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
    q = deque([(ipt.start, 0)])
    seen = set()
    final = set()
    S = 64
    is_even = S % 2
    while len(q) > 0:
        pos, steps = q.popleft()
        if pos in seen:
            continue
        if steps == S:
            final.add(pos)
            continue
        if steps % 2 == is_even:
            final.add(pos)
        seen.add(pos)
        for d in PointDir.all():
            new = pos + d
            if new.in_bounds(ipt.garden) and ipt.garden[new.r][new.c] == '.':
                q.append((new, steps + 1))
    return len(final)


@advent.day(21, part=2)
def solve2(ipt: Garden):
    return 'not solved'


def print_ppm(grid: list[list[str]], counts: defaultdict[set]):
    import sys
    import colorsys

    def write(*args):
        print(*args, file=sys.stderr)

    mn = min(len(count) for count in counts.values())
    mx = max(len(count) for count in counts.values()) + 1
    print(mn, mx)

    write('P3')
    write(len(grid), len(grid[0]))
    write('255')
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if Point(r, c) in counts:
                percent = (mx - len(counts[Point(r, c)])) / (mx - mn)
                write(' '.join(list(map(str, tuple(round(e*255) for e in colorsys.hsv_to_rgb(1, 0.5, percent))))))
            else:
                write('255 255 255')


    # q = deque([(ipt.start, 0)])
    # seen = set()
    # final = set()
    # stepdict = defaultdict(list)
    # # counts = defaultdict(lambda: defaultdict(set))
    # counts = defaultdict(set)
    # # S = 26_501_365
    # S = int(input())
    # is_even = S % 2
    # while len(q) > 0:
    #     pos, steps = q.popleft()
    #     if pos in seen:
    #         continue
    #     if steps == S:
    #         stepdict[Point(pos.r % len(ipt.garden), pos.c % len(ipt.garden[0]))].append(steps)
    #         counts[(Point(pos.r % len(ipt.garden), pos.c % len(ipt.garden[0])))].add(pos)
    #         # counts[pos.r % len(ipt.garden)][pos.c % len(ipt.garden[0])].add((pos, dir))
    #         continue
    #     if steps % 2 == is_even:
    #         # counts[pos.r % len(ipt.garden)][pos.c % len(ipt.garden[0])].add((pos, dir))
    #         counts[(Point(pos.r % len(ipt.garden), pos.c % len(ipt.garden[0])))].add(pos)
    #         stepdict[Point(pos.r % len(ipt.garden), pos.c % len(ipt.garden[0]))].append(steps)
    #     seen.add(pos)
    #     for d in PointDir.all():
    #         new = pos + d
    #         if ipt.garden[new.r % len(ipt.garden)][new.c % len(ipt.garden[0])] == '.':
    #             q.append((new, steps + 1))
    # tot = 0
    # unique = defaultdict(list)
    # count_counts = defaultdict(int)
    # for r in range(len(ipt.garden)):
    #     for c in range(len(ipt.garden[0])):
    #         unique[tuple(stepdict[Point(r, c)])].append((r,c))

    # for u in unique.items():
    #     print(u)
    # # print_ppm(ipt.garden, counts)
    # # for k, v in counts.items():
    # #     print(k, len(v), file=sys.stderr)
    # #     tot += len(v)
    # # for r in range(len(ipt.garden)):
    # #     for c in range(len(ipt.garden[0])):
    # #         if ipt.garden[r][c] != '#':
    # #             # print(r, c, len(counts[r][c]))
    # #             tot += len(counts[r][c])
    # #             count_counts[len(counts[r][c])] += 1
    
    # # for k, v in sorted(count_counts.items()):
    # #     print(k, v)