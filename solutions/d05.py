from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict
import re
from pprint import pprint


@dataclass
class MapRange:
    dst: int
    src: int
    amt: int

    def convert(self, src: int) -> int | None:
        ds = src - self.src
        if ds <= self.amt and ds >= 0:
            return self.dst + ds
        return None

ConversionMap = defaultdict[str, defaultdict[str, list[MapRange]]]
@dataclass
class ConversionRules:
    seeds: list[int]
    maps: ConversionMap


@advent.parser(5)
def parse(file: TextIOWrapper):
    blocks = [line.strip() for line in file.read().split('\n\n')]
    maps: ConversionMap = defaultdict(lambda: defaultdict(list))
    seeds = list(map(int, blocks[0].split(': ')[1].split()))
    for b in blocks[1:]:
        block_data = b.split('\n')
        src_name, _, dst_name, _ = re.split(r'-| map:', block_data[0])
        for row in block_data[1:]:
            dst, src, amt = map(int, row.strip().split())
            maps[src_name][dst_name].append(MapRange(dst, src, amt))
    return ConversionRules(seeds, maps)


@advent.day(5, part=1)
def solve1(ipt: ConversionRules):
    src_key = 'seed'
    goal_key = 'location'
    conversions = [s for s in ipt.seeds]
    while src_key != goal_key:
        dst_key = list(ipt.maps[src_key].keys())[0]
        new_conversions = []
        print(ipt.maps[src_key])
        for num in conversions:
            new_conversions.append(get_conversion(src_key, dst_key, num, ipt.maps))
        conversions = new_conversions
        print(conversions)
        src_key = dst_key
        
    return min(conversions)


@advent.day(5, part=2)
def solve2(ipt):
    return 0


def get_conversion(src: str, dst: str, num: int, maps: ConversionMap):
    for m in maps[src][dst]:
        c = m.convert(num)
        if c:
            return c
        print(src, dst, num, c)
    return num
