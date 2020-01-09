# Creating the evaluation function
# The evaluation function will find which player can get first to each tile
# In addition we will keep the moves that we can get by 1 step
# -- we will create 2 new matrices that in each position will be the minimum number of step
# -- that require to get there for each player

from Constants import EMPTY_SPACE, BLACK_QUEEN, WHITE_QUEEN
from collections import deque
from Rules import IsMoveLegal
from copy import deepcopy

state = []
size = 0
player_board = []
enemy_board = []
white_mobility = 0
black_mobility = 0
player_color = ""


def territory_mobility_evaluation(board_state, board_size, color):
    global state
    global size
    global player_board
    global enemy_board
    global player_color

    state = board_state
    size = board_size
    white_board = [[0 for x in range(int(size))] for y in range(int(size))]
    black_board = [[0 for x in range(int(size))] for y in range(int(size))]
    player_color = color
    return player_evaluation()


def player_evaluation():
    white_eval = 0
    black_eval = 0
    for row in range(int(size)):  # we will search for each empty square
        for col in range(int(size)):
            if state[row][col] == EMPTY_SPACE:  # founded empty square
                nearest_queen(row, col)
    print("Finish search")
    # now we will check in the minimum distances matrices which player got each square first
    for row in range(int(size)):
        for col in range(int(size)):
            if enemy_board[row][col] < player_board[row][col]:
                black_eval += 1
            if player_board[row][col] < enemy_board[row][col]:
                white_eval += 1
    if player_color == "WHITE":
        return (0.3 * white_mobility + 0.7 * white_eval) - (0.3 * black_mobility + 0.7 * black_eval)
    else:
        return (0.3 * black_mobility + 0.7 * black_eval) - (0.3 * white_mobility + 0.7 * white_eval)


def nearest_queen(row, col):
    global white_mobility
    global black_mobility

    turn = 0
    queen_found = False
    checked_matrix = [[0 for x in range(int(size))] for y in range(int(size))]  # for not visiting same square twice
    checked_matrix[row][col] = 1
    square_moves = deque([])  # make queue
    square_moves = add_square_moves(square_moves, row, col, checked_matrix)
    # finding all the the legal moves from this square

    while queen_found is False:
        turn += 1
        temp_queue = deque([])
        if len(square_moves) == 0:  # the square is blocked
            queen_found = True
            return
        while len(square_moves) != 0:
            move = square_moves[0]
            square_moves.popleft()
            if state[move[0]][move[1]] == BLACK_QUEEN:  # if we found a black queen in the square
                if turn == 1:  # checking for mobility in 1 move
                    black_mobility += 1
                if enemy_board[row][col] > turn:
                    enemy_board[row][col] = turn  # TODO Daniel what this part does? should be = and not == ?
            if state[move[0]][move[1]] == WHITE_QUEEN:  # if we found a white queen in the square
                if turn == 1:  # checking for mobility in 1 move
                    white_mobility += 1
                if player_board[row][col] > turn:
                    player_board[row][col] = turn  # TODO Daniel what this part does? should be = and not == ?
            if len(square_moves) == 1 and (player_board[row][col] != 0 or player_board[row][col] != 0):
                queen_found = True
                square_moves.clear()
                break
            if player_board[row][col] != 0 and player_board[row][col] != 0:
                queen_found = True
                square_moves.clear()
                break
            if state[move[0]][move[1]] == EMPTY_SPACE:  # if its empty we will search from him
                temp_queue = add_square_moves(temp_queue, move[0], move[1], checked_matrix)
        square_moves = deepcopy(temp_queue)
        temp_queue.clear()


