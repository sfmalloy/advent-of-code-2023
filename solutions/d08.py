from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque
import re
import math


@dataclass
class Node:
    src: str
    left: str
    right: str


@dataclass
class Data:
    dirs: list[int]
    nodes: dict[str, Node]


@advent.parser(8)
def parse(file: TextIOWrapper):
    dirs, nodes = file.read().split('\n\n')
    parsed_nodes = {}
    for line in nodes.split('\n')[:-1]:
        src, left, right = re.search(r'([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)', line).groups()
        parsed_nodes[src] = (left, right)
    return Data([0 if d == 'L' else 1 for d in dirs], parsed_nodes)


@advent.day(8, part=1)
def solve1(ipt: Data):
    dist = 0
    curr = 'AAA'
    idx = 0
    while curr != 'ZZZ':
        d = ipt.dirs[idx]
        curr = ipt.nodes[curr][d]
        dist += 1
        idx += 1
        if idx == len(ipt.dirs):
            idx = 0
    return dist


@advent.day(8, part=2)
def solve2(ipt: Data):
    q = deque([])
    for n in ipt.nodes:
        if n[2] == 'A':
            q.append((n, 0, 0))
    L = len(ipt.dirs)
    dists = []
    while len(q) > 0:
        n, d, idx = q.popleft()
        if n[2] == 'Z':
            dists.append(d)
            continue
        q.append((ipt.nodes[n][ipt.dirs[idx]], d+1, (idx+1) % L))
    return math.lcm(*dists)
