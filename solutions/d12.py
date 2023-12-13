from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque
from functools import cache


@dataclass(frozen=True, eq=True)
class Record:
    record: str
    sizes: tuple[int]


@advent.parser(12)
def parse(file: TextIOWrapper):
    return [(lambda record, sizes: Record(record, tuple(map(int, sizes.split(',')))))(*line.strip().split()) 
            for line in file.readlines()]


@advent.day(12, part=1)
def solve1(records: list[Record]):
    total = 0
    for record in records:
        total += arrange(record)
    return total


@advent.day(12, part=2)
def solve2(records: list[Record]):
    total = 0
    for record in records:
        bigger_record = '?'.join([record.record for _ in range(5)])
        bigger_sizes = record.sizes*5
        total += arrange(Record(bigger_record, bigger_sizes))
    return total


@cache
def arrange(record: Record):
    if len(record.sizes) == 0:
        return '#' not in record.record

    sub = ''
    start_op = 0
    total = 0
    end_sub = '#'*record.sizes[0] + ('.' if len(record.sizes) > 1 else '')
    sub = end_sub
    while len(sub) <= len(record.record):
        valid = True
        for s, r in zip(sub, record.record):
            if r != '?' and s != r:
                valid = False
                break
        if valid:
            total += arrange(Record(record.record[len(sub):], record.sizes[1:]))
        start_op += 1
        sub = '.'*start_op + end_sub
    return total
