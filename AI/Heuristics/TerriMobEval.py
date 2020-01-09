
# Creating the evaluation function
# The evaluation function will find which player can get first to each tile
# In addition we will keep the moves that we can get by 1 step
# -- we will create 2 new matrices that in each position will be the minimum number of step
# -- that require to get there for each player

from Game_Enginge.Constants import EMPTY_SPACE, BLACK_QUEEN, WHITE_QUEEN
from collections import deque
from Game_Enginge.Rules import is_move_legal
from copy import deepcopy


class TerriMobEval:
    def __init__(self, board_state, board_size, player_color):
        self.white_board = [[0 for x in range(int(board_size))] for y in range(int(board_size))]
        self.black_board = [[0 for x in range(int(board_size))] for y in range(int(board_size))]
        self.board = board_state
        self.color = player_color
        self.size = board_size
        self.white_mob = 0
        self.black_mob = 0
        self.possible_move_list = []
        for row in range(int(board_size)):
            for col in range(int(board_size)):
                self.possible_move_list.append([row, col])

    def playerEval(self):
        white_eval = 0
        black_eval = 0
        for row in range(1, int(self.size)):  # we will search for each empty square
            for col in range(1, int(self.size)):
                if self.board[row][col] == EMPTY_SPACE:  # founded empty square
                    self.nearestQueen(row, col)
        # now we will check in the minimum distances matrices which player got each square first
        for row in range(int(self.size)):
            for col in range(int(self.size)):
                if self.black_board[row][col] < self.white_board[row][col]:
                    black_eval += 1
                if self.white_board[row][col] < self.black_board[row][col]:
                    white_eval += 1
        if self.color == "WHITE":
            return white_eval - black_eval, self.white_mob - self.black_mob
        else:
            return black_eval - white_eval, self.black_mob - self.white_mob

    def nearestQueen(self, row, col):
        self.possible_move_list.remove([row, col])
        move_list = deepcopy(self.possible_move_list)
        temp_squares = []
        turn = 0
        temp_queue = deque([])
        black_found = False
        white_found = False
        queen_found = False
        square_moves = deque([])  # make queue
        square_moves.extend(
            self.addSquareMoves(row, col, move_list, 1000))  # finding all the the legal moves from this square
        while queen_found is False:
            turn += 1
            while len(square_moves) != 0:
                move = square_moves.popleft()
                # if we found a black queen in the square
                if self.board[move[0]][move[1]] == BLACK_QUEEN:
                    black_found = True
                    if turn == 1:  # checking for mobility in 1 move
                        self.black_mob += 1
                    if self.black_board[row][col] > turn or self.black_board[row][col] == 0:
                        self.black_board[row][col] = turn
                # if we found a white queen in the square
                if self.board[move[0]][move[1]] == WHITE_QUEEN:
                    white_found = True
                    if turn == 1:  # checking for mobility in 1 move
                        self.white_mob += 1
                    if self.white_board[row][col] > turn or self.white_board[row][col] == 0:
                        self.white_board[row][col] = turn
                # black spot - we do not need to keep searching for white queen
                if len(square_moves) == 0 and black_found and not white_found:
                    queen_found = True
                    if self.white_board[row][col] == 0:  # if we did not find any queen yet for white board
                        self.white_board[row][col] = turn + 1
                    square_moves.clear()
                    temp_queue.clear()
                    break
                # white spot - we do not need to keep searching for black queen
                if len(square_moves) == 0 and white_found and not black_found:
                    queen_found = True
                    if self.black_board[row][col] == 0:  # if we did not find any queen yet
                        self.black_board[row][col] = turn + 1
                    square_moves.clear()
                    temp_queue.clear()
                    break
                # if we founded both queens
                if white_found and black_found:
                    queen_found = True
                    square_moves.clear()
                    temp_queue.clear()
                    break
                temp_squares.append(move)
            if queen_found is False:
                for square in temp_squares:
                    # if its empty we will search from him
                    if self.board[square[0]][square[1]] == EMPTY_SPACE:
                        temp_queue.extend(self.addSquareMoves(square[0], square[1], move_list, turn))
            temp_squares.clear()
            square_moves = deepcopy(temp_queue)
            temp_queue.clear()
            if len(square_moves) == 0:
                queen_found = True
                break

    def addSquareMoves(self, curRow, curCol, move_list, turn):
        moves = []
        for square in move_list:
            if turn < self.black_board[curRow][curCol] or turn < self.white_board[curRow][curCol] \
                    or self.black_board[curRow][curCol] == 0 or self.white_board[curRow][curCol] == 0:
                if is_move_legal(square, [curRow, curCol], self.size, self.board):
                    moves.append(square)
                    move_list.remove(square)  # remove square from the possible move list
            else:
                move_list.remove(square)
        return moves
