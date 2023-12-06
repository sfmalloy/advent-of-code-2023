from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass


class MapRange:
    src_min: int
    src_max: int
    dst_min: int
    dst_max: int
    diff: int

    def __init__(self, dst: int, src: int, amt: int):
        self.src_min = src
        self.src_max = src + amt - 1
        self.dst_min = dst
        self.dst_max = dst + amt - 1
        self.diff = dst - src    

    def convert(self, src: int) -> int | None:
        if self.src_min <= src <= self.src_max:
            return src + self.diff
        return None


    def reverse_convert(self, dst: int) -> int | None:
        if self.dst_min <= dst <= self.dst_max:
            return dst - self.diff
        return None


@dataclass
class ConversionRules:
    seeds: list[int]
    maps: list[list[MapRange]]


@advent.parser(5)
def parse(file: TextIOWrapper):
    blocks = [line.strip() for line in file.read().split('\n\n')]
    maps: list[list[MapRange]] = []
    seeds = list(map(int, blocks[0].split(': ')[1].split()))
    for b in blocks[1:]:
        block_data = b.split('\n')
        curr = []
        for row in block_data[1:]:
            dst, src, amt = map(int, row.strip().split())
            curr.append(MapRange(dst, src, amt))
        maps.append(curr)
    return ConversionRules(seeds, maps)


@advent.day(5, part=1)
def solve1(ipt: ConversionRules):
    conversions = [s for s in ipt.seeds]
    for m in ipt.maps:
        new_conversions = []
        for num in conversions:
            new_conversions.append(fwd_convert(num, m))
        conversions = new_conversions
    return min(conversions)


@advent.day(5, part=2)
def solve2(ipt: ConversionRules):
    seed_ranges = [(ipt.seeds[i], ipt.seeds[i]+ipt.seeds[i+1]-1) for i in range(0, len(ipt.seeds), 2)]
    val = 0
    while True:
        prev = val
        for m in reversed(ipt.maps):
            val = rev_convert(val, m)
        if is_valid_seed(val, seed_ranges):
            return prev
        val = prev + 1


def fwd_convert(num: int, map: list[MapRange]):
    for m in map:
        val = m.convert(num)
        if val:
            return val
    return num


def rev_convert(num: int, map: list[MapRange]):
    for m in map:
        val = m.reverse_convert(num)
        if val:
            return val
    return num


def is_valid_seed(num: int, seed_ranges: list[tuple[int, int]]):
    for (mn, mx) in seed_ranges:
        if mn <= num <= mx:
            return True
    return False