def add_square_moves(queen_moves, current_row, current_column, checked_matrix):
    i = 1
    while current_column - i >= 0:
        if checked_matrix[current_row][(current_column - i)] == 0:
            queen_moves.append([current_row, current_column - i])
        if not IsMoveLegal([current_row, current_column], [current_row, current_column - i], size, state):
            break
        i += 1

    i = 1
    while current_column + i <= 9:
        if checked_matrix[current_row][current_column + i] == 0:
            queen_moves.append([current_row, current_column + i])
        if not IsMoveLegal([current_row, current_column], [current_row, current_column + i], size, state):
            break
        i += 1

    i = 1
    while current_row - i >= 0:
        if checked_matrix[current_row - i][current_column] == 0:
            queen_moves.append([current_row - i, current_column])
        if not IsMoveLegal([current_row, current_column], [current_row - i, current_column], size, state):
            break
        i += 1

    i = 1
    while current_row + i <= 9:
        if checked_matrix[current_row + i][current_column] == 0:
            queen_moves.append([current_row + i, current_column])
        if not IsMoveLegal([current_row, current_column], [current_row + i, current_column], size, state):
            break
        i += 1

    i = 1
    while current_column - i >= 0 and current_row - i >= 0:
        if checked_matrix[current_row - i][current_column - i] == 0:
            queen_moves.append([current_row - i, current_column - i])
        if not IsMoveLegal([current_row, current_column], [current_row - i, current_column - i], size, state):
            break
        i += 1

    i = 1
    while current_column - i >= 1 and current_row + i <= 9:
        if checked_matrix[current_row + i][(current_column - i)] == 0:
            queen_moves.append([current_row + i, current_column - i])
        if not IsMoveLegal([current_row, current_column], [current_row + i, current_column - i], size, state):
            break
        i += 1

    i = 1
    while current_column + i <= 9 and current_row - i >= 0:
        if checked_matrix[current_row - i][(current_column + i)] == 0:
            queen_moves.append([current_row - i, current_column + i])
        if not IsMoveLegal([current_row, current_column], [current_row - i, current_column + i], size, state):
            break
        i += 1

    i = 1
    while current_column + i <= 9 and current_row + i <= 9:
        if checked_matrix[current_row + i][current_column + i] == 0:
            queen_moves.append([current_row + i, current_column + i])
        if not IsMoveLegal([current_row, current_column], [current_row + i, current_column + i], size, state):
            break
        i += 1

    return queen_moves


