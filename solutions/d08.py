from .lib.advent import advent
from io import TextIOWrapper

import re
import math
from dataclasses import dataclass
from collections import deque


@dataclass
class DocumentData:
    dirs: list[int]
    nodes: dict[str, tuple[int, int]]


@advent.parser(8)
def parse(file: TextIOWrapper) -> DocumentData:
    dirs, nodes = file.read().split('\n\n')
    parsed_nodes = {}
    for line in nodes.split('\n')[:-1]:
        src, left, right = re.findall(r'([0-9A-Z]{3})', line)
        parsed_nodes[src] = (left, right)
    return DocumentData([int(d == 'R') for d in dirs], parsed_nodes)


@advent.day(8, part=1)
def solve1(ipt: DocumentData) -> int:
    dist = 0
    curr = 'AAA'
    L = len(ipt.dirs)
    while curr != 'ZZZ':
        dir = ipt.dirs[dist % L]
        curr = ipt.nodes[curr][dir]
        dist += 1
    return dist


@advent.day(8, part=2)
def solve2(ipt: DocumentData) -> int:
    q = deque([])
    for name in ipt.nodes:
        if name[2] == 'A':
            q.append((name, 0))

    dists = []
    L = len(ipt.dirs)
    while len(q) > 0:
        name, dist = q.popleft()
        if name[2] == 'Z':
            dists.append(dist)
        else:
            dir = ipt.dirs[dist%L]
            q.append((ipt.nodes[name][dir], dist+1))
    return math.lcm(*dists)
