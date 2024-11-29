from .lib.advent import advent
from .lib.util import Point, PointDir

from io import TextIOWrapper
from collections import deque, defaultdict
import sys


@advent.parser(23)
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return lines


@advent.day(23, part=1)
def solve1(grid: list[str]):
    q = deque([(set(), Point(0, 1))])
    R = len(grid)
    C = len(grid[0])
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
        if n.in_bounds(grid) and n not in path and grid[curr.r][curr.c] in n_tiles and grid[n.r][n.c] != '#':
            q.append((path | {curr}, n))

        e = curr + PointDir.E
        if e.in_bounds(grid) and e not in path and grid[curr.r][curr.c] in e_tiles and grid[e.r][e.c] != '#':
            q.append((path | {curr}, e))

        s = curr + PointDir.S
        if s.in_bounds(grid) and s not in path and grid[curr.r][curr.c] in s_tiles and grid[s.r][s.c] != '#':
            q.append((path | {curr}, s))

        w = curr + PointDir.W
        if w.in_bounds(grid) and w not in path and grid[curr.r][curr.c] in w_tiles and grid[w.r][w.c] != '#':
            q.append((path | {curr}, w))

    return best


@advent.day(23, part=2)
def solve2(grid: list[list[str]]):
    end = Point(len(grid)-1, len(grid[0])-2)
    
    graph = construct_graph(grid)
    condensed = condense_graph(graph, end)
    q = deque([(Point(0, 1), 0, frozenset())])
    best = 0
    while q:
        curr, L, visited = q.pop()
        if curr == end:
            best = max(L, best)
            if best == L:
                print(best)
            continue
        for neighbor in condensed[curr]:
            if neighbor not in visited:
                q.append((neighbor, L+condensed[curr][neighbor], visited | {curr}))
    return best


def append_if_valid(curr: Point, dir: Point, grid: list[list[str]], q: deque, visited: set, graph: defaultdict[Point, set]):
    pt = curr + dir
    if pt.in_bounds(grid) and grid[pt.r][pt.c] != '#':
        graph[curr].add(pt)
        if pt not in visited:
            q.append(pt)


def construct_graph(grid: list[list[str]]):
    q = deque([Point(0, 1)])
    visited = set()
    graph = defaultdict(set)

    while q:
        curr = q.pop()
        visited.add(curr)

        append_if_valid(curr, PointDir.N, grid, q, visited, graph)
        append_if_valid(curr, PointDir.E, grid, q, visited, graph)
        append_if_valid(curr, PointDir.S, grid, q, visited, graph)
        append_if_valid(curr, PointDir.W, grid, q, visited, graph)

    return graph


def condense_graph(graph: defaultdict[list, Point], end: Point):
    condensed = defaultdict(lambda: defaultdict(set))
    q = deque([(Point(0, 1), Point(0, 1), 0)])
    visited = set()
    while q:
        src, curr, L = q.pop()
        if len(graph[curr]) > 2 or curr == end:
            condensed[curr][src] = L
            condensed[src][curr] = L
            L = 0
            src = curr
        visited.add((src, curr))
        for dst in graph[curr]:
            if (src, dst) not in visited:
                q.append((src, dst, L+1))
    return condensed
