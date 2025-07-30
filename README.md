## pokerの役判定をするコード

実行例
```
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

# テスト用のカード（例: "AH"はAのハート、"9D"は9のダイヤ）
hole1 = ["AH", "KH"]  # Player 1の手札
hole2 = ["QH", "JD"]  # Player 2の手札
board = ["TH", "9H", "8H", "2C", "3S"]  # 共通ボードカード

# 実行してみる
result, rank1, rank2 = compare_hands(hole1, hole2, board, None)

print("Result:", result)
print("Player 1 Hand Strength:", HAND_RANKS[rank1[0]])
print("Player 2 Hand Strength:", HAND_RANKS[rank2[0]])
```

実行結果
```
Result: Player 1 wins
Player 1 Hand Strength: Flush
Player 2 Hand Strength: Straight
```
