from AI.Search_tree.AlphaBetaPruning import start_alpha_beta
from Game_Enginge.Constants import MIN_VALUE
from time import time
import math

depth_found = 0
WINDOW_SIZE = 25  # For the Aspiration Search
MAX = math.inf


def iterative_deepening_search(starting_board_matrix, max_depth, size, player_queens, enemy_q,
                               turn_number, time_to_play):
    global depth_found
    search_time = time_to_play
    global_best = MIN_VALUE
    global_best_move = []
    start_time = time()
    val = 0
    for ids_depth in range(2, max_depth + 1):  # We should start check from depth 2
        start = time()
        if ids_depth == 2:
            val, move = aspiration(starting_board_matrix, ids_depth, 0, size, player_queens, enemy_q,
                                   turn_number)
        else:
            val, move = aspiration(starting_board_matrix, ids_depth, val, size, player_queens, enemy_q,
                                   turn_number)
        end = time()
        print(end-start)
        print(move)
        if val > global_best:
            global_best = val
            global_best_move = move
            depth_found = ids_depth
        elapsed_time = time() - start_time
        search_time -= elapsed_time
        if search_time <= 0:
            break
    # print("Elapsed time: {0}".format(elapsed_time))
    end_time = time()
    print("Finish deepening", end_time-start_time)
    return global_best_move


def aspiration(starting_board_matrix, maxDepth, previous, size, player_queens, enemy_q, turn_number):
    alpha = previous - WINDOW_SIZE
    beta = previous + WINDOW_SIZE
    result, move = start_alpha_beta(starting_board_matrix, maxDepth, size, player_queens, enemy_q,
                                    turn_number, alpha, beta)
    if move is False:
        alpha = -MAX
        beta = MAX
        result, move = start_alpha_beta(starting_board_matrix, maxDepth, size, player_queens, enemy_q, turn_number,
                                        alpha, beta)
        return result, move
    else:
        return result, move
