import random
from Rules import IsMoveLegal
from Constants import EMPTY_SPACE, WHITE_QUEEN, BLACK_QUEEN, ARROW_SPACE
from copy import deepcopy
from LiranAITest.ZorbistHashing import compute_hash, hash_table

MIN = -1000
MAX = 1000
board_state = []
board_size = 0
players = []
current_depth = 0
move_list = []
son_to_save = None
turn_count = 0
pruning_count = 0

# What our Hash table need to hold
# value, Move, How deep we looked, father/son, current turn(How much deep we looked from the start of the game), player


def clear_hash():
    for key in list(hash_table):
        data = hash_table[key]
        if data[3] < turn_count:
            hash_table.pop(key)


def evaluate():
    return random.randint(-1200, 1200)


def find_legal_moves(queens, is_arrow, color, arrow_start_position=None):
    global current_queen

    for queen in queens:
        if is_arrow:
            px, py = arrow_start_position
        else:
            current_queen = queen.GetPosition()
            px, py = current_queen
        for step in range(1, int(board_size)):
            # Check move up
            if IsMoveLegal([px, py], [px - step, py], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px - step, py])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px - step, py]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px - step, py]])
            # Check move down
            if IsMoveLegal([px, py], [px + step, py], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px + step, py])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px + step, py]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px + step, py]])
            # Check right move
            if IsMoveLegal([px, py], [px, py + step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px, py + step])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px, py + step]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px, py + step]])
            # Check left move
            if IsMoveLegal([px, py], [px, py - step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px, py - step])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px, py - step]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px, py - step]])
            # Check up-left diagonal
            if IsMoveLegal([px, py], [px - step, py - step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px - step, py - step])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px - step, py - step]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px - step, py - step]])
            # Check down-right diagonal
            if IsMoveLegal([px, py], [px + step, py + step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px + step, py + step])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px + step, py + step]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px + step, py + step]])
            # Check up-right diagonal
            if IsMoveLegal([px, py], [px - step, py + step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px - step, py + step])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px - step, py + step]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px - step, py + step]])
            # Check down-left diagonal
            if IsMoveLegal([px, py], [px + step, py - step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, [px + step, py - step])
                    board_state[px][py] = color
                else:
                    if [current_queen, arrow_start_position, [px + step, py - step]] not in move_list:
                        move_list.append([current_queen, arrow_start_position, [px + step, py - step]])
    return move_list


def update_move_to_board(move, queens, color):
    global board_state
    global current_depth

    old_queen, new_queen, arrow = move
    # need to update the queen list
    for queen in queens:
        if old_queen == queen.GetPosition():
            break

    queen.SetNewPosition(new_queen)
    board_state[old_queen[0]][old_queen[1]] = EMPTY_SPACE
    board_state[new_queen[0]][new_queen[1]] = color
    board_state[arrow[0]][arrow[1]] = ARROW_SPACE
    current_depth += 1


def undo_move_to_board(move, player):
    global current_depth

    new_queen, old_queen, arrow = move
    update_move_to_board([new_queen, old_queen, arrow], player[0], player[3])
    board_state[arrow[0]][arrow[1]] = EMPTY_SPACE
    current_depth -= 2


# This way our hash table will hold the value of the state_board, his son which is the best move from it and the move
# from his father that made this state
# No need to add the depth, we can find the sate in O(1) each time and then access his son to add his move to the start
# of the list, this way we will always check the best moves in this direction
# Next step we need to do is find how we can clean the move_table from data of illegal moves, or maybe not? is this
# table holds a huge amount of data? not really, the amount of cells in the table is huge but the values hold small data
def add_to_zobrist_hash_table(key, value, move, depth, son_key, player_color):

    if key not in hash_table:
        hash_table[key] = [value, move, depth, depth + turn_count, son_key, player_color]
    else:
        # Checking if the data is new
        data = hash_table[key]
        new_data = [value, move, depth, depth + turn_count, son_key, player_color]
        # if new we update the data
        if data != new_data:
            if data[0] < new_data[0]:
                temp = [value, data[1], data[2], data[3], data[4], data[5]]
                update_this = {key: temp}
                hash_table.update(update_this)


def temp_func(value, move):

    if value not in hash_table:
        hash_table[value] = move

    else:
        tmp = {value: move}
        hash_table.update(tmp)


def sevaluate():
    return random.randint(1001, 1200)


def sort_moves(moves_to_sort, player):
    max_move = []
    for i in range(6):
        max_value = -100000
        for move in moves_to_sort:
            update_move_to_board(move, player[0], player[3])
            value = sevaluate()
            if max_value < value:
                max_value = value
                max_move = move
            undo_move_to_board(move, player)
        moves_to_sort.remove(max_move)
        moves_to_sort.insert(i, max_move)


def alpha_beta(depth, alpha, beta):
    global current_depth
    global son_to_save
    global pruning_count

    best_value = 0
    move_count = 0
    # 1st stopping condition for the alpha_beta (Since we are not looking to the end for now this is efficient)
    # Will need to add a stopping condition where we are having the queens isolated
    current_player = players[current_depth % 2]
    moves = deepcopy(find_legal_moves(current_player[0], False, current_player[3]))
    print("Number of moves in list: {0}".format(len(moves)))
    move_list.clear()
    best_value_min = MIN
    best_value_max = MAX
    if (depth == 0) or (len(moves) == 0):
        son_to_save = None
        return evaluate()
    sort_moves(moves, current_player)
    for move in moves:
        move_count += 1
        update_move_to_board(move, current_player[0], current_player[3])
        value = -alpha_beta(depth - 1, -beta, -alpha)
        key = compute_hash(board_state)
        add_to_zobrist_hash_table(key, value, move, current_depth, son_to_save, current_player[2])
        undo_move_to_board(move, current_player)
        if current_player[1]:
            if best_value_min < value:
                son_to_save = key
                best_value = best_value_min = value
            alpha = max(alpha, best_value_min)
            if alpha >= beta:

                print("Moves done: {0}\n Moves Found {1}\n Moves pruned: {2}\n".format(move_count, len(moves),
                                                                                       len(moves) - move_count))
                pruning_count += 1
                break
        else:
            if best_value_max > value:
                son_to_save = key
                best_value = best_value_max = value
            beta = min(beta, best_value_max)
            if beta <= alpha:

                print("Moves done: {0}\n Moves Found {1}\n Moves pruned: {2}\n".format(move_count, len(moves),
                                                                                       len(moves) - move_count))
                pruning_count += 1

                break
    return best_value


def start_alpha_beta(starting_board_matrix, depth, size, player_queens, enemy_q, turn_number):
    global board_state
    global board_size
    global players
    global current_depth
    global turn_count
    global pruning_count

    pruning_count = 0
    move = 0
    # Setting values
    turn_count = turn_number
    board_size = size
    board_state = starting_board_matrix

    # Getting the players data
    max_player = [player_queens, True, player_queens[0].GetColor()]
    min_player = [enemy_q, False, enemy_q[0].GetColor()]
    if max_player[2].upper() == "WHITE":
        max_player.append(WHITE_QUEEN)
        min_player.append(BLACK_QUEEN)
    else:
        max_player.append(BLACK_QUEEN)
        min_player.append(WHITE_QUEEN)
    players = [max_player, min_player]

    # Reset our current depth to 0
    current_depth = 0
    # Freeing memory from old moves in hash table
    clear_hash()
    val = alpha_beta(depth, MIN, MAX)
    print("Number of pruning_count: {0}".format(pruning_count))
    # Searching for the value in our hash table.
    for key in hash_table:
        data = hash_table[key]
        # {value, move, depth, depth + turn_count, father_son, player_color}
        if data[0] == val and data[3] == turn_count+1 and data[5] == max_player[2]:
            move = data[1]
            # print(key)
            break
    if move == 0:
        raise Exception("Didn't find a viable move")

    return val, move

# TODO The bug that happens is that we never make a cell for the starting board state, therefore he never get a son_key
# TODO causing all the problem in our loop, in this loop we must have at least 2 consitions to be able to find the right
# TODO state that we want, if our random range was bigger it was no problem maybe we can do it by telling who player
