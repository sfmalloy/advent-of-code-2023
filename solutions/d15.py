from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass


@advent.parser(15)
def parse(file: TextIOWrapper) -> list[str]:
    return file.read().strip().split(',')


@advent.day(15, part=1)
def solve1(init_sequence: list[str]) -> int:
    total = 0
    for step in init_sequence:
        total += box_hash(step)
    return total


@dataclass
class LabeledFocalLength:
    label: str
    focal_length: str


@advent.day(15, part=2)
def solve2(init_sequence: list[str]) -> int:
    hashmap: list[list[LabeledFocalLength]] = [[] for _ in range(256)]
    for step in init_sequence:
        if step.endswith('-'):
            label = step[:-1]
            box = box_hash(label)
            idx = find_in_box(hashmap[box], label)
            if idx != -1:
                hashmap[box].pop(idx)
        else:
            label, focal_length = step.split('=')
            box = box_hash(label)
            focal_length = int(focal_length)
            idx = find_in_box(hashmap[box], label)
            if idx == -1:
                hashmap[box].append(LabeledFocalLength(label, focal_length))
            else:
                hashmap[box][idx].focal_length = focal_length
    
    total = 0
    for b, box in enumerate(hashmap, start=1):
        if len(box) > 0:
            for slot, length in enumerate(box, start=1):
                total += b * slot * length.focal_length
    return total


def box_hash(step: str) -> int:
    curr = 0
    for char in step:
        curr = ((curr + ord(char)) * 17) % 256
    return curr


def find_in_box(box: list[LabeledFocalLength], label: str) -> int:
    for i, length in enumerate(box):
        if length.label == label:
            return i
    return -1
