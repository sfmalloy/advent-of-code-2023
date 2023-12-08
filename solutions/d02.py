from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass

@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0


@advent.parser(2)
def parse(file: TextIOWrapper) -> list[list[CubeSet]]:
    games = []
    for line in file.readlines():
        game = []
        for round in line.split(': ')[-1].split('; '):
            cubeset = CubeSet()
            for group in round.split(', '):
                num, color = group.split()
                match color:
                    case 'red':
                        cubeset.red = int(num)
                    case 'green':
                        cubeset.green = int(num)
                    case 'blue':
                        cubeset.blue = int(num)
            game.append(cubeset)
        games.append(game)
    return games


@advent.day(2, part=1)
def solve1(ipt: list[list[CubeSet]]):
    red = 12
    green = 13
    blue = 14
    total = 0
    for id, game in enumerate(ipt, start=1):
        possible = True
        for round in game:
            if red < round.red or blue < round.blue or green < round.green:
                possible = False
                break
        if possible:
            total += id
    return total


@advent.day(2, part=2)
def solve2(ipt: list[list[CubeSet]]):
    pow = 0
    for game in ipt:
        red = 0
        green = 0
        blue = 0
        for round in game:
            red = max(round.red, red)
            blue = max(round.blue, blue)
            green = max(round.green, green)
        pow += red*green*blue
