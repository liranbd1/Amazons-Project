from LiranAITest.AlphaBetaPruning import start_alpha_beta
from Constants import MIN_VALUE
import time

depth_found = 0


def iterative_deepening_search(starting_board_matrix, max_depth, size, player_queens, enemy_q,
                               turn_number, time_to_play):
    global depth_found
    search_time = time_to_play
    global_best = MIN_VALUE
    global_best_move = []
    start_time = time.time()
    for ids_depth in range(1, max_depth+1):
        val, move = start_alpha_beta(starting_board_matrix, ids_depth, size, player_queens, enemy_q, turn_number)
        if val > global_best:
            global_best = val
            global_best_move = move
            depth_found = ids_depth
        elapsed_time = time.time() - start_time
        search_time -= elapsed_time
        if search_time <= 0:
            break
    return global_best_move

