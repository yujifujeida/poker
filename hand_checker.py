import itertools
from collections import Counter

# カードの強さ順（2〜A）
CARD_ORDER = '23456789TJQKA'
CARD_VALUE = {r: i for i, r in enumerate(CARD_ORDER)}

HAND_RANKS = [
    "High Card", 
    "One Pair", 
    "Two Pair", 
    "Three of a Kind", 
    "Straight",
    "Flush", 
    "Full House", 
    "Four of a Kind", 
    "Straight Flush"
]

def card_value(card):
    return CARD_VALUE[card[0]]

def hand_rank(hand):
    # hand: 5枚のカード ["AS", "KH", "QC", "JD", "TS"]
    ranks = sorted([card_value(c) for c in hand], reverse=True)
    suits = [c[1] for c in hand]
    count = Counter(ranks)
    rank_count = sorted(count.items(), key=lambda x: (-x[1], -x[0]))
    rank_vals = [x[0] for x in rank_count]

    is_flush = len(set(suits)) == 1
    is_straight = (
        len(set(ranks)) == 5 and
        max(ranks) - min(ranks) == 4
    )
    is_wheel = (set(ranks) == {12, 3, 2, 1, 0})  # A-2-3-4-5

    if is_flush and (is_straight or is_wheel):
        return (8, [0 if is_wheel else max(ranks)])  # Straight Flush
    elif rank_count[0][1] == 4:
        return (7, [rank_vals[0], rank_vals[1]])  # Four of a Kind
    elif rank_count[0][1] == 3 and rank_count[1][1] == 2:
        return (6, [rank_vals[0], rank_vals[1]])  # Full House
    elif is_flush:
        return (5, ranks)  # Flush
    elif (is_straight or is_wheel):
        return (4, [0 if is_wheel else max(ranks)])  # Straight
    elif rank_count[0][1] == 3:
        return (3, [rank_vals[0]] + rank_vals[1:])  # Three of a Kind
    elif rank_count[0][1] == 2 and rank_count[1][1] == 2:
        return (2, sorted([rank_vals[0], rank_vals[1]], reverse=True) + [rank_vals[2]])  # Two Pair
    elif rank_count[0][1] == 2:
        return (1, [rank_vals[0]] + rank_vals[1:])  # One Pair
    else:
        return (0, ranks)  # High Card

def best_hand(cards):
    best = max(
        (hand_rank(list(combo)) for combo in itertools.combinations(cards, 5)),
        key=lambda x: x
    )
    return best

def compare_hands(hole1, hole2, board1, board2):
    cards1 = hole1 + board1
    cards2 = hole2 + (board1 if board2 is None else board2)
    rank1 = best_hand(cards1)
    rank2 = best_hand(cards2)

    result = "Player 1 wins" if rank1 > rank2 else "Player 2 wins" if rank2 > rank1 else "Tie"
    return result, rank1, rank2