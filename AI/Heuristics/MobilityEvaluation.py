from Game_Enginge.Constants import WHITE_QUEEN, BLACK_QUEEN, EMPTY_SPACE, ARROW_SPACE
from Game_Enginge.Rules import is_move_legal


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
