from AI.Enchantments.MoveGenerator import move_generator
from Game_Enginge.Constants import EMPTY_SPACE, ARROW_SPACE, WHITE_QUEEN, BLACK_QUEEN
import random


class GameRules:
    def __init__(self, board_size):
        self.num_players = 2
        self.board_size = board_size

    def num_players(self):
        return 2

    def get_actions(self, state):
        queens = state[1]
        board_state = state[0]
        return move_generator(queens, board_state, self.board_size)

    def get_current_player_id(self, state):
        if state[3].upper() == "WHITE":
            return 0
        else:
            return 1

    def is_terminal(self, state):
        board = state[0]
        queens = state[1]
        for queen in queens:
            (row, col) = queen.get_position()
            if row + 1 < 10:
                if board[row + 1][col] != EMPTY_SPACE:
                    return False
            else:
                return False
            if col + 1 < 10:
                if board[row][col + 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row - 1 > 0:
                if board[row - 1][col] != EMPTY_SPACE:
                    return False
            else:
                return False
            if col - 1 > 0:
                if board[row][col - 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row + 1 < 10 and col + 1 < 10:
                if board[row + 1][col + 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row + 1 < 10 and col - 1 > 0:
                if board[row + 1][col - 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row - 1 > 0 and col - 1 > 0:
                if board[row - 1][col - 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row - 1 > 0 and col + 1 < 10:
                if board[row - 1][col + 1] != EMPTY_SPACE:
                    return False
            else:
                return False
        return True

    def perform_action(self, action, state):
        #move = numpy.
        old_queen, new_queen, arrow = action
        queens = state[1]
        if queens[0].get_color().upper() == "WHITE":
            color = WHITE_QUEEN
            player = "white"
        else:
            color = BLACK_QUEEN
            player = "black"
        board_state = state[0]
        for queen in queens:
            if old_queen == queen.get_position():
                queen.set_new_position(new_queen)
                board_state[old_queen[0]][old_queen[1]] = EMPTY_SPACE
                board_state[new_queen[0]][new_queen[1]] = color
                board_state[arrow[0]][arrow[1]] = ARROW_SPACE
                break
        newstate = [board_state, queens, state[2], player]
        return newstate


def reward(self, state):
    return random.randint(0, 1)