class TerriMobEval:
    def __init__(self, board_state, board_size):
        self.state = board_state
        self.white_board = [[0 for x in range(board_size)] for y in range(board_size)]
        self.black_board = [[0 for x in range(board_size)] for y in range(board_size)]
        self.board = board_state
        self.size = board_size
        self.white_mobility = 0
        self.black_mobility = 0

    def player_evaluation(self):
        white_eval = 0
        black_eval = 0
        for row in range(int(self.size)):  # we will search for each empty square
            for col in range(int(self.size)):
                if self.board[row][col] == EMPTY_SPACE:  # founded empty square
                    self.nearest_queen(row, col)
        print("Finish search")
        # now we will check in the minimum distances matrices which player got each square first
        for row in range(int(self.size)):
            for col in range(int(self.size)):
                if self.black_board[row][col] < self.white_board[row][col]:
                    black_eval += 1
                if self.white_board[row][col] < self.black_board[row][col]:
                    white_eval += 1
        q = self.state.get_turn_queens()
        if q[0].GetColor() == "WHITE":
            return (0.3 * self.white_mobility + 0.7 * white_eval) - (0.3 * self.black_mobility + 0.7 * black_eval)
        else:
            return (0.3 * self.black_mobility + 0.7 * black_eval) - (0.3 * self.white_mobility + 0.7 * white_eval)

    def nearest_queen(self, row, col):
        turn = 0
        queen_found = False
        checked_matrix = [[0 for x in range(self.size)] for y in range(self.size)]  # for not visiting same square twice
        checked_matrix[row][col] = 1
        square_moves = deque([])  # make queue
        square_moves = self.add_square_moves(square_moves, row, col,
                                             checked_matrix)  # finding all the the legal moves from this square
        while queen_found is False:
            turn += 1
            temp_queue = deque([])
            if len(square_moves) == 0:  # the square is blocked
                queen_found = True
                return
            while len(square_moves) != 0:
                move = square_moves[0]
                square_moves.popleft()
                if self.board[move[0]][move[1]] == BLACK_QUEEN:  # if we found a black queen in the square
                    if turn == 1:  # checking for mobility in 1 move
                        self.black_mobility += 1
                    if self.black_board[row][col] > turn:
                        self.black_board[row][col] == turn
                if self.board[move[0]][move[1]] == WHITE_QUEEN:  # if we found a white queen in the square
                    if turn == 1:  # checking for mobility in 1 move
                        self.white_mobility += 1
                    if self.white_board[row][col] > turn:
                        self.white_board[row][col] == turn
                if len(square_moves) == 1 and (self.white_board[row][col] != 0 or self.white_board[row][col] != 0):
                    queen_found = True
                    square_moves.clear()
                    break
                if self.white_board[row][col] != 0 and self.white_board[row][col] != 0:
                    queen_found = True
                    square_moves.clear()
                    break
                if self.board[move[0]][move[1]] == EMPTY_SPACE:  # if its empty we will search from him
                    temp_queue = self.add_square_moves(temp_queue, move[0], move[1], checked_matrix)
            square_moves = temp_queue
            temp_queue.clear()

    def add_square_moves(self, queen_moves, current_row, current_column, checked_matrix):
        i = 1
        while current_column - i >= 0:
            if checked_matrix[current_row][(current_column - i)] == 0:
                queen_moves.append([current_row, current_column - i])
            if not IsMoveLegal([current_row, current_column], [current_row, current_column - i], self.size, self.board):
                break
            i += 1

        i = 1
        while current_column + i <= 9:
            if checked_matrix[current_row][current_column + i] == 0:
                queen_moves.append([current_row, current_column + i])
            if not IsMoveLegal([current_row, current_column], [current_row, current_column + i], self.size, self.board):
                break
            i += 1

        i = 1
        while current_row - i >= 0:
            if checked_matrix[current_row - i][current_column] == 0:
                queen_moves.append([current_row - i, current_column])
            if not IsMoveLegal([current_row, current_column], [current_row - i, current_column], self.size, self.board):
                break
            i += 1

        i = 1
        while current_row + i <= 9:
            if checked_matrix[current_row + i][current_column] == 0:
                queen_moves.append([current_row + i, current_column])
            if not IsMoveLegal([current_row, current_column], [current_row + i, current_column], self.size, self.board):
                break
            i += 1

        i = 1
        while current_column - i >= 0 and current_row - i >= 0:
            if checked_matrix[current_row - i][current_column - i] == 0:
                queen_moves.append([current_row - i, current_column - i])
            if not IsMoveLegal([current_row, current_column], [current_row - i, current_column - i], self.size,
                               self.board):
                break
            i += 1

        i = 1
        while current_column - i >= 1 and current_row + i <= 9:
            if checked_matrix[current_row + i][(current_column - i)] == 0:
                queen_moves.append([current_row + i, current_column - i])
            if not IsMoveLegal([current_row, current_column], [current_row + i, current_column - i], self.size,
                               self.board):
                break
            i += 1

        i = 1
        while current_column + i <= 9 and current_row - i >= 0:
            if checked_matrix[current_row - i][(current_column + i)] == 0:
                queen_moves.append([current_row - i, current_column + i])
            if not IsMoveLegal([current_row, current_column], [current_row - i, current_column + i], self.size,
                               self.board):
                break
            i += 1

        i = 1
        while current_column + i <= 9 and current_row + i <= 9:
            if checked_matrix[current_row + i][current_column + i] == 0:
                queen_moves.append([current_row + i, current_column + i])
            if not IsMoveLegal([current_row, current_column], [current_row + i, current_column + i], self.size,
                               self.board):
                break
            i += 1

        return queen_moves
