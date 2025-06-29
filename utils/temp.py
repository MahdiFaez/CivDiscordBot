# def calc_elo_change(self, player_elo, opp_elo, result, k=32):
#     expected = 1 / (1 +10**((opp_elo - player_elo)/400))
#     return round(k*(result-expected))

# print(calc_elo_change("self", 1000, 1031, 1))


data={
    "_phil99": {
        "wins": 3,
        "games": 3,
        "elo": 1044
    },
    "_maf.": {
        "wins": 0,
        "games": 3,
        "elo": 956
    }
}

print(data.items())

ranked = sorted(data.items(), key=lambda i: i[1]["elo"], reverse=True)
print(ranked)