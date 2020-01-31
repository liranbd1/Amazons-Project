from AI.Heuristics.TerriMobEval import TerritoryMobilityEvaluation
from AI.Heuristics.MobilityEvaluation import MobilityEvaluation
from Game_Enginge.Constants import EMPTY_SPACE, WHITE_QUEEN, BLACK_QUEEN, ARROW_SPACE
from AI.Enchantments.ZorbistHashing import compute_hash, hash_table
from AI.Enchantments.Killer_Moves import killer_moves
import collections
import random
from AI.Enchantments.MoveGenerator import move_generator
from AI.Enchantments.DataToSave import data_to_save_AB

hash_access_count = 0
MIN = -1000
MAX = 1000
board_state = []
board_size = 0
players = []
current_depth = 0
son_to_save = None
turn_count = 0
pruning_count = 0
max_depth_found = 0


""" Simulating the move that was made to the board"""
def update_move_to_board(move, queens, color):
    global board_state
    global current_depth

    old_queen, new_queen, arrow = move
    # need to update the queen list
    for queen in queens:
        if old_queen == queen.get_position():
            queen.set_new_position(new_queen)
            board_state[old_queen[0]][old_queen[1]] = EMPTY_SPACE
            board_state[new_queen[0]][new_queen[1]] = color
            board_state[arrow[0]][arrow[1]] = ARROW_SPACE
            current_depth += 1
            break

"""Undoing the move that were simulated to the board"""
def undo_move_to_board(move, player):
    global current_depth

    pos_to_back, pos_to_del, arrow = move

    for queen in player[0]:
        if pos_to_del == queen.get_position():
            queen.set_new_position(pos_to_back)
            board_state[pos_to_del[0]][pos_to_del[1]] = EMPTY_SPACE
            board_state[pos_to_back[0]][pos_to_back[1]] = player[3]
            if pos_to_back != arrow:
                board_state[arrow[0]][arrow[1]] = EMPTY_SPACE
            current_depth -= 1
            break


"""Updating our zobrist hash table
key: the value we are given from the hash function for the specific board state
value: the value we bubbled up or found with the evaluation function
move: what was the move that we want to do from this state
depth: how deep is the state in the full tree search
son_key: the key of the son node
player_color: who made the move
max_depth: how deep we looked"""
def add_to_zobrist_hash_table(key, value, move, depth, son_key, player_color, max_depth):
    global hash_access_count

    hash_access_count += 1
    if key not in hash_table:
        hash_table[key] = [value, move, depth, depth + turn_count, son_key, player_color, max_depth - depth]
    else:
        # Checking if the data is new
        data = hash_table[key]
        new_data = [value, move, depth, depth + turn_count, son_key, player_color, max_depth - depth]
        # if new we update the data
        if data != new_data:
            if data[0] < new_data[0] and data[6] < new_data[6]:
                hash_table.update({key: new_data})


"""evaluating our leaf node"""
def evaluate():

    if players[current_depth % 2][1] is True:
        player_queens = players[current_depth % 2][0]
        enemy_queens = players[(current_depth+1) % 2][0]
    else:
        player_queens = players[(current_depth+1) % 2][0]
        enemy_queens = players[current_depth % 2][0]

    territory_score, mobility_score = TerritoryMobilityEvaluation(board_state, player_queens, enemy_queens, board_size)
    random_score = random.randint(-10, 10)
    score = 4 * territory_score + mobility_score + 0.2 * random_score
    return score


"""sof evaluation for the sorting of the moves"""
def soft_evaluate():
    global hash_access_count

    key = compute_hash(board_state)
    if key in hash_table:
        hash_access_count += 1
        data = hash_table[key]
        return data[0]
    else:
        return random.randint(-10, 10)


"""sorting the moves for better pruning"""
def sort_moves(moves_to_sort, player):
    global hash_access_count

    moves_scores = {}
    iteration = 1
    for move in moves_to_sort:
        update_move_to_board(move, player[0], player[3])
        key = compute_hash(board_state)
        if key not in hash_table:
            if players[(current_depth+1) % 2][1] is True:
                my_value = MobilityEvaluation(board_state, board_size, players[(current_depth+1) % 2][0])
                enemy_value = MobilityEvaluation(board_state, board_size, players[current_depth % 2][0])
            else:
                enemy_value = MobilityEvaluation(board_state, board_size, players[(current_depth+1) % 2][0])
                my_value = MobilityEvaluation(board_state, board_size, players[current_depth % 2][0])
            value = my_value - enemy_value
        else:
            data = hash_table[key]
            value = data[0]
            hash_access_count += 1
        moves_scores[value] = move
        iteration += 1
        undo_move_to_board(move, player)

    if players[current_depth % 2] is True:
        sorted_max_moves = collections.OrderedDict(sorted(moves_scores.items(), reverse=True))
    else:
        sorted_max_moves = collections.OrderedDict(sorted(moves_scores.items()))
    sorted_list = list(sorted_max_moves.values())
    if current_depth - 1 in killer_moves:
        for killer_move in killer_moves[current_depth - 1]:
            if killer_move in sorted_list:
                sorted_list = killer_move + sorted_list.pop(sorted_list.index(killer_move))
    return sorted_list


