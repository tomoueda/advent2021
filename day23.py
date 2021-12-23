inputs = []

inputs.append("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""")

inputs.append("""#############
#...........#
###D#A#C#D###
  #B#C#B#A#
  #########
""")

#D#C#B#A#
#D#B#A#C#
board1 = (None, None, None, None, None, None, None, \
        'B', 'D', 'D', 'A', 'C', 'C', 'B', 'D', 'B', 'B', 'A', \
        'C', 'D', 'A', 'C', 'A')
board2 = (None, None, None, None, None, None, None, \
        'D', 'D', 'D', 'B', 'A', 'C', 'B', 'C', 'C', 'B', 'A', \
        'B', 'D', 'A', 'C', 'A')

import heapq
import sys
board = board1

heap = [(0, board, [])]

lt = 7
lt2 = 8
lt3 = 9
lb= 10
mlt = 11
mlt2 = 12
mlt3 = 13
mlb = 14
mrt = 15
mrt2 = 16
mrt3 = 17
mrb = 18
rt = 19
rt2 = 20
rt3 = 21
rb = 22 

def new_board():
    return board1


def print_board(board):
    def _idx(idx):
        return board[idx] if board[idx] is not None else '.'
    print _idx(0) + _idx(1) + '.' + _idx(2) + '.' + _idx(3) + \
            '.' + _idx(4) + '.' + _idx(5) + _idx(6)
    print '##' + _idx(lt) + '#' + _idx(mlt) + '#' + \
            _idx(mrt) + '#' + _idx(rt) + '##'
    print '##' + _idx(lt2) + '#' + _idx(mlt2) + '#' + \
            _idx(mrt2) + '#' + _idx(rt2) + '##'
    print '##' + _idx(lt3) + '#' + _idx(mlt3) + '#' + \
            _idx(mrt3) + '#' + _idx(rt3) + '##'
    print '##' + _idx(lb) + '#' + _idx(mlb) + '#' + \
            _idx(mrb) + '#' + _idx(rb) + '##'


def next_board(board, begin, end):
    mutable = list(board)
    piece = board[begin]
    mutable[begin] = None
    mutable[end] = piece
    return tuple(mutable)

cost_map = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
def get_cost(piece, steps):
    return cost_map[piece] * steps

