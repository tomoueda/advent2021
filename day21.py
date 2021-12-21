inputs = []
inputs.append("""Player 1 starting position: 4
Player 2 starting position: 8""")
inputs.append("""Player 1 starting position: 7
Player 2 starting position: 5""")

lines = inputs[1].split('\n')
p1_pos = int(lines[0][-1]) - 1
p2_pos = int(lines[1][-1]) - 1

# pos = [p1_pos, p2_pos]
# scores = [0, 0]



def score(current_pos, move):
    next_pos = current_pos + move
    next_pos %= 10
    return (next_pos + 1, next_pos)

#prev = 0
#c = 0
#
#def roll():
#    global prev, c
#    r = range(prev, prev + 3)
#    n = sum(list(map(lambda n: n % 100 + 1, r)))
#    c += 3 
#    prev += 3
#    prev %= 100
#    return n
#
#
#
#player = 0
#while scores[0] < 1000 and scores[1] < 1000:
#    move = roll()
#    s, pos[player] = score(pos[player], move)
#    scores[player] += s
#    player = 1 if player == 0 else 0


# print min(scores) * c
from collections import Counter
moves = Counter()
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            moves[i + j + k] += 1


wins = [0, 0] 
memo = {} 
def simulate_quantum_turn(player, positions, scores):
    if (player, positions, scores) in memo:
        return list(memo[(player, positions, scores)])
    w = [0, 0] 
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                move = i + j + k
                s, p = score(positions[player], move)
                if scores[player] + s >= 21:
                    w[player] += 1 
                else: 
                    n_pos = list(positions)
                    n_pos[player] = p
                    n_sco = list(scores)
                    n_sco[player] += s
                    t = simulate_quantum_turn(1 if player == 0 else 0, \
                            (n_pos[0], n_pos[1]), (n_sco[0], n_sco[1]))
                    w[0] += t[0]
                    w[1] += t[1]
    memo[(player, positions, scores)] = list(w)
    return list(w)

print (0, (p1_pos, p2_pos), (0, 0))
w = simulate_quantum_turn(0, (p1_pos, p2_pos), (0, 0))
print w


