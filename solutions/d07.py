from .lib.advent import advent
from io import TextIOWrapper
from enum import Enum, auto
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cmp_to_key
from itertools import combinations_with_replacement


class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


@dataclass
class Hand:
    hand: str
    bid: int
    encoded_hand: list[int] = field(default_factory=list)
    hand_type: HandType = HandType.HIGH_CARD


CARD_ENCODINGS_PART_1 = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'J': 10,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1
}

CARD_ENCODINGS_PART_2 = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1
}


@advent.parser(7)
def parse(file: TextIOWrapper):
    hands = []
    for line in file.readlines():
        hand_str, bid = line.strip().split()
        hands.append(Hand(hand_str, int(bid)))
    return hands


@advent.day(7, part=1)
def solve1(ipt: list[Hand]):
    for hand in ipt:
        hand.encoded_hand = [CARD_ENCODINGS_PART_1[c] for c in hand.hand]

    buckets: dict[HandType, list[Hand]] = {hand_type: [] for hand_type in HandType}
    for row in ipt:
        parse_hand(row)
        buckets[row.hand_type].append(row)

    for bucket in buckets.values():
        bucket.sort(key=cmp_to_key(compare))
    
    return count_winnings(buckets)


@advent.day(7, part=2)
def solve2(ipt: list[Hand]):
    for hand in ipt:
        hand.encoded_hand = [CARD_ENCODINGS_PART_2[c] for c in hand.hand]

    buckets: dict[HandType, list[Hand]] = {hand_type: [] for hand_type in HandType}
    j_set = {'J'}
    for hand in ipt:
        parse_hand(hand)
        best = hand.hand_type
        no_joker = set(hand.hand) - j_set
        if set(hand.hand) != no_joker:
            for combo in combinations_with_replacement(no_joker, hand.hand.count('J')):
                curr = hand.hand
                for c in combo:
                    curr = curr.replace('J', c, 1)
                new = Hand(curr, hand.bid)
                parse_hand(new)
                if new.hand_type.value > best.value:
                    best = new.hand_type
            hand.hand_type = best
        buckets[hand.hand_type].append(hand)

    for bucket in buckets.values():
        bucket.sort(key=cmp_to_key(compare))
    
    return count_winnings(buckets)


def compare(a: Hand, b: Hand) -> int:
    idx = 0
    while a.encoded_hand[idx] - b.encoded_hand[idx] == 0:
        idx += 1
    return a.encoded_hand[idx] - b.encoded_hand[idx]


def parse_hand(hand: Hand):
    card_counts = defaultdict(int)
    for card in hand.hand:
        card_counts[card] += 1

    count_counts = defaultdict(int)
    for card, count in card_counts.items():
        count_counts[count] += 1

    hand.hand_type = HandType.HIGH_CARD
    if count_counts.get(5):
        hand.hand_type = HandType.FIVE_OF_A_KIND
    elif count_counts.get(4):
        hand.hand_type = HandType.FOUR_OF_A_KIND
    elif count_counts.get(2) and count_counts.get(3):
        hand.hand_type = HandType.FULL_HOUSE
    elif count_counts.get(3):
        hand.hand_type = HandType.THREE_OF_A_KIND
    elif count_counts.get(2) == 2:
        hand.hand_type = HandType.TWO_PAIR
    elif count_counts.get(2):
        hand.hand_type = HandType.ONE_PAIR


def count_winnings(buckets: dict[HandType, list[Hand]]):
    winnings = 0
    idx = 1
    for hand_type in HandType:
        for hand in buckets[hand_type]:
            winnings += idx * hand.bid
            idx += 1
    return winnings
