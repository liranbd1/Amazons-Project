"""Mobility evaluation heuristic - checking per player how fast can it get to any space on the board
fast: the number of turns it takes the player to get to the space
This heuristic alone will cause the queen to prefer going to center of the board, alone it is not strong causing an
easy capture by the enemy"""

from Game_Enginge.Constants import WHITE_QUEEN, BLACK_QUEEN, EMPTY_SPACE, ARROW_SPACE


def MobilityEvaluation(board_state, board_size, queens):
    mobility = 0
    size = int(board_size)
    for queen in queens:
        queen_position = queen.get_position()
        px, py = queen_position
        i = 1
        # check movement up:
        while 0 <= px - i:
            if board_state[px - i][py] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break
        i = 1
        # check movement down:
        while px + i < size:
            if board_state[px + i][py] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break
        i = 1
        # check movement right:
        while py + i < size:
            if board_state[px][py + i] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break
        i = 1
        # check movement left:
        while 0 <= py - i:
            if board_state[px][py - i] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break
        i = 1
        # check movement up-left:
        while 0 <= px - i and 0 <= py - i:
            if board_state[px - i][py - i] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break
        i = 1
        # check movement up-right:
        while 0 <= px - i and py + i < size:
            if board_state[px - i][py + i] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break
        i = 1
        # check movement down-left:
        while px + i < size and 0 <= py - i:
            if board_state[px + i][py - i] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break
        i = 1
        # check movement down-right:
        while px + i < size and py + i < size:
            if board_state[px + i][py + i] == EMPTY_SPACE:
                mobility += 1
                i += 1
            else:
                break

    return mobility
