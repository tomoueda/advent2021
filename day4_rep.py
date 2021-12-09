inputs = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

lines = filter(lambda line: line != '', inputs.split('\n'))
calls = lines[0].split(',')
board_lines = lines[1:]
num_boards = len(board_lines) / 5
boards = []
for i in range(num_boards):
    board = [line.split() for line in board_lines[i*5:i*5+5]]
    boards.append(board)

def check_bingo(board):
    # check row
    for row in board:
        if row == [True, True, True, True, True]:
            return True
    # check col
    for i in range(5):
        if board[i][0] == True and board[i][1] == True \ 
        and board[i][2] == True and board[i][3] == True \ 
        and board[i][4] == True:
            return True
    return False


for call in calls:
    for board in boards:
        for i in range(5):
            if board[i] == call:
                board[i] = True
        if check_bingo(board):
            print(int(call) * unmarked(call))
    else:
        continue
    break
