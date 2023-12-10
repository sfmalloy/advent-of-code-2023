from .lib.advent import advent
from .lib.util import Point
from io import TextIOWrapper
from dataclasses import dataclass, field
from typing import Self, Optional
from collections import deque

INF = 2**31-1
N = Point(-1, 0)
S = Point(1, 0)
E = Point(0, 1)
W = Point(0, -1)

@dataclass(eq=True)
class Node:
    symbol: str
    pos: Point
    dist: int = INF
    neighbors: list[Self] = field(default_factory=list)
    visited: bool = False

    def add_neighbor(self, r: int, c: int, grid: list[list[Optional[Self]]], valid_symbols: set[str]):
        '''
        Adds the Node at grid[r][c] if it's a valid position, and not None. Otherwise None
        '''
        if r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r]) \
            and grid[r][c] is not None and grid[r][c].symbol in valid_symbols:
            self.neighbors.append(grid[r][c])
    
    def validate_neighbors(self):
        return (self.symbol == 'S' or len(self.neighbors) == 2)
    
    def filter_neighbors(self, grid: list[list[Optional[Self]]]):
        filtered = []
        for neighbor in self.neighbors:
            if grid[neighbor.pos.r][neighbor.pos.c] is not None:
                filtered.append(neighbor)
        self.neighbors = filtered

    def __repr__(self) -> str:
        return f'("{self.symbol}",{self.pos},{[n.pos for n in self.neighbors]})'


@dataclass
class Data:
    start: Node
    grid: list[list[Node]]


@advent.parser(10)
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    grid: list[list[Optional[Node]]] = []
    start = None

    # Build out Nodes without populating neighbors list
    for r, row in enumerate(lines):
        grid_row = []
        for c, col in enumerate(row):
            if col != '.':
                grid_row.append(Node(col, Point(r, c)))
            else:
                grid_row.append(None)
            if col == 'S':
                start = grid_row[-1]
        grid.append(grid_row)

    # 'S' gets added everywhere because we don't know what shape it actually has
    north_symbols = {'|','L','J', 'S'}
    south_symbols = {'|', '7', 'F', 'S'}
    east_symbols = {'-', 'L', 'F', 'S'}
    west_symbols = {'-', 'J', '7', 'S'}

    # Iterate through all Nodes connecting valid neighbors
    for row in grid:
        for node in row:
            if node is not None:
                if node.symbol in north_symbols:
                    node.add_neighbor(node.pos.r-1, node.pos.c, grid, south_symbols)
                if node.symbol in south_symbols:
                    node.add_neighbor(node.pos.r+1, node.pos.c, grid, north_symbols)
                if node.symbol in west_symbols:
                    node.add_neighbor(node.pos.r, node.pos.c-1, grid, east_symbols)
                if node.symbol in east_symbols:
                    node.add_neighbor(node.pos.r, node.pos.c+1, grid, west_symbols)

    # remove extra pipes that aren't connected to a loop
    has_extra = True    
    while has_extra:
        has_extra = False
        to_remove: list[Point] = []
        for row in grid:
            for node in row:
                if node is not None and not node.validate_neighbors():
                    has_extra = True
                    to_remove.append(node.pos)
        for pos in to_remove:
            grid[pos.r][pos.c] = None
        for row in grid:
            for node in row:
                if node is not None:
                    node.filter_neighbors(grid)
    return Data(start, grid)


@advent.day(10, part=1)
def solve1(ipt: Data):
    # Dijsktra's for distances
    q = deque([ipt.start])
    ipt.start.dist = 0
    while len(q) > 0:
        node = q.popleft()
        for neighbor in node.neighbors:
            if neighbor.dist > node.dist + 1:
                neighbor.dist = node.dist + 1
                q.append(neighbor)
    
    # Another BFS pass to get largest distance within the main loop
    q = deque([ipt.start])
    far = 0
    while len(q) > 0:
        node = q.popleft()
        node.visited = True
        far = max(far, node.dist)
        for neighbor in node.neighbors:
            if not neighbor.visited:
                q.append(neighbor)

    return far


@advent.day(10, part=2, reparse=False)
def solve2(ipt: Data):
    # Remove any extra pipes that aren't part of the MAIN loop
    for r, row in enumerate(ipt.grid):
        for c, node in enumerate(row):
            if node is not None and node.dist == INF:
                ipt.grid[r][c] = None

    # Replace S with whatever pipe shape it's supposed to have
    ipt.start.symbol = find_start_symbol(ipt.start)

    # Create fake gaps between all the symbols with a different filler symbol
    #   as to not get counted as ground. Also includes padding on all 4 sides
    #   of the grid to make it so I can do flood fill from 1 starting point
    filler = '*'
    symbols = []
    for r, row in enumerate(ipt.grid):
        srow = ['*']
        for c, node in enumerate(row):
            if node is not None:
                srow.append(node.symbol)
            else:
                srow.append('.')
            srow.append(filler)
        symbols.append(srow)
        symbols.append([filler]*len(srow))
    symbols = [[filler]*len(symbols[0])] + symbols
    
    # Extend previous connections replacing filler spots with either | or - depending
    #   on the direction
    for r, row in enumerate(symbols):
        for c, col in enumerate(row):
            pos = Point(r, c)
            if col == filler:
                north = pos+N
                if in_bounds(north, symbols) and symbols[north.r][north.c] in '|7F':
                    symbols[r][c] = '|'
                east = pos+E
                if in_bounds(east, symbols) and symbols[east.r][east.c] in '-7J':
                    symbols[r][c] = '-'

    # Flood fill starting from outside the loop.
    # If ground or filler is encountered, replace with 'O'
    q = deque([Point(0, 0)])
    while len(q) > 0:
        pos = q.pop()
        symbols[pos.r][pos.c] = 'O'
        north = pos+N
        if in_bounds(north, symbols) and symbols[north.r][north.c] in '.*':
            q.append(north)
        south = pos+S
        if in_bounds(south, symbols) and symbols[south.r][south.c] in '.*':
            q.append(south)
        west = pos+W
        if in_bounds(west, symbols) and symbols[west.r][west.c] in '.*':
            q.append(west)
        east = pos+E
        if in_bounds(east, symbols) and symbols[east.r][east.c] in '.*':
            q.append(east)

    # All remaining dots are fully contained in the loop so we can just count
    #   the leftovers
    total = 0    
    for row in symbols:
        for col in row:
            if col == '.':
                total += 1
    return total


def in_bounds(pt: Point, grid: list[list]):
    return pt.r >= 0 and pt.c >= 0 and pt.r < len(grid) and pt.c < len(grid[pt.r])


def find_start_symbol(start: Node):
    dirs = []
    for n in start.neighbors:
        dirs.append(n.pos - start.pos)

    if dirs[0] == N:
        if dirs[1] == S:
            return '|'
        elif dirs[1] == E:
            return 'L'
        elif dirs[1] == W:
            return 'J'
    elif dirs[0] == S:
        if dirs[1] == N:
            return '|'
        elif dirs[1] == E:
            return 'F'
        elif dirs[1] == W:
            return '7'
    elif dirs[0] == E:
        if dirs[1] == W:
            return '-'
        elif dirs[1] == N:
            return 'L'
        elif dirs[1] == S:
            return 'F'
    elif dirs[0] == W:
        if dirs[1] == E:
            return '-'
        elif dirs[1] == N:
            return 'J'
        elif dirs[1] == S:
            return '7'