"""The alpha beta algorithm"""
def alpha_beta(depth, alpha, beta):
    global current_depth
    global son_to_save
    global pruning_count
    global max_depth_found

    current_player = players[current_depth % 2]

    if depth == 0:
        max_depth_found = current_depth
        son_to_save = None
        key = compute_hash(board_state)
        if key not in hash_table:
            value = evaluate()
        else:
            data = hash_table[key]
            value = data[0]

        return value

    move_count = 0
    # 1st stopping condition for the alpha_beta (Since we are not looking to the end for now this is efficient)
    # Will need to add a stopping condition where we are having the queens isolated
    if current_player[1]:
        max_evaluation = MIN
        moves = move_generator(current_player[0], board_state, board_size)
        moves = sort_moves(moves, current_player)
        while len(moves) != 0:
            move = moves.pop(0)
            move_count += 1
            update_move_to_board(move, current_player[0], current_player[3])
            value = alpha_beta(depth - 1, alpha, beta)
            key = compute_hash(board_state)
            add_to_zobrist_hash_table(key, value, move, current_depth, son_to_save, current_player[2], max_depth_found)
            undo_move_to_board(move, current_player)
            if max_evaluation < value:
                max_evaluation = value
                son_to_save = key
            alpha = max(alpha, max_evaluation)
            if beta <= alpha:
                pruning_count += 1
                if current_depth - 1 in killer_moves:
                    if move not in killer_moves[current_depth - 1]:
                        if len(killer_moves[current_depth - 1]) == 2:
                            killer_moves[current_depth - 1] = move + [killer_moves[current_depth - 1][0]]
                        elif len(killer_moves[current_depth - 1]) == 1:
                            killer_moves[current_depth - 1] = \
                                move + [killer_moves[current_depth - 1]]  # killer Move produced a cut-off
                else:
                    killer_moves[current_depth - 1] = move
                break
        return max_evaluation

    else:
        min_evaluation = MAX
        moves = move_generator(current_player[0], board_state, board_size)
        moves = sort_moves(moves, current_player)
        while len(moves) != 0:
            move = moves.pop(0)
            move_count += 1
            update_move_to_board(move, current_player[0], current_player[3])
            value = alpha_beta(depth - 1, alpha, beta)
            key = compute_hash(board_state)
            add_to_zobrist_hash_table(key, value, move, current_depth, son_to_save, current_player[2], max_depth_found)
            undo_move_to_board(move, current_player)
            if min_evaluation > value:
                min_evaluation = value
                son_to_save = key
            beta = min(beta, min_evaluation)
            if beta <= alpha:
                pruning_count += 1
                if current_depth - 1 in killer_moves:
                    if move not in killer_moves[current_depth - 1]:
                        if len(killer_moves[current_depth - 1]) == 2:
                            killer_moves[current_depth - 1] = move + [killer_moves[current_depth - 1][0]]
                        elif len(killer_moves[current_depth - 1]) == 1:
                            killer_moves[current_depth - 1] = \
                                move + [killer_moves[current_depth - 1]]  # killer Move produced a cut-off
                else:
                    killer_moves[current_depth - 1] = move
                break
        return min_evaluation


def clear_hash_table():
    for key in hash_table:
        if turn_count > hash_table[key][3]:
            del hash_table[key]


"""The call for this script page - getting all the needed data and starting the alpha beta after all is ready"""
def start_alpha_beta(starting_board_matrix, depth, size, player_queens, enemy_q, turn_number, alpha, beta):
    global board_state
    global board_size
    global players
    global current_depth
    global turn_count
    global pruning_count
    global max_depth_found
    global hash_access_count

    hash_access_count = 0
    max_depth_found = 0
    pruning_count = 0
    move = 0
    # Setting values
    turn_count = turn_number
    board_size = size
    board_state = starting_board_matrix

    # Getting the players data
    max_player = [player_queens, True, player_queens[0].get_color()]
    min_player = [enemy_q, False, enemy_q[0].get_color()]
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
    clear_hash_table()
    val = alpha_beta(depth, alpha, beta)
    data_to_save_AB(pruning_count, depth, hash_access_count)
    # Searching for the value in our hash table.
    for key in hash_table:
        data = hash_table[key]
        if data[0] == val and data[3] == turn_count + 1 and data[5] == max_player[2]:
            move = data[1]
            break
    if move == 0 or len(move) != 3:
        return 1, False

    return val, move
