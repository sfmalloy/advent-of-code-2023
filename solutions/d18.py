import math
from .lib.advent import advent
from .lib.util import Vec2, Vec2Dir
from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque


@dataclass
class Edge:
    dir: Vec2Dir
    dist: int
    color: int


@advent.parser(18)
def parse(file: TextIOWrapper):
    edges = []
    dirs = {
        'R': Vec2Dir.R,
        'D': Vec2Dir.D,
        'L': Vec2Dir.L,
        'U': Vec2Dir.U
    }
    for line in file.readlines():
        line = line.strip()
        dir, dist, color = line.split()
        edges.append(Edge(dirs[dir], int(dist), int(color[2:-1], 16)))
    return edges


@advent.day(18, part=1)
def solve1(edges: list[Edge]):
    pos = Vec2(0, 0)
    vertices: deque[Vec2] = deque([])
    for edge in edges:
        pos += edge.dist * edge.dir
        vertices.append(pos)
    area = calculate_area(vertices)
    return area


@advent.day(18, part=2)
def solve2(edges: list[Edge]):
    dirs = [Vec2Dir.R, Vec2Dir.D, Vec2Dir.L, Vec2Dir.U]
    pos = Vec2(0, 0)
    corners: list[Vec2] = list()
    for edge in edges:
        dir = dirs[edge.color & 15]
        dist = edge.color >> 4
        pos += dist * dir
        corners.append(pos)
    return calculate_area(corners)


# https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf
def calculate_area(vertices: deque[Vec2]) -> int:
    triangles = set()
    i = 0
    perimiter = 0
    for i in range(len(vertices)):
        perimiter += vertices[(i+1) % len(vertices)].dist(vertices[i])

    while len(vertices) > 3:
        for i in range(len(vertices)):
            a = vertices[(i-1) % len(vertices)]
            b = vertices[i]
            c = vertices[(i+1) % len(vertices)]
            if is_convex(a, b, c) and is_ear(vertices, a, b, c):
                triangles.add((a, b, c))
                vertices.remove(b)
                break

    tri_area = 0
    triangles.add((vertices[0], vertices[1], vertices[2]))
    for t in triangles:
        a, b, c = t
        tri_area += triangle_area(a, b, c)

    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    area = tri_area - (perimiter / 2) + 1
    return round(area + perimiter)


# https://stackoverflow.com/questions/21483999/using-atan2-to-find-angle-between-two-vectors
def interior_angle_radians(a: Vec2, b: Vec2, c: Vec2) -> float:
    ba = b - a
    cb = c - b
    angle = math.atan2(ba.y, ba.x) - math.atan2(cb.y, cb.x)
    return angle


def is_convex(a: Vec2, b: Vec2, c: Vec2) -> bool:
    angle = math.degrees(interior_angle_radians(a, b, c))
    if angle < 0:
        angle += 360
    return angle < 180


# https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle
def vertex_in_triangle(test: Vec2, a: Vec2, b: Vec2, c: Vec2):
    area = triangle_area(a, b, c)
    sum_area = triangle_area(test, a, b) + triangle_area(test, b, c) + triangle_area(test, c, a)
    return sum_area == area


# also got area formula from link above
def triangle_area(a: Vec2, b: Vec2, c: Vec2):
    ab = b - a
    ac = c - a
    return abs(ab.cross(ac)) / 2


def is_ear(vertices: deque[Vec2], a: Vec2, b: Vec2, c: Vec2) -> bool:
    for v in vertices:
        if v != a and v != b and v != c and vertex_in_triangle(v, a, b, c):
            return False
    return True
