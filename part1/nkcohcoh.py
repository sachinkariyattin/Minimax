import copy
import sys
import numpy as np

# count number of marbles in a column
def count_col(current_board, marble_color):
    for col in range(0, n):
        count = 0
        for row in range(0, n):
            if current_board[row][col] == marble_color:
                count += 1
            if count == k:
                return True
            if current_board[row][col] != marble_color:
                count = 0
    return False

# count number of marbles in a row
def count_row(current_board, marble_color):
    for row in range(0, n):
        count = 0
        for col in range(0, n):
            if current_board[row][col] == marble_color:
                count += 1
            if count == k:
                return True
            if current_board[row][col] != marble_color:
                count = 0

    return False

# count number of marbles in diagonals
def count_diagonals(current_board, marble_color):

    # get all possible diagonals
    # Ref - http://stackoverflow.com/a/6313414/3446129
    a = np.array(current_board)
    diags = [a[::-1, :].diagonal(i) for i in range(-a.shape[0] + 1, a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0], -1))
    dia_list = [r.tolist() for r in diags if len(r) >= k]

    for each_diagonal in dia_list:
        count = 0
        for dia_element in each_diagonal:
            if dia_element == marble_color:
                count += 1
            if count == k:
                return True
            if dia_element != marble_color:
                count = 0
    return False

# count number of black and white marbles
def count_marbles(current_board):
    countW = 0
    countB = 0
    for i in range(0, n):
        for j in range(0, n):
            if current_board[i][j] == 'w':
                countW = countW + 1
            elif current_board[i][j] == 'b':
                countB = countB + 1
    return (countW, countB)

# check whose turn to play
def check_turn(current_board):
    countW, countB = count_marbles(current_board)

    if countB == countW:
        return 'w'
    else:
        return 'b'

# count open diagonals,rows and columns for each player
def count_possibilities(current_board, marble_color):
    row_total = 0
    for row in range(0, n):
        count = 0
        col = 0
        while col < n:
            if current_board[row][col] != marble_color and current_board[row][col] != '.':
                count = 0
            if current_board[row][col] == marble_color or current_board[row][col] == '.':
                count += 1
                if count == k:
                    row_total += 1
                    col -= 1
                    count = 0
            col += 1

    col_total = 0
    for col in range(0, n):
        count = 0
        row = 0
        while row < n:
            if current_board[row][col] != marble_color and current_board[row][col] != '.':
                count = 0
            if current_board[row][col] == marble_color or current_board[row][col] == '.':
                count += 1
                if count == k:
                    col_total += 1
                    row -= 1
                    count = 0
            row += 1

    # get all possible diagonals
    a = np.array(current_board)
    diags = [a[::-1, :].diagonal(i) for i in range(-a.shape[0] + 1, a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0], -1))
    dia_list = [r.tolist() for r in diags if r >= 2]

    dia_total = 0
    for each_diagonal in dia_list:
        count = 0
        dia_element = 0
        while dia_element < len(each_diagonal):
            if each_diagonal[dia_element] != marble_color and each_diagonal[dia_element] != '.':
                count = 0
            if each_diagonal[dia_element] == marble_color or each_diagonal[dia_element] == '.':
                count += 1
                if count == k:
                    dia_total += 1
                    dia_element -= 1
                    count = 0
            dia_element += 1

    return row_total + col_total + dia_total


# evaluation function : check for diagonals, rows and columns
def eval_fun(current_board):
    white_options = count_possibilities(current_board, 'w')
    black_options = count_possibilities(current_board, 'b')

    return black_options - white_options

# check if terminal state and return score
def count_score(gen_state, current_depth):
    countW, countB = count_marbles(gen_state)
    global depth

    if count_row(gen_state,'w') or count_col(gen_state,'w') or count_diagonals(gen_state,'w'):
        if countW + countB == n*n:
            depth = 101
        return -10000
    elif count_row(gen_state,'b') or count_col(gen_state,'b') or count_diagonals(gen_state,'b'):
        if countW + countB == n*n:
            depth = 101
        return 10000
    elif countW + countB == n*n:
        depth = 101
        return 0
    elif current_depth == depth:
        return eval_fun(gen_state)
    else:
        return 5000



# generate successors based on the current board state
def generate_successors(current_board):
    turn = check_turn(current_board)
    successors = []

    for i in range(0, n):
        for j in range(0, n):
            if current_board[i][j] == '.':
                copy_board = copy.deepcopy(current_board)
                if turn == 'w':
                    copy_board[i][j] = 'w'
                else:
                    copy_board[i][j] = 'b'

                successors.append(copy_board)
    return successors


# max function
def max_func(current_board, current_depth, alpha, beta):
    max_successors = generate_successors(current_board)
    current_depth += 1
    best_move = []

    current_best_score = -100000

    for s in max_successors:
        score = count_score(s, current_depth)
        if score != 5000:
            current_best_score = score
        else:
            move,current_best_score = min_func(s, current_depth, alpha, beta)
        if current_best_score == -100000 or current_best_score > alpha:
            alpha = current_best_score
            best_move = s
            if alpha >= beta:
                return best_move, alpha

    return best_move, alpha

# min function
def min_func(current_board, current_depth, alpha, beta):
    min_successors = generate_successors(current_board)
    current_depth += 1
    best_move = []

    current_best_score = 100000

    for s in min_successors:
        score = count_score(s, current_depth)
        if score != 5000:
            current_best_score = score
        else:
            move, current_best_score = max_func(s, current_depth, alpha, beta)
        if current_best_score == 100000 or current_best_score < beta:
            beta = current_best_score
            best_move = s
            if alpha >= beta:
                return best_move, beta

    return best_move, beta


# minimax function
def minimax(current_board):

    turn = check_turn(current_board)

    if turn == 'w':
        next_state,score = max_func(current_board, 0, -100000, 100000)
        return next_state
    else:
        next_state, score = min_func(current_board, 0, -100000, 100000)
        return next_state


# convert board to list of lists for computation
def convert_board(initial_board):
    tolist = list(initial_board)
    row_list = zip(*[iter(tolist)]*n)
    tuple_to_list = [list(i) for i in row_list]
    return tuple_to_list

def get_next_step(converted_board):
    global depth
    while depth < 50:
        next_step = minimax(converted_board)
        final_step = ""
        # convert it to string
        for k in next_step:
            final_step += "".join(k)
        print "New Board: "
        print ("".join(final_step))
        print
        depth += 1

# get initial board
n = int(sys.argv[1])
k = int(sys.argv[2])
board = sys.argv[3]
time = int(sys.argv[4])

if n <= 3 and time >= 5:
    depth = 6
elif n > 3 and n <= 7 and time >= 15:
    depth = 4
else:
    depth = 1

converted_board = convert_board(board)
print "Thinking! Please wait......"
get_next_step(converted_board)