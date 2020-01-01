# Creating the evaluation function
# The evaluation function will find which player can get first to each tile
# In addition we will keep the moves that we can get by 1 step
# -- we will create 2 new matrices that in each position will be the minimum number of step
# -- that require to get there for each player

from Constants import EMPTY_SPACE, BLACK_QUEEN, WHITE_QUEEN
from collections import deque
from Rules import IsMoveLegal


class TerriMobEval:
    def __init__(self, _state):
        self.state = _state
        self.white_board = [[0 for x in range(10)] for y in range(10)]
        self.black_board = [[0 for x in range(10)] for y in range(10)]
        self.board = _state.board_matrix
        self.size = _state.board_size
        self.white_mob = 0
        self.black_mob = 0

    def playerEval(self):
        white_eval = 0
        black_eval = 0
        for row in range(int(self.size)):  # we will search for each empty square
            for col in range(int(self.size)):
                if self.board[row][col] == EMPTY_SPACE:  # founded empty square
                    self.nearestQueen(row, col)
        print("Finish search")
        # now we will check in the minimum distances matrices which player got eache square first
        for row in range(int(self.size)):
            for col in range(int(self.size)):
                if self.black_board[row][col] < self.white_board[row][col]:
                    black_eval += 1
                if self.white_board[row][col] < self.black_board[row][col]:
                    white_eval += 1
        q = self.state.get_turn_queens()
        if q[0].GetColor() == "WHITE":
            return (0.3*self.white_mob+0.7*white_eval)-(0.3*self.black_mob+0.7*black_eval)
        else:
            return (0.3*self.black_mob+0.7*black_eval)-(0.3*self.white_mob+0.7*white_eval)

    def nearestQueen(self, row, col):
        turn = 0
        queen_found = False
        checked_matrix = [[0 for x in range(10)] for y in range(10)]  # for not visiting same square twice
        checked_matrix[row][col] = 1
        square_moves = deque([])  # make queue
        square_moves = self.addSquareMoves(square_moves, row, col,
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
                        self.black_mob += 1
                    if self.black_board[row][col] > turn:
                        self.black_board[row][col] == turn
                if self.board[move[0]][move[1]] == WHITE_QUEEN:  # if we found a white queen in the square
                    if turn == 1:  # checking for mobility in 1 move
                        self.white_mob += 1
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
                    temp_queue = self.addSquareMoves(temp_queue, move[0], move[1], checked_matrix)
            square_moves = temp_queue
            temp_queue.clear()

    def addSquareMoves(self, queen_moves, curRrow, curCol, checked_matrix):
        i = 1
        while curCol - i >= 0:
            if checked_matrix[curRrow][(curCol - i)] == 0:
                queen_moves.append([curRrow, curCol - i])
            if not IsMoveLegal([curRrow, curCol], [curRrow, curCol - i], self.size, self.board):
                break
            i += 1

        i = 1
        while curCol + i <= 9:
            if checked_matrix[curRrow][curCol + i] == 0:
                queen_moves.append([curRrow, curCol + i])
            if not IsMoveLegal([curRrow, curCol], [curRrow, curCol + i], self.size, self.board):
                break
            i += 1

        i = 1
        while curRrow - i >= 0:
            if checked_matrix[curRrow - i][curCol] == 0:
                queen_moves.append([curRrow - i, curCol])
            if not IsMoveLegal([curRrow, curCol], [curRrow - i, curCol], self.size, self.board):
                break
            i += 1

        i = 1
        while curRrow + i <= 9:
            if checked_matrix[curRrow + i][curCol] == 0:
                queen_moves.append([curRrow + i, curCol])
            if not IsMoveLegal([curRrow, curCol], [curRrow + i, curCol], self.size, self.board):
                break
            i += 1

        i = 1
        while curCol - i >= 0 and curRrow - i >= 0:
            if checked_matrix[curRrow - i][curCol - i] == 0:
                queen_moves.append([curRrow - i, curCol - i])
            if not IsMoveLegal([curRrow, curCol], [curRrow - i, curCol - i], self.size, self.board):
                break
            i += 1

        i = 1
        while curCol - i >= 1 and curRrow + i <= 9:
            if checked_matrix[curRrow + i][(curCol - i)] == 0:
                queen_moves.append([curRrow + i, curCol - i])
            if not IsMoveLegal([curRrow, curCol], [curRrow + i, curCol - i], self.size, self.board):
                break
            i += 1

        i = 1
        while curCol + i <= 9 and curRrow - i >= 0:
            if checked_matrix[curRrow - i][(curCol + i)] == 0:
                queen_moves.append([curRrow - i, curCol + i])
            if not IsMoveLegal([curRrow, curCol], [curRrow - i, curCol + i], self.size, self.board):
                break
            i += 1

        i = 1
        while curCol + i <= 9 and curRrow + i <= 9:
            if checked_matrix[curRrow + i][curCol + i] == 0:
                queen_moves.append([curRrow + i, curCol + i])
            if not IsMoveLegal([curRrow, curCol], [curRrow + i, curCol + i], self.size, self.board):
                break
            i += 1

        return queen_moves

