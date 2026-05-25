
#  Funções do 8-puzzle

GOAL  = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVES = ['U', 'D', 'L', 'R']
DELTA = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}

def apply_move(state, move):
    s = list(state)
    i = s.index(0)
    bi, bj = i // 3, i % 3
    di, dj = DELTA[move]
    ni, nj = bi + di, bj + dj
    if 0 <= ni < 3 and 0 <= nj < 3:
        t = ni * 3 + nj
        s[i], s[t] = s[t], s[i]
        return tuple(s)
    return None

def apply_sequence(state, moves):
    valid = 0
    for m in moves:
        r = apply_move(state, m)
        if r:
            state, valid = r, valid + 1
    return state, valid

def manhattan(state):
    pos = {v: (v-1)//3 if v else 2 for v in range(9)}
    col = {v: (v-1)%3  if v else 2 for v in range(9)}
    return sum(abs(i//3 - pos[v]) + abs(i%3 - col[v])
               for i, v in enumerate(state) if v)

def solvable(state):
    f = [x for x in state if x]
    inv = sum(f[i] > f[j] for i in range(len(f)) for j in range(i+1, len(f)))
    return inv % 2 == 0

def extract(initial, sequence):
    state, sol = initial, []
    for m in sequence:
        if state == GOAL: break
        r = apply_move(state, m)
        if r: sol.append(m); state = r
    return sol, state
