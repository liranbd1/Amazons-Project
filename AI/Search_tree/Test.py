from random import randint
from AI.Enchantments.MoveGenerator import move_generator
from Game_Enginge.StringInput import translate_cordinate, translating_move
from Game_Enginge.Constants import EMPTY_SPACE, BLACK_QUEEN, WHITE_QUEEN, ARROW_SPACE
from Game_Enginge.Rules import is_move_legal
from AI.Enchantments.ZorbistHashing import compute_hash
import numpy as np

mcts_table = {}
board_state = []
board_size = 0
# First we want somehow to hold our data how about I will use the zobrist here?


def mcts_start(board, size, iteration, p_queens, e_queens):
    global board_state
    global board_size

    board_size = size
    board_state = board
    key = compute_hash(board_state)
    mcts_table[key] = [0, 0, None, None, [], p_queens, e_queens]# num of wins, num of visits, action, parent, sons
    for i in range(iteration):
        tree_policy(mcts_table[key])
        score = simulation(mcts_table[compute_hash(board_state)])
        backpropagation(score)
    best_child_key = best_action()
    return translating_move(mcts_table[best_child_key][2])


def backpropagation(points):
    starting_state = mcts_table[compute_hash(board_state)]

    while starting_state[3] is not None:
        starting_state[0] += points
        starting_state[1] += 1
        undo_action(starting_state[2], starting_state[6])
        starting_state = mcts_table[compute_hash(board_state)]


def simulation(state):
    action_list = []
    queens = [state[5], state[6]]
    i = 0
    while not is_terminal(queens[i]):
        action_set = get_actions(queens[i])
        action = action_set[randint(0, len(action_set)-1)]
        action_list.insert(0, action)
        perform_action(action, queens[i])
        i = (i+1) % 2
    score = reward()
    for act in action_list:
        undo_action(act, queens[(i+1)%2])
        i = (i+1) % 2
    return score


def undo_action(action, queens):
    global board_state

    old_position, clear_queen, arrow = translating_move(action)
    if queens[0].get_color().upper() == "WHITE":
        color = WHITE_QUEEN
    else:
        color = BLACK_QUEEN
    for queen in queens:
        if clear_queen == queen.get_position():
            queen.set_new_position(old_position)
            board_state[clear_queen[0]][clear_queen[1]] = EMPTY_SPACE
            board_state[old_position[0]][old_position[1]] = color
            if old_position != arrow:
                board_state[arrow[0]][arrow[1]] = EMPTY_SPACE
            break


def reward():
    return randint(0, 1)


def tree_policy(state):
    if not is_terminal(state[5]):
        if not is_fully_expanded():
            key = compute_hash(board_state)
            action_set = np.setdiff1d(get_actions(state[5]), state[4])
            action = action_set[randint(0, len(action_set)-1)]
            perform_action(action, state[5])
            expansion(action, key, state)
            return
        else:
            child_key = best_action()
            perform_action(mcts_table[child_key][2], mcts_table[child_key][5])

    else:
        return


def best_action():
    key = compute_hash(board_state)
    childrens = mcts_table[key][4]
    Ni = mcts_table[key][1]
    max_value = -100000
    max_child = 0
    for child in childrens:
        wi = mcts_table[child][0]
        ni = mcts_table[child][1]
        ucb = wi/ni + 1.8*np.sqrt(np.log(Ni)/ni)
        if ucb > max_value:
            max_value = ucb
            max_child = child
    return max_child


def expansion(action, key, state):
    global mcts_table

    son_key = compute_hash(board_state)
    mcts_table[key][4].append(son_key)
    mcts_table[son_key] = [0, 0, action, key, [], state[6], state[5]]


def perform_action(action, queens):
    global board_state

    old_queen, new_queen, arrow = translating_move(action)
    if queens[0].get_color().upper() == "WHITE":
        color = WHITE_QUEEN
    else:
        color = BLACK_QUEEN

    for queen in queens:
        if old_queen == queen.get_position():
            queen.set_new_position(new_queen)
            board_state[old_queen[0]][old_queen[1]] = EMPTY_SPACE
            board_state[new_queen[0]][new_queen[1]] = color
            board_state[arrow[0]][arrow[1]] = ARROW_SPACE
            break


def is_fully_expanded():
    key = compute_hash(board_state)
    return len(get_actions(mcts_table[key][5])) == len(mcts_table[key][4])


def get_actions(queens):
    moves_string_list = []
    moves = move_generator(queens, board_state, board_size)
    for move in moves:
        moves_string_list.append(translate_cordinate(move[0], move[1], move[2]))

    return moves_string_list


def is_terminal(queens):
    blocked = 0
    size = int(board_size)
    for queen in queens:
        (row, col) = queen.get_position()

        if row + 1 < size:
            if board_state[row + 1][col] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1

        if col + 1 < size:
            if board_state[row][col + 1] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1

        if row - 1 > 0:
            if board_state[row - 1][col] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1
        if col - 1 > 0:
            if board_state[row][col - 1] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1

        if row + 1 < size and col + 1 < size:
            if board_state[row + 1][col + 1] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1

        if row + 1 < size and col - 1 > 0:
            if board_state[row + 1][col - 1] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1

        if row - 1 > 0 and col - 1 > 0:
            if board_state[row - 1][col - 1] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1

        if row - 1 > 0 and col + 1 < size:
            if board_state[row - 1][col + 1] != EMPTY_SPACE:
                blocked += 1
        else:
            blocked += 1

    if blocked == (len(queens) * 8):  # If every queen is blocked from 8 positions
        return True
    else:
        return False
