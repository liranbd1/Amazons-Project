import random
from Rules import IsMoveLegal
from Constants import EMPTY_SPACE, WHITE_QUEEN, BLACK_QUEEN, ARROW_SPACE
from copy import deepcopy
from LiranAITest.ZorbistHashing import compute_hash, zobrist_table

MIN = -1000
MAX = 1000
board_state = []
board_size = 0
players = []
current_depth = 0
move_list = []
hash_table = dict()
son_to_save = None


def evaluate():
    return random.randint(-10000, 10000)


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
                    find_legal_moves(queens, True, color, (px - step, py))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px - step, py)))
            # Check move down
            if IsMoveLegal([px, py], [px + step, py], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, (px + step, py))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px + step, py)))
            # Check right move
            if IsMoveLegal([px, py], [px, py + step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, (px, py + step))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px, py + step)))
            # Check left move
            if IsMoveLegal([px, py], [px, py - step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, (px, py - step))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px, py - step)))
            # Check up-left diagonal
            if IsMoveLegal([px, py], [px - step, py - step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, (px - step, py - step))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px - step, py - step)))
            # Check down-right diagonal
            if IsMoveLegal([px, py], [px + step, py + step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, (px + step, py + step))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px + step, py + step)))
            # Check up-right diagonal
            if IsMoveLegal([px, py], [px - step, py + step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, (px - step, py + step))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px - step, py + step)))
            # Check down-left diagonal
            if IsMoveLegal([px, py], [px + step, py - step], board_size, board_state):
                if not is_arrow:
                    board_state[px][py] = EMPTY_SPACE
                    find_legal_moves(queens, True, color, (px + step, py - step))
                    board_state[px][py] = color
                else:
                    move_list.append((current_queen, arrow_start_position, (px + step, py - step)))
    return move_list


def update_move_to_board(move, queens, color):
    global board_state

    old_queen, new_queen, arrow = move
    # need to update the queen list
    for queen in queens:
        if old_queen == queen.GetPosition():
            break

    queen.SetNewPosition(new_queen)
    board_state[old_queen[0]][old_queen[1]] = EMPTY_SPACE
    board_state[new_queen[0]][new_queen[1]] = color
    board_state[arrow[0]][arrow[1]] = ARROW_SPACE


def undo_move_to_board(move, player):
    new_queen, old_queen, arrow = move
    update_move_to_board([new_queen, old_queen, arrow], player[0], player[3])
    board_state[arrow[0]][arrow[1]] = EMPTY_SPACE


# This way our hash table will hold the value of the state_board, his son which is the best move from it and the move
# from his father that made this state
# No need to add the depth, we can find the sate in O(1) each time and then access his son to add his move to the start
# of the list, this way we will always check the best moves in this direction
# Next step we need to do is find how we can clean the move_table from data of illegal moves, or maybe not? is this
# table holds a huge amount of data? not really, the amount of cells in the table is huge but the values hold small data
def add_to_zobrist_table(key, value, move, depth, player_color):
    global hash_table
    if key in hash_table:
        data = {key: (value, move, depth, player_color)}

        hash_table.update(data)
    else:
        hash_table[key] = [value, move, depth, player_color]


def temp_func(value, move):
    global hash_table

    if value not in hash_table:
        hash_table[value] = move

    else:
        tmp = {value: move}
        hash_table.update(tmp)


def alpha_beta(depth, alpha, beta):
    global current_depth
    global son_to_save
    key = None
    if depth == 0:
        son_to_save = None
        return evaluate()
    current_player = players[current_depth % 2]
    current_depth += 1
    if current_player[1]:
        best_value = MIN
        moves = deepcopy(find_legal_moves(current_player[0], False, current_player[3]))
        move_list.clear()
        for move in moves:
            update_move_to_board(move, current_player[0], current_player[3])
            value = alpha_beta(depth - 1, alpha, beta)
            key = compute_hash(board_state)
            add_to_zobrist_table(key, value, move, current_depth, current_player[2])
            undo_move_to_board(move, current_player)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        son_to_save = key
        return best_value

    else:
        best_value = MAX
        moves = deepcopy(find_legal_moves(current_player[0], False, current_player[3]))
        move_list.clear()
        for move in moves:
            update_move_to_board(move, current_player[0], current_player[3])
            value = alpha_beta(depth - 1, alpha, beta)
            key = compute_hash(board_state)
            add_to_zobrist_table(key, value, move, current_depth, current_player[2])
            undo_move_to_board(move, current_player)
            best_value = min(value, best_value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        son_to_save = key
        return best_value


def start_alpha_beta(starting_board_matrix, depth, size, player_queens, enemy_q):
    global board_state
    global board_size
    global players
    global current_depth
    global hash_table

    print(hash_table)
    board_size = size
    board_state = starting_board_matrix
    max_player = [player_queens, True, player_queens[0].GetColor()]
    min_player = [enemy_q, False, enemy_q[0].GetColor()]
    if max_player[2].upper() == "WHITE":
        max_player.append(WHITE_QUEEN)
        min_player.append(BLACK_QUEEN)
    else:
        max_player.append(BLACK_QUEEN)
        min_player.append(WHITE_QUEEN)
    players = [max_player, min_player]
    current_depth = 0
    val = alpha_beta(depth, MIN, MAX)
    for key in hash_table:
        data = hash_table[key]
        if data[0] == val and data[2] == 1 and data[3] == max_player[2]:
            move = data[1]
            print(key)
            break
    hash_table.clear()
    return move

# TODO The bug that happens is that we never make a cell for the starting board state, therefore he never get a son_key
# TODO causing all the problem in our loop, in this loop we must have at least 2 consitions to be able to find the right
# TODO state that we want, if our random range was bigger it was no problem maybe we can do it by telling who player