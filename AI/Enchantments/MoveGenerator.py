from Game_Enginge.Constants import WHITE_QUEEN, BLACK_QUEEN, EMPTY_SPACE
import random


def move_generator(player_queens, board_state, board_size):
    move_list = []
    size = int(board_size)
    if player_queens[0].get_color().upper() == "WHITE":
        color = WHITE_QUEEN
    else:
        color = BLACK_QUEEN
    for queen in player_queens:
        queen_position = queen.get_position()
        px, py = queen_position
        i = 1
        # check movement up:
        while 0 <= px - i:
            if board_state[px - i][py] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px - i, py], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px - i, py], arrow])
                i += 1
            else:
                break
        i = 1
        # check movement down:
        while px + i < size:
            if board_state[px + i][py] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px + i, py], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px + i, py], arrow])
                i += 1
            else:
                break
        i = 1
        # check movement right:
        while py + i < size:
            if board_state[px][py + i] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px, py + i], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px, py + i], arrow])
                i += 1
            else:
                break
        i = 1
        # check movement left:
        while 0 <= py - i:
            if board_state[px][py - i] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px, py - i], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px, py - i], arrow])
                i += 1
            else:
                break
        i = 1
        # check movement up-left:
        while 0 <= px - i and 0 <= py - i:
            if board_state[px - i][py - i] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator(([px - i, py - i]), board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px - i, py - i], arrow])
                i += 1
            else:
                break
        i = 1
        # check movement up-right:
        while 0 <= px - i and py + i < size:
            if board_state[px - i][py + i] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px - i, py + i], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px - i, py + i], arrow])
                i += 1
            else:
                break
        i = 1
        # check movement down-left:
        while px + i < size and 0 <= py - i:
            if board_state[px + i][py - i] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px + i, py - i], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px + i, py - i], arrow])
                i += 1
            else:
                break
        i = 1
        # check movement down-right:
        while px + i < size and py + i < size:
            if board_state[px + i][py + i] == EMPTY_SPACE:  # TODO not checking by is move legal
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px + i, py + i], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px + i, py + i], arrow])
                i += 1
            else:
                break
    random.shuffle(move_list)  # TODO shuffle the move list
    return move_list


def arrow_move_generator(starting_position, board_state, board_size):
    arrow_list = []
    px, py = starting_position
    size = int(board_size)
    i = 1
    # check movement up:
    while 0 <= px - i:
        if board_state[px - i][py] == EMPTY_SPACE:  # TODO not checking by is move legal (same for all arrows)
            arrow_list.append([px - i, py])
            i += 1
        else:
            break
    i = 1
    # check movement down:
    while px + i < size:
        if board_state[px + i][py] == EMPTY_SPACE:
            arrow_list.append([px + i, py])
            i += 1
        else:
            break
    i = 1
    # check movement right:
    while py + i < size:
        if board_state[px][py + i] == EMPTY_SPACE:
            arrow_list.append([px, py + i])
            i += 1
        else:
            break
    i = 1
    # check movement left:
    while 0 <= py - i:
        if board_state[px][py - i] == EMPTY_SPACE:
            arrow_list.append([px, py - i])
            i += 1
        else:
            break
    i = 1
    # check movement up-left:
    while 0 <= px - i and 0 <= py - i:
        if board_state[px - i][py - i] == EMPTY_SPACE:
            arrow_list.append([px - i, py - i])
            i += 1
        else:
            break
    i = 1
    # check movement up-right:
    while 0 <= px - i and py + i < size:
        if board_state[px - i][py + i] == EMPTY_SPACE:
            arrow_list.append([px - i, py + i])
            i += 1
        else:
            break
    i = 1
    # check movement down-left:
    while px + i < size and 0 <= py - i:
        if board_state[px + i][py - i] == EMPTY_SPACE:
            arrow_list.append([px + i, py - i])
            i += 1
        else:
            break
    i = 1
    # check movement down-right:
    while px + i < size and py + i < size:
        if board_state[px + i][py + i] == EMPTY_SPACE:
            arrow_list.append([px + i, py + i])
            i += 1
        else:
            break
    return arrow_list
