import math
from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass, field
from abc import abstractmethod
from collections import defaultdict, deque


@dataclass
class Module:
    name: str
    state: bool = False
    outputs: list[str] = field(default_factory=list)
    inputs: set[str] = field(default_factory=set)

    lo = False
    hi = True

    @abstractmethod
    def receive(self, src: str, pulse: bool, button_press: int):
        return deque([])

    
    def send(self, pulse: bool) -> deque[tuple[str, bool]]:
        pulses = deque([])
        for output in self.outputs:
            pulses.append((self.name, output, pulse))
        return pulses


class FlipFlopModule(Module):
    def receive(self, src: str, pulse: bool, button_press: int=0) -> deque[tuple[str, bool]]:
        if pulse == Module.lo:
            self.state = not self.state
            return self.send(self.state)
        return deque()


@dataclass
class ConjunctionModule(Module):
    input_pulses: defaultdict[str, bool] = field(default_factory=lambda: defaultdict(bool))
    hi_pulses: defaultdict[str, list] = field(default_factory=lambda: defaultdict(list))

    def receive(self, src: str, pulse: bool, button_press: int=0) -> deque[tuple[str, bool]]:
        self.input_pulses[src] = pulse
        if len(self.hi_pulses[src]) < 2 and self.input_pulses[src] == Module.hi:
            self.hi_pulses[src].append(button_press)
        all_hi = True
        for name in self.inputs:
            if self.input_pulses[name] == Module.lo:
                all_hi = False
                break
        return self.send(not all_hi)

    def all_hi(self):
        for name in self.inputs:
            if self.input_pulses[name] == Module.lo:
                return False
        return True


class BroadcastModule(Module):
    def receive(self, src: str, pulse: bool, button_press: int=0) -> deque[tuple[str, bool]]:
        return self.send(pulse)


class MachineOnModule(Module):
    received: bool = False
    def receive(self, src: str, pulse: bool, button_press: int=0):
        if pulse == Module.lo:
            self.received = True
        return deque([])



@advent.parser(20)
def parse(file: TextIOWrapper):
    modules: dict[str, Module] = {}
    inputs: defaultdict[str, set] = defaultdict(set)
    for line in file.readlines():
        name, rhs = line.strip().split(' -> ')
        outputs = rhs.split(', ')
        if line[0] == '%':
            name = name[1:]
            modules[name] = FlipFlopModule(name=name, outputs=outputs)
        elif line[0] == '&':
            name = name[1:]
            modules[name] = ConjunctionModule(name=name, outputs=outputs)
        elif name == 'broadcaster':
            modules[name] = BroadcastModule(name=name, outputs=outputs)
        for module in outputs:
            inputs[module].add(name)
    
    modules['rx'] = MachineOnModule('rx')
    for module in modules.values():
        module.inputs = inputs[module.name]
    return modules


@advent.day(20, part=1)
def solve1(modules: dict[str, Module]):
    lo = hi = 0
    for _ in range(1000):
        l, h = push_button(modules)
        lo += l
        hi += h
    return lo * hi


@advent.day(20, part=2)
def solve2(modules: dict[str, Module]):
    checks = set()
    rx_input = next(iter(modules['rx'].inputs))
    for ipt in modules[rx_input].inputs:
        checks.add(next(iter(modules[ipt].inputs)))
    presses = 1
    nums = defaultdict(set)
    while len(checks) > 0:
        push_button(modules, presses)
        to_remove = set()
        for m in checks:
            hi_pulses = modules[m].hi_pulses.values()
            if len(hi_pulses) == len(modules[m].inputs) and all(len(pulses) == 2 for pulses in hi_pulses):
                for a, b in hi_pulses:
                    nums[m].add(b - a)
                to_remove.add(m)
        checks -= to_remove
        presses += 1
    finals = set()
    for n in nums.values():
        finals.add(max(n))
    return math.lcm(*finals)


def push_button(modules: dict[str, Module], press: int=0):
    hi = 0
    lo = 1
    q = modules['broadcaster'].send(False)
    while len(q) > 0:
        src, dst, pulse = q.popleft()
        if pulse:
            hi += 1
        else:
            lo += 1
        q += modules[dst].receive(src, pulse, press)
    return lo, hi
