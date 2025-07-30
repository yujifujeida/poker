import pytest
from hand_checker import compare_hands

# 各役ごとにサンプル手札とボード（勝つために最低限必要な形で構成）
sample_hands = {
    "High Card": (["8C", "7D"], ["2S", "5H", "9D", "JC", "KD"]),
    "One Pair": (["8C", "8D"], ["2S", "5H", "9D", "JC", "KD"]),
    "Two Pair": (["8C", "9D"], ["8H", "9H", "2S", "5H", "KD"]),
    "Three of a Kind": (["8C", "8D"], ["8H", "2S", "5H", "JD", "KD"]),
    "Straight": (["8C", "7D"], ["5H", "6S", "9D", "TC", "2H"]),
    "Flush": (["2S", "9S"], ["4S", "5S", "8S", "JS", "KD"]),
    "Full House": (["8C", "8D"], ["8H", "5H", "5D", "JC", "KD"]),
    "Four of a Kind": (["8C", "8D"], ["8H", "8S", "5H", "JC", "KD"]),
    "Straight Flush": (["6S", "7S"], ["8S", "9S", "TS", "2H", "3C"])
}

# 役の強さの順番（インデックスが強さ）
hand_rankings = list(sample_hands.keys())

@pytest.mark.parametrize("i", range(len(hand_rankings)))
@pytest.mark.parametrize("j", range(len(hand_rankings)))
def test_hand_strength(i, j):

    stronger_name = hand_rankings[max(i, j)]
    weaker_name = hand_rankings[min(i, j)]

    # プレイヤー1に強い役、プレイヤー2に弱い役を与える
    hole1, board1 = sample_hands[stronger_name]
    hole2, board2 = sample_hands[weaker_name]

    # 両方の役が成立するボードが必要なため、プレイヤーごとの専用ボードを使用
    result, _, _ = compare_hands(hole1, hole2, board1, board2)

    if i == j:
        assert result == "Tie", f"{stronger_name} vs {weaker_name} で Tieにならない: result={result}"
    else:
        assert result == "Player 1 wins", f"{stronger_name} vs {weaker_name} で Player 1 が勝たない: result={result}"

@pytest.mark.parametrize("desc, hole1, hole2, board, expected", [
    (
        "One Pair: pair of Jacks beats pair of Tens",
        ["JH", "JS"],
        ["TH", "TS"],
        ["2C", "3D", "5S", "7H", "9C"],
        "Player 1 wins"
    ),
    (
        "Two Pair: Aces and Kings beats Kings and Queens",
        ["AH", "AD"],
        ["KH", "KD"],
        ["KC", "QS", "AC", "3H", "2D"],
        "Player 1 wins"
    ),
    (
        "Two Pair: same top pair, second pair decides",
        ["KH", "QH"],
        ["KS", "9S"],
        ["KC", "QS", "9C", "3H", "2D"],
        "Player 1 wins"
    ),
    (
        "Three of a Kind: 9s beat 8s",
        ["9H", "9D"],
        ["8H", "8D"],
        ["9C", "8C", "2S", "4D", "6H"],
        "Player 1 wins"
    ),
    (
        "Four of a Kind: Kings beat Queens",
        ["KH", "KD"],
        ["QH", "QD"],
        ["KC", "KS", "QC", "QS", "2D"],
        "Player 1 wins"
    ),
    (
        "Full House: 9 over 2 beats 8 over 7",
        ["9H", "9D"],
        ["8H", "8D"],
        ["9C", "2D", "2C", "8C", "7D"],
        "Player 1 wins"
    ),
    (
        "Full House: Same trips (9s), but pair of 4s beats pair of 2s",
        ["9H", "4D"],  
        ["9S", "2C"],
        ["9D", "4H", "2D", "9C", "3S"],
        "Player 1 wins"
    ),
    (
        "Straight: AKQJT beats QJT98",
        ["AH", "KD"],  
        ["9S", "8C"],
        ["TD", "JH", "QD", "2C", "3S"],
        "Player 1 wins"
    ),
    (
        "Straight: 76543 beats 54321",
        ["7S", "6C"],
        ["AH", "KD"],
        ["5D", "4H", "3D", "2C", "9S"],
        "Player 1 wins"
    ),
    (
        "Flush: Player 1 has A-high flush, Player 2 has Q-high flush",
        ["AH", "KH"],
        ["QH", "JH"],
        ["2H", "5H", "7H", "9C", "3D"],
        "Player 1 wins"
    ),
    (
        "Straight Flush: Player 1 has 9-high SF, Player 2 has 7-high SF",
        ["9H", "8H"],
        ["4H", "3H"],
        ["7H", "5H", "6H", "QD", "KS"],
        "Player 1 wins"
    ),
    (
        "Straight Flush Wheel: Player 1 has A-5 SF (wheel), Player 2 has 7-high SF",
        ["6H", "7H"],
        ["AH", "2H"],
        ["3H", "4H", "5H", "QD", "KS"],
        "Player 1 wins"
    )
])
def test_same_rank_comparison(desc, hole1, hole2, board, expected):
    result, _, _ = compare_hands(hole1, hole2, board, None)
    assert result == expected, f"{desc} → Expected: {expected}, Got: {result}"

