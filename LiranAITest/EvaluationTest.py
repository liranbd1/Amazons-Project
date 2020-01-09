from Constants import EMPTY_SPACE
from Rules import IsMoveLegal
from copy import deepcopy

unchecked_squares = []
checked_squares = []
player_board = []
enemy_board = []
size = 0
state = []
unreachable_squares = []


def relative_territory_mobility(board_state, board_size, player_queens, enemy_queens):
    global unchecked_squares
    global player_board
    global enemy_board
    global size
    global state

    state = board_state
    size = int(board_size)
    player_territory_score = 0
    enemy_territory_score = 0
    # Finding all the empty spaces
    unchecked_squares = find_empty_spaces(state, size)

    # Settings the players boards
    player_board = [[0 for x in range(size)] for y in range(size)]
    enemy_board = [[0 for x in range(size)] for y in range(size)]

    player_queens_pos = []
    for queen in player_queens:
        player_queens_pos.append(queen.GetPosition())

    enemy_queens_pos = []
    for queen in enemy_queens:
        enemy_queens_pos.append(queen.GetPosition())

    territory(player_queens_pos, True)
    territory(enemy_queens_pos, False)

    for i in range(size):
        for j in range(size):
            if (player_board[i][j] - enemy_board[i][j]) > 0:
                enemy_territory_score += 1
            elif (player_board[i][j] - enemy_board[i][j]) < 0:
                player_territory_score += 1
    mobility_score = mobility_evaluation(state, size, player_queens, enemy_queens)
    unchecked_squares.clear()
    return 4 * (player_territory_score - enemy_territory_score) + mobility_score


def territory(list_to_check, is_player):
    global player_board
    unchecked_squares_temp = deepcopy(unchecked_squares)
    mobility_counter = 0
    temp_list = []
    space_to_compare_to = list_to_check
    counter = 0
    while len(unchecked_squares_temp) != 0:
        for unchecked_square in unchecked_squares_temp:
            for space in space_to_compare_to:
                if IsMoveLegal(space, unchecked_square, size, state):
                    if state[space[0]][space[1]] == EMPTY_SPACE:
                        if is_player:
                            player_board[unchecked_square[0]][unchecked_square[1]] = 1 + player_board[space[0]][space[1]]
                        else:
                            enemy_board[unchecked_square[0]][unchecked_square[1]] = 1 + enemy_board[space[0]][space[1]]
                    else:
                        if is_player:
                            player_board[unchecked_square[0]][unchecked_square[1]] = 1
                        else:
                            enemy_board[unchecked_square[0]][unchecked_square[1]] = 1
                        # mobility_counter += 1

                    temp_list.append(unchecked_square)
                    break

        space_to_compare_to = deepcopy(temp_list)
        unchecked_squares_temp = [x for x in unchecked_squares_temp if x not in temp_list]
        temp_list.clear()
        if len(space_to_compare_to) == 0:
            # unreachable_squares.append(deepcopy(unchecked_squares))
            break

    return mobility_counter


def find_empty_spaces(board_state, board_size):
    temp_list = []
    for i in range(int(board_size)):
        for j in range(int(board_size)):
            if board_state[i][j] == EMPTY_SPACE:
                temp_list.append([i, j])

    return temp_list


def mobility_evaluation(board_state, board_size, player_queens, enemy_queens):

    unchecked_squares_list = find_empty_spaces(board_state, board_size)
    p_score = 0
    e_score = 0
    for square in unchecked_squares_list:
        for p_queen in player_queens:
            if IsMoveLegal(p_queen.GetPosition(), square,  board_size, board_state):
                p_score += 1
                break
        for e_queen in enemy_queens:
            if IsMoveLegal(e_queen.GetPosition(), square,  board_size, board_state):
                e_score += 1
                break
    return p_score - e_score
