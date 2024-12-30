from .lib.advent import advent
from .lib.util import Vec3
from io import TextIOWrapper
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class CubeData:
    bricks: list[list[Vec3]]
    plane: defaultdict[int, defaultdict[int, defaultdict[int, int]]]


@advent.parser(22)
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    bricks = []
    plane = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for i, line in enumerate(lines):
        start, end = line.split('~')
        start_cube = Vec3(*map(int, start.split(',')))
        end_cube = Vec3(*map(int, end.split(',')))
        brick = []
        for x in range(start_cube.x, end_cube.x+1):
            for y in range(start_cube.y, end_cube.y+1):
                for z in range(start_cube.z, end_cube.z+1):
                    brick.append(Vec3(x, y, z))
                    plane[x][y][z] = i
        bricks.append(brick)
    return CubeData(bricks, plane)


@advent.day(22, part=1)
def solve1(data: CubeData):
    bricks = data.bricks
    plane = data.plane
    '''
    NOTE: z is vertical
    '''
    max_z = max(max(max(z for z in y_plane) for y_plane in x_plane.values()) for x_plane in plane.values())
    
    return 0


@advent.day(22, part=2)
def solve2(ipt):
    return 0
