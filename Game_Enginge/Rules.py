from Game_Enginge.Constants import EMPTY_SPACE


def check_straight_moves(bigger, smaller, constant, direction, board_matrix):
    delta = bigger - smaller
    symbol = ""
    for i in range(delta):
        if i == 0:
            continue
        if direction == "Down":
            symbol = board_matrix[smaller + i][constant]
        elif direction == "Up":
            symbol = board_matrix[bigger - i][constant]
        elif direction == "Right":
            symbol = board_matrix[constant][smaller + i]
        elif direction == "Left":
            symbol = board_matrix[constant][bigger - i]
        if symbol != EMPTY_SPACE:
          #  print("We got {0} in the way".format(symbol))
            return False
    # print("Move accepted")
    return True


def check_diagonal_movements(current_position_x, current_position_y, delta, direction, board_matrix):
    symbol = ""
    for i in range(delta):
        if i == 0:
            continue
        elif direction == "Up-Left":
            symbol = board_matrix[current_position_x - i][current_position_y - i]
        elif direction == "Down-Right":
            symbol = board_matrix[current_position_x + i][current_position_y + i]
        elif direction == "Up-Right":
            symbol = board_matrix[current_position_x - i][current_position_y + i]
        elif direction == "Down-Left":
            symbol = board_matrix[current_position_x + i][current_position_y - i]
        if symbol != EMPTY_SPACE:
      #      print("We got {0} in the way".format(symbol))
            return False
    # print("Move accepted")
    return True


def is_move_legal(current_position, new_position, board_size, board_matrix):

    # Check if new position is in the board
    if (
        new_position[0] > int(board_size) - 1
        or new_position[0] < 0
        or new_position[1] > int(board_size) - 1
        or new_position[1] < 0
    ):
      #  print("Please choose a position in the board")
        return False

    # Check if the new position is free (Also includes the check that the queen is not moving in place)
    if board_matrix[new_position[0]][new_position[1]] != EMPTY_SPACE:
     #   print("Please enter a valid position for the queen")
        return False
    # Check that we are not trying to stay in place
    if current_position == new_position:
        return False
    # Check if the move is possible by this queen (Moving like a queen not a horse)
    current_position_x, current_position_y = current_position
    new_position_x, new_position_y = new_position
    # Check Up and Down (moving on the letters)
    if current_position_y == new_position_y and current_position_x != new_position_x:
        # Going down
        if new_position_x > current_position_x:
            return check_straight_moves(new_position_x, current_position_x, current_position_y, "Down", board_matrix)

        # Going up
        else:
            return check_straight_moves(current_position_x, new_position_x, current_position_y, "Up", board_matrix)

    # Check Left or Right (moving on the numbers)
    if current_position_x == new_position_x and current_position_y != new_position_y:
        # Going right
        if new_position_y > current_position_y:
            return check_straight_moves(new_position_y, current_position_y, current_position_x, "Right", board_matrix)

        # Going left
        else:
            return check_straight_moves(current_position_y, new_position_y, current_position_x, "Left", board_matrix)

    # Check diagonals (We got four diagonals to check [up-left, up-right, down-left, down-right]
    delta_x = current_position_x - new_position_x
    delta_y = current_position_y - new_position_y
    if abs(delta_x) != abs(delta_y):
      #  print("You can only move like a queen")
        return False

    # Up-Left
    if delta_x == delta_y > 0:
        return check_diagonal_movements(current_position_x, current_position_y, delta_x, "Up-Left", board_matrix)

    # Down-Right
    elif delta_x == delta_y < 0:
        return check_diagonal_movements(current_position_x, current_position_y, delta_y, "Down-Right", board_matrix)

    else:
        # Up-Right
        if delta_x > 0:
            return check_diagonal_movements(current_position_x, current_position_y, delta_x, "Up-Right", board_matrix)
        # Down-Left
        if delta_y > 0:
            return check_diagonal_movements(current_position_x, current_position_y, delta_y, "Down-Left", board_matrix)
