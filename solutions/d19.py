import re
import operator
from io import TextIOWrapper
from dataclasses import dataclass
from typing import Optional
from functools import reduce

from .lib.advent import advent

@dataclass
class Workflow:
    result: str
    part: Optional[str]=None
    op: Optional[str]=None
    val: Optional[int]=None

    def possible_values(self, values: set[int], negated: bool=False):
        new = set()
        if self.op == '<':
            for rating in values:
                if (not negated and rating < self.val) or (negated and rating >= self.val):
                    new.add(rating)
        elif self.op == '>':
            for rating in values:
                if (not negated and rating > self.val) or (negated and rating <= self.val):
                    new.add(rating)
        return new


@dataclass
class PartWorkflows:
    workflows: dict[str, list[Workflow]]
    parts: list[dict[str, int]]


@advent.parser(19)
def parse(file: TextIOWrapper):
    workflow_str, part_str = file.read().split('\n\n')
    workflows = {}
    for line in workflow_str.splitlines():
        name, prog = line[:-1].split('{')
        workflow = []
        for wf in prog.split(','):
            if len(wf) > 1 and wf[1] in '<>':
                part, op, val, result = re.match(r'(x|m|a|s)(<|>)([0-9]+):([a-z]+|A|R)', wf).groups()
                workflow.append(Workflow(result, part, op, int(val)))
            else:
                workflow.append(Workflow(result=wf))
        workflows[name] = workflow
    
    parts = [
        {
            name: int(val)
            for (name, val) in [
                tuple(part.split('=')) for part in line[1:-1].split(',')
            ]
        }
        for line in part_str.strip().splitlines()
    ]
    return PartWorkflows(workflows, parts)


@advent.day(19, part=1)
def solve1(ipt: PartWorkflows):
    ratings = 0
    for part in ipt.parts:
        if evaluate(ipt.workflows, part):
            ratings += sum(part.values())
    return ratings


@advent.day(19, part=2)
def solve2(ipt: PartWorkflows):
    return get_combos(ipt.workflows, 'in', { part: frozenset(i for i in range(1, 4001)) for part in 'xmas' })


def evaluate(workflows: dict[str, list[Workflow]], part: dict[str, int]):
    ip = 'in'
    while True:
        curr = workflows[ip]
        for test in curr:
            if test.op == '>' and part[test.part] > test.val \
                or test.op == '<' and part[test.part] < test.val \
                or test.op is None:
                ip = test.result
                break
        if ip == 'A':
            return True
        elif ip == 'R':
            return False


def get_combos(workflows: dict[str, list[Workflow]], name: str, accepted: dict[str, frozenset[int]]):
    if name == 'A':
        return reduce(operator.mul, map(len, accepted.values()), 1)
    elif name == 'R':
        return 0
    
    combos = 0
    completed_tests: list[Workflow] = []
    for test in workflows[name]:
        new_accepted = {k:v for k,v in accepted.items()}
        for ctest in completed_tests:
            new_accepted[ctest.part] = ctest.possible_values(new_accepted[ctest.part], negated=True)
        if test.part is not None:
            new_accepted[test.part] = test.possible_values(new_accepted[test.part])
        combos += get_combos(workflows, test.result, new_accepted)
        completed_tests.append(test)

    return combos