@pytest.mark.parametrize("desc, hole1, hole2, board, expected", [
    (
        "High Card: 1st kicker (A vs K)",
        ["AH", "7D"],
        ["KD", "9S"],
        ["3C", "4D", "6H", "2S", "8C"],
        "Player 1 wins"
    ),
    (
        "High Card: 2nd kicker (A9 vs A8)",
        ["AH", "TD"],
        ["AD", "9S"],
        ["3C", "4D", "7H", "2S", "6C"],
        "Player 1 wins"
    ),
    (
        "High Card: 3rd kicker (AKQ vs AKJ)",
        ["AH", "QH"],
        ["AD", "JD"],
        ["KH", "8C", "7S", "4D", "2H"],
        "Player 1 wins"
    ),
    (
        "High Card: 4th kicker (AKQ9 vs AKQ8)",
        ["AH", "9H"],
        ["AD", "8D"],
        ["KH", "QC", "7S", "3D", "2H"],
        "Player 1 wins"
    ),
    (
        "High Card: 5th kicker (AKQ98 vs AKQ97)",
        ["AH", "8H"],
        ["AD", "7D"],
        ["KH", "QC", "9S", "3D", "2H"],
        "Player 1 wins"
    ),
    (
        "One Pair: 1st kicker decides (Pair of 9s + A vs K)",
        ["9H", "AH"],
        ["9D", "KH"],
        ["9S", "2C", "4D", "6H", "8S"],
        "Player 1 wins"
    ),
    (
        "One Pair: 2nd kicker decides (Pair of 9s + A8 vs A7)",
        ["9H", "8H"],
        ["9D", "7D"],
        ["9S", "2C", "4D", "AH", "5S"],
        "Player 1 wins"
    ),
    (
        "One Pair: 3rd kicker decides (Pair of 9s + A87 vs A86)",
        ["9H", "7H"],
        ["9D", "6D"],
        ["9S", "2C", "4D", "AH", "8S"],
        "Player 1 wins"
    ),
    (
        "Two Pair: Same pairs (Queens & Jacks), kicker 9 vs 8 → 9 wins",
        ["QH", "9C"],
        ["QD", "8S"],
        ["QS", "JC", "JD", "3H", "5S"],
        "Player 1 wins"
    ),
    (
        "Trips (Eights): kicker A vs Q → A wins",
        ["8H", "AH"],
        ["8D", "QH"],
        ["8S", "2C", "3D", "4H", "8C"],
        "Player 1 wins"
    ),
    (
        "Trips (Tens): 2nd kicker decides J vs 9",
        ["TS", "JH"],
        ["TH", "9D"],
        ["TC", "7H", "AC", "5D", "TD"],
        "Player 1 wins"
    )
])
def test_high_card_kicker_levels(desc, hole1, hole2, board, expected):
    result, _, _ = compare_hands(hole1, hole2, board, None)
    assert result == expected, f"{desc} → Expected: {expected}, Got: {result}"