def get_possible_ends(start, board):
    checks = set()
    # hallway starts
    def check_rooms(top, bottom, step):
        checks = set() 
        if board[bottom] == None: 
            checks.add((bottom, step + 4))
            return checks
        if board[top+2] == None and board[bottom] == board[start]:
            checks.add((top + 2, step + 3))
            return checks
        if board[top+1] == None and board[bottom] == board[start]:
            checks.add((top + 1, step + 2))
            return checks
        if board[top] == None and board[bottom] == board[start]:
            checks.add((top, step + 1))
        return checks
        
    def check_right():
        checks = set() 
        step = 0
        if start in {0}:
            if board[1] is not None:
                return checks
            step += 1

        if start in {0, 1}: 
            checks |= check_rooms(lt, lb, step)
            if board[2] is not None:
                return checks
            step += 2 

        if start in {0, 1, 2}: 
            checks |= check_rooms(mlt, mlb, step)
            if board[3] is not None:
                return checks
            step += 2 

        if start in {0, 1, 2, 3}: 
            checks |= check_rooms(mrt, mrb, step)
            if board[4] is not None:
                return checks
            step += 2 

        if start in {0, 1, 2, 3, 4}: 
            checks |= check_rooms(rt, rb, step)
        return checks

    def check_left():
        checks = set() 
        step = 0
        if start in {6}:
            if board[5] is not None:
                return checks
            step += 1

        if start in {6, 5}:
            checks |= check_rooms(rt, rb, step)
            if board[4] is not None:
                return checks 
            step += 2 

        if start in {6, 5, 4}:
            checks |= check_rooms(mrt, mrb, step)
            if board[3] is not None:
                return checks
            step += 2 

        if start in {6, 5, 4, 3}:
            checks |= check_rooms(mlt, mlb, step)
            if board[2] is not None:
                return checks
            step += 2 

        if start in {6, 5, 4, 3, 2}:
            checks |= check_rooms(lt, lb, step)
        return checks

    checks |= check_right()
    checks |= check_left()

    start_step = 0
    def check_above(bottom):
        start_step = 0
        if start in {bottom, bottom - 1, bottom - 2}:
            if board[start - 1] is not None:
                return -1 
            start_step += 3 - (bottom - start) 
        return start_step 

    for bottom_slots in {lb, mlb, mrb, rb}:
        start_step = check_above(bottom_slots)
        if start_step == -1:
            return checks

    def r(start, end):
        return set(range(start, end + 1))

    def from_room_check_right():
        step = start_step
        if start in r(rt, rb):
            if board[4] is not None:
                return checks
            step += 2
            checks.add((4, step))
        if start in r(mrt, rb):
            if board[3] is not None:
                return checks
            step += 2
            checks.add((3, step))
        if start in r(mlt, rb):
            if board[2] is not None:
                return checks
            step += 2
            checks.add((2, step))
        if start in r(lt, rb):
            if board[1] is None:
                step += 2 
                checks.add((1, step))
                if board[0] is None:
                    step += 1 
                    checks.add((0, step))
        return checks

    def from_room_check_left():
        step = start_step
        if start in r(lt, lb):
            if board[2] is not None:
                return checks
            step += 2
            checks.add((2, step))
        if start in r(lt, mlb):
            if board[3] is not None:
                return checks
            step += 2
            checks.add((3, step))
        if start in r(lt, mlb):
            if board[4] is not None:
                return checks
            step += 2
            checks.add((4, step))
        if start in r(lt, rb):
            if board[5] is None:
                step += 2
                checks.add((5, step))
                if board[6] is None:
                    step += 1 
                    checks.add((6, step))
        return checks

    checks |= from_room_check_right()
    checks |= from_room_check_left()
    return checks

"""(11, 2) (9, 3) (3, 11) (10, 3), (2, 10) (7, 2), (2, 9) (13, 4) (14 5)""" 
def all_next_states(board, history):
#    print_board(board)
    for start in range(23):
        if board[start] is not None:
            pos = get_possible_ends(start, board)
#             for h in history:
#                 if (14, 5) in h and len(history) == 9:
#                     print_board(board)
#                     print start, pos
#            print start, pos
            for end, steps in pos:
                yield (get_cost(board[start], steps), \
                        next_board(board, start, end), (start, end))

def end_state(board):
    t = lt
    for _ in range(4):
        if board[t] != 'A':
            return False
        t += 1
    for _ in range(4):
        if board[t] != 'B':
            return False
        t += 1
    for _ in range(4):
        if board[t] != 'C':
            return False
        t += 1
    for _ in range(4):
        if board[t] != 'D':
            return False
        t += 1
    return True

min_cost = sys.maxsize
min_cost_map = {}
save = None
while len(heap) != 0:
    cost, board, action = heapq.heappop(heap)
    sys.stdout.flush()
    sys.stdout.write('\r' +\
            str(float(cost) / 44169))
    if min_cost < cost:
        break
    visited = set() 
    if board not in visited:
        visited.add(board)
        for ncost, next_state, naction in all_next_states(board, \
                action):
            next_action = list(action)
            next_action.append((naction, ncost))
            next_cost = cost + ncost
            if end_state(next_state):
                if min_cost < next_cost:
                    save = next_action
                min_cost = min(min_cost, next_cost)
            else:
                if next_state in min_cost_map:
                    if next_cost >= min_cost_map[next_state]:
                        continue
                min_cost_map[next_state] = next_cost
                heapq.heappush(heap, (next_cost, next_state, \
                        next_action))


print min_cost

def play_back():
    a = new_board()
    for s in save:
        a = next_board(a, s[0][0], s[0][1])
        print(s[0], s[1])
        print_board(a)
        print('\n')
