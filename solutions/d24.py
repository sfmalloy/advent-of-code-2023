from .lib.advent import advent
from .lib.util import Vec3
from io import TextIOWrapper
from dataclasses import dataclass
from itertools import islice
import turtle


@dataclass(eq=True)
class Hailstone:
    pos: Vec3
    vel: Vec3
    id: int

    def __init__(self, line: str, id: int):
        p, v = line.split('@')
        self.pos = Vec3(*map(int, p.split(', ')))
        self.vel = Vec3(*map(int, v.split(', ')))
        self.id = id
    
    def at(self, t: int) -> Vec3:
        print(self.pos, self.pos + t*self.vel)
        return self.pos + (t*self.vel)
    

@advent.parser(24)
def parse(file: TextIOWrapper):
    return [Hailstone(line, i) for i, line in enumerate(file.readlines())]


@advent.day(24, part=1)
def solve1(hailstones: list[Hailstone]):
    lower_bound = 200000000000000
    upper_bound = 400000000000000

    total = 0
    for i, a in enumerate(hailstones):
        for b in islice(hailstones, i, None):
            ra = a.vel.y / a.vel.x
            rb = b.vel.y / b.vel.x

            if ra != rb:
                x = ((b.pos.y - a.pos.y) - (rb*b.pos.x - ra*a.pos.x)) / (ra - rb)
                y = (x-a.pos.x) * ra + a.pos.y

                if x >= lower_bound and y >= lower_bound and x <= upper_bound and y <= upper_bound:
                    total += (x-a.pos.x) / a.vel.x >= 0 and (x-b.pos.x) / b.vel.x >= 0
    return total


@advent.day(24, part=2)
def solve2(hailstones: list[Hailstone]):
    return None
