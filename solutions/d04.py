import re
from .lib.advent import advent
from io import TextIOWrapper
from dataclasses import dataclass


@dataclass
class Card:
    winners: set[int]
    mine: set[int]


@advent.parser(4)
def parse(file: TextIOWrapper):
    cards = []
    for line in file.readlines():
        groups = re.search(r'((\d+ +)+)\| +((\d+ *)+)\n', line).groups()
        winners = set(map(int, groups[0].split()))
        mine = set(map(int, groups[2].split()))
        cards.append(Card(winners, mine))
    return cards


@advent.day(4, part=1)
def solve1(cards: list[Card]):
    return sum(int(2**(len(card.winners & card.mine)-1)) for card in cards)


@advent.day(4, part=2)
def solve1(cards: list[Card]):
    counts = [1 for _ in range(len(cards))]
    for i,card in enumerate(cards):
        num_winners = len(card.winners & card.mine)
        for c in range(i+1, i+num_winners+1):
            counts[c] += counts[i]
    return sum(counts)
