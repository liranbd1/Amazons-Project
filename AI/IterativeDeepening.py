from AI.MinMaxTree import start_alpha_beta
from Constants import MIN_VALUE


def IDS(max_depth, board_matrix, pqueens, npqueens, size, _serachTime = None):
    search_time = _serachTime
    global_best = MIN_VALUE
    global_move = None
    for depth in range(1, max_depth):
        best_move, best_value = start_alpha_beta(board_matrix, pqueens, npqueens, size, depth)
        if best_value > global_best:
            global_best = best_value
            global_move = best_move
    return global_move

