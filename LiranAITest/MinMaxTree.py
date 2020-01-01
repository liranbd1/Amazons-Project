from Constants import EMPTY_SPACE, BLACK_QUEEN, WHITE_QUEEN, ARROW_SPACE
from Rules import IsMoveLegal
from LiranAITest.StateNode import *
import random
from copy import deepcopy
MAX, MIN = 1000, -1000
tree = treelib.Tree()


def evaluation(node):
    return random.randint(-10, 10)


def alpha_beta_min_max(depth, is_max_player, node, alpha, beta):
    global i
    i = tree.size() + 1
    if depth != 0:
        enumerate_sons(node)
    if node.is_leaf() or depth == 0:
        return evaluation(node), node

    if is_max_player:
        best_val = MIN
        best_val_node = node
        childrens = tree.children(node.identifier)
        for son in childrens:
            value = alpha_beta_min_max(depth - 1, False, son, alpha, beta)
            if best_val < value[0]:
                best_val = value[0]
                best_val_node = son
            if alpha < best_val:
                alpha = best_val
            if beta <= alpha:
                break
        return best_val, best_val_node

    else:
        best_val = MAX
        best_val_node = node
        childrens = tree.children(node.identifier)
        for son in childrens:
            value = alpha_beta_min_max(depth - 1, True, son, alpha, beta)
            if best_val > value[0]:
                best_val = value[0]
                best_val_node = son
            if beta > best_val:
                beta = best_val
            if beta <= alpha:
                break
        return best_val, best_val_node


def add_son_to_tree(parent_node, move):
    p_node_data = parent_node.data
    temp_board_matrix = deepcopy(p_node_data.get_board_matrix())
    p_turn_queens = deepcopy(p_node_data.get_turn_queens())
    if p_turn_queens[0].GetColor().upper() == "WHITE":
        color = WHITE_QUEEN
    else:
        color = BLACK_QUEEN
    queen_location, queen_new_location, arrow_location = move

    for queen in p_turn_queens:
        if queen.GetPosition() == queen_location:
            queen.SetNewPosition(queen_new_location)
            break
    temp_board_matrix[queen_location[0]][queen_location[1]] = EMPTY_SPACE
    temp_board_matrix[queen_new_location[0]][queen_new_location[1]] = color
    temp_board_matrix[arrow_location[0]][arrow_location[1]] = ARROW_SPACE
    temp_node = tree.create_node(parent=parent_node.identifier, data=StateNode(p_node_data.get_non_turn_queens(),
                                                                               p_turn_queens,
                                                                               temp_board_matrix,
                                                                               p_node_data.get_size()))
    temp_node.data.set_move(move)

# When we enter here as an arrow we have only the new queen position and the arrow position, to create move we are
# missing the original position of the queen, we can pass this as default parameter which is None


def save_legal_moves(old_position, new_position, board_matrix, board_size, parent_node, is_arrow, queen_origin):
    opx, opy = old_position
    npx, npy = new_position
    if not is_arrow:
        saved_queen = board_matrix[opx][opy]
        board_matrix[opx][opy] = EMPTY_SPACE
        find_moves([npx, npy], board_matrix, board_size, parent_node, True, [opx, opy])
        # now we need to create a new list consisting of 3 positions, queenCPos, queenNPos, arrowPos
        board_matrix[opx][opy] = saved_queen

    else:
        if queen_origin is None:
            print("Not working")
        move = [queen_origin, old_position, new_position]
        add_son_to_tree(parent_node, move)


def find_moves(obj_to_check, board_matrix, board_size, parent_node, is_arrow, queen_origin=None):
    px, py = obj_to_check[0], obj_to_check[1]
    for step in range(1, int(board_size)):
        # Check move up
        if IsMoveLegal([px, py], [px - step, py], board_size, board_matrix):
            save_legal_moves([px, py], [px - step, py], board_matrix, board_size, parent_node, is_arrow, queen_origin)
        # Check move down
        if IsMoveLegal([px, py], [px + step, py], board_size, board_matrix):
            save_legal_moves([px, py], [px + step, py], board_matrix, board_size, parent_node, is_arrow, queen_origin)
        # Check right move
        if IsMoveLegal([px, py], [px, py + step], board_size, board_matrix):
            save_legal_moves([px, py], [px, py + step], board_matrix, board_size, parent_node, is_arrow, queen_origin)
        # Check left move
        if IsMoveLegal([px, py], [px, py - step], board_size, board_matrix):
            save_legal_moves([px, py], [px, py - step], board_matrix, board_size, parent_node, is_arrow, queen_origin)
        # Check up-left diagonal
        if IsMoveLegal([px, py], [px - step, py - step], board_size, board_matrix):
            save_legal_moves([px, py], [px - step, py - step], board_matrix, board_size, parent_node, is_arrow,
                             queen_origin)
        # Check down-right diagonal
        if IsMoveLegal([px, py], [px + step, py + step], board_size, board_matrix):
            save_legal_moves([px, py], [px + step, py + step], board_matrix, board_size, parent_node, is_arrow,
                             queen_origin)
        # Check up-right diagonal
        if IsMoveLegal([px, py], [px - step, py + step], board_size, board_matrix):
            save_legal_moves([px, py], [px - step, py + step], board_matrix, board_size, parent_node, is_arrow,
                             queen_origin)
        # Check down-left diagonal
        if IsMoveLegal([px, py], [px + step, py - step], board_size, board_matrix):
            save_legal_moves([px, py], [px + step, py - step], board_matrix, board_size, parent_node, is_arrow,
                             queen_origin)

    # If we checked an arrow we will send back the arrow list, if we check a queen and we done with the loop we can
    # now send it back to the calling function to set up all our possible moves nodes


# TODO improve performance 18-12-19 depth = 1 size = 10*10 time ~ 60 seconds Ram_Usage = 550~600 mb
# 18-12-19 depth = 1 size = 10*10 time~20 seconds Ram_usage ~650 mb


def enumerate_sons(starting_node):
    node_data = starting_node.data
    queen_setup = node_data.get_turn_queens()

    for queen in queen_setup:
        find_moves(queen.GetPosition(), node_data.get_board_matrix(), node_data.get_size(), starting_node, False)


def start_alpha_beta(board_matrix, pqueens, npqueens, size, depth):
    tree.create_node(data=StateNode(pqueens, npqueens, board_matrix, size))
    best_value, best_value_node = alpha_beta_min_max(depth, True, tree.get_node(tree.root), MIN, MAX)
    move = best_value_node.data.get_move()
    tree.remove_node(tree.root)
    tree.root = None
    return move
