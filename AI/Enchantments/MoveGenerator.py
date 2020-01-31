# Creating a list of all the possible moves we can make in the following way queen_to_move - where_to_move - arrow_pos

from Game_Enginge.Constants import WHITE_QUEEN, BLACK_QUEEN, EMPTY_SPACE
import random

"""move_generator

player_queens: a list of the queens of the active player
board_state: how the board looks
board_size: the size of the board (10/6)

Checking for each queens all the possible positions that it can move in any direction, stopping checking in any
direction if something blocking the way
"""
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
            if board_state[px - i][py] == EMPTY_SPACE:
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
            if board_state[px + i][py] == EMPTY_SPACE:
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
            if board_state[px][py + i] == EMPTY_SPACE:
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
            if board_state[px][py - i] == EMPTY_SPACE:
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
            if board_state[px - i][py - i] == EMPTY_SPACE:
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
            if board_state[px - i][py + i] == EMPTY_SPACE:
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
            if board_state[px + i][py - i] == EMPTY_SPACE:
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
            if board_state[px + i][py + i] == EMPTY_SPACE:
                board_state[queen_position[0]][queen_position[1]] = EMPTY_SPACE
                arrows = arrow_move_generator([px + i, py + i], board_state, board_size)
                board_state[queen_position[0]][queen_position[1]] = color
                for arrow in arrows:
                    move_list.append([queen_position, [px + i, py + i], arrow])
                i += 1
            else:
                break
    random.shuffle(move_list)  # Avoiding any certain moves done by how we checked the queens
    return move_list


"""arrow_move_generator
The function is called from the move_generator with the possible position we found 
starting_position: a new possible position for a queen
board_state: How the board looks
board_size: the size of the board

The code below is similar to the move_generator, an attempt for a recursive function was made but for unknown reason 
we got 4 times the possible moves(duplicates) and a check for each move if we already checked it made a the time of 
finding a move was a lot longer then making a code duplication 
"""
def arrow_move_generator(starting_position, board_state, board_size):
    arrow_list = []
    px, py = starting_position
    size = int(board_size)
    i = 1
    # check movement up:
    while 0 <= px - i:
        if board_state[px - i][py] == EMPTY_SPACE:
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
