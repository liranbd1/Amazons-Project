pruning_count = 0
depth_searched_AB = 0
hash_access_count = 0
depth_searched_MCTS = 0
simulations = 0


def data_to_save_AB(prun_count, depth, hash):
    global pruning_count
    global depth_searched
    global hash_access_count

    pruning_count = prun_count
    depth_searched = depth
    hash_access_count = hash


def data_to_save_mcts(depth, simulation):
    global depth_searched_MCTS
    global simulations

    depth_searched_MCTS = depth
    simulations = simulation