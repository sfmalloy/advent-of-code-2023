from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass

@dataclass
class Race:
    time: int
    dist: int


@advent.day(6, part=1)
def solve1(file: TextIOWrapper):
    times, dists = [list(map(int, line.strip().split(': ')[1].split())) for line in file.readlines()]
    races = [Race(t, d) for t, d in zip(times, dists)]
    mult = 1
    for race in races:
        mult *= num_wins(race)
    return mult


@advent.day(6, part=2)
def solve2(file: TextIOWrapper):
    time = int(''.join(file.readline().strip().split(': ')[1].split()))
    dist = int(''.join(file.readline().strip().split(': ')[1].split()))
    return num_wins(Race(time, dist))


def num_wins(race: Race) -> int:
    t_hold = 0
    while (race.time - t_hold) * t_hold <= race.dist:
        t_hold += 1
    return race.time - 2*t_hold + 1
