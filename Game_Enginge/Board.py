from Game_Enginge.Constants import *
import time
from Game_Enginge.Queen import *
from Game_Enginge import Rules, StringInput as SI
from AI.Enchantments.ZorbistHashing import init_zobrist_table, hash_table, compute_hash, clear_hash
from AI.Search_tree.IterativeDeepening import iterative_deepening_search, depth_found
from AI.Search_tree.Test import mcts_start
from AI.Search_tree.MCTS import MCTS_Tree as mcts
from copy import deepcopy
import numpy as np

# Variables to create the board initial state
board_size = 0
# (y,x)
board_matrix = []
white_queens_setup = []
black_queen_setup = []
ai_time = 0
player_turn = ["White", "Black"]
players = [["", player_turn[0]], ["", player_turn[1]]]
turn_count = 0
game_rules = 0


def set_board_size():
    global board_size
    while True:
        size = input("Please enter size, 10 or 6: ")
        if (int(size) == 10) or (int(size) == 6):
            board_size = size
            if int(board_size) == 10:
                SI.set_letters_dictionary(LETTERS_DICTIONARY_10)
            elif int(board_size) == 6:
                SI.set_letters_dictionary(LETTERS_DICTIONARY_06)
            break

        print("Please enter a valid size")


def create_board_matrix():
    global board_matrix
    board_matrix = [
        [EMPTY_SPACE for x in range(int(board_size))] for y in range(int(board_size))
    ]


def setup_board():
    queen_position_setup()
    for wq in white_queens_setup:
        position = wq.get_position()
        board_matrix[int(position[0])][int(position[1])] = WHITE_QUEEN

    for bq in black_queen_setup:
        position = bq.get_position()
        board_matrix[int(position[0])][int(position[1])] = BLACK_QUEEN


def queen_position_setup():
    global white_queens_setup
    global black_queen_setup

    if int(board_size) == 10:
        start_position_white = WHITE_QUEENS_START_10
        start_position_black = BLACK_QUEENS_START_10
    else:
        start_position_white = WHITE_QUEENS_START_06
        start_position_black = BLACK_QUEENS_START_06

    for i in range(len(start_position_white)):
        white_queen_position = start_position_white[i]
        white_queen_to_add = Queen(
            [white_queen_position[0], white_queen_position[1]], "White"
        )
        white_queens_setup.insert(i, white_queen_to_add)

        black_queen_position = start_position_black[i]
        black_queen_to_add = Queen(
            [black_queen_position[0], black_queen_position[1]], "Black"
        )
        black_queen_setup.insert(i, black_queen_to_add)


def player_move(player):
    # global arrowsPosition
    if player == "White":
        queen_to_draw = WHITE_QUEEN
    else:
        queen_to_draw = BLACK_QUEEN
    while True:
        move_input = input("Please enter a move")  # According to the rules QM-WTM/AP
        current_position, new_position, arrow = SI.translating_move(move_input)
        queen_to_move = find_queen(current_position, player)
        # Check if queen is chosen
        if queen_to_move == "No legal queen":
            print("Please choose a queen")
        # Check if queen is free
        elif not queen_to_move.is_queen_free(board_matrix, board_size):
            print("Queen is not free")
        # Queen move is legal
        elif Rules.is_move_legal(current_position, new_position, board_size, board_matrix):
            board_matrix[current_position[0]][current_position[1]] = EMPTY_SPACE
            if Rules.is_move_legal(new_position, arrow, board_size, board_matrix):
                board_matrix[new_position[0]][new_position[1]] = queen_to_draw
                queen_to_move.set_new_position(new_position)
                board_matrix[arrow[0]][arrow[1]] = ARROW_SPACE
                # arrowsPosition.append(arrow)
                break
            else:
                board_matrix[current_position[0]][current_position[1]] = queen_to_draw
        else:
            print("Move not legal")
    print_board()


def find_queen(current_position, player):
    px, py = current_position
    if player == "White":
        for queen in white_queens_setup:
            qpx, qpy = queen.get_position()
            if qpx == px and qpy == py:
                return queen

    elif player == "Black":
        for queen in black_queen_setup:
            qpx, qpy = queen.get_position()
            if qpx == px and qpy == py:
                return queen

    return "No legal queen"


def print_board():
    i = int(board_size) - 1
    for line in board_matrix:
        print(LETTERS[i], end="")
        print(line)
        i -= 1

    for i in range(int(board_size)):
        print("   {0}   ".format(i + 1), end="")
    print()


def set_timer():
    global ai_time
    ai_time = input("Please enter timer for each player in minutes: ")
    ai_time = float(ai_time) * 60  # Converting to seconds


def ai_move(current_position, new_position, arrow_pos, color):
    if color == "White":
        queen = WHITE_QUEEN
    else:
        queen = BLACK_QUEEN
    print(color)
    queen_to_move = find_queen(current_position, color)
    print(queen_to_move)
    board_matrix[current_position[0]][current_position[1]] = EMPTY_SPACE
    board_matrix[new_position[0]][new_position[1]] = queen
    queen_to_move.set_new_position(new_position)
    board_matrix[arrow_pos[0]][arrow_pos[1]] = ARROW_SPACE
    # arrowsPosition.append(arrow_pos)


def is_game_ended(player):
    if player == "White":
        queen_setup = white_queens_setup
    else:
        queen_setup = black_queen_setup

    for queen in queen_setup:
        if queen.is_queen_free(board_matrix, board_size):
            return False
    return True


def set_game_mode():
    while True:
        game_mode = input("PvE or EvE? ")
        if game_mode.upper() == "PVE":
            who_starts()
            break
        elif game_mode.upper() == "EVE":
            players[0][0] = "AI"
            players[1][0] = "AI"
            break
        elif game_mode.upper() == "PVP":
            players[0][0] = "Human"
            players[1][0] = "Human"
            break
        else:
            print("Please enter a valid input")


def who_starts():
    while True:
        color_chosen = input("Please choose your color, white or black(white starts): ")
        if color_chosen.upper() == "WHITE":
            players[0][0] = "Human"
            players[1][0] = "AI"
            break
        elif color_chosen.upper() == "BLACK":
            players[0][0] = "AI"
            players[1][0] = "Human"
            break
        else:
            print("Please enter a valid input")

def are_we_in_the_endgame_now():
    # we need to get to matrix of relative territory for each color
    pass


def initialize_board():
    set_board_size()
    create_board_matrix()
    setup_board()
    set_game_mode()
    set_timer()
    print_board()
    init_zobrist_table(board_size)


# state = [board_matrix, p_queens, e_queens]
def ai_algorithm_to_run(count, state):

    move_found = mcts_start(board_matrix, board_size, 10000, state[1], state[2])
    return SI.translating_move(move_found)
   # if count < 20:
    #print("MCTS")
    #np_board_state = np.array([np.array(line) for line in state[0]])
    #np_p_queens = np.array(state[1], order='F')
   # np_e_queens = np.array(state[2], order='F')
    #np_state = np.array([np_board_state, np_p_queens, np_e_queens, state[3], state[4]])
    #monte_carlo = mcts(np_state)
    #move_found = monte_carlo.start_mcts_search(1000)
    #return SI.translating_move(move_found)
    #else:
     #   print("AlphaBeta")
      #  move_found = iterative_deepening_search(state[0], 2, board_size, state[1], state[2], count, ai_time / 10)


initialize_board()
i = 0
while True:
    turn_count += 1
    print(player_turn[i])
    if players[i][0].upper() == "HUMAN":
        player_move(player_turn[i])

    elif players[i][0].upper() == "AI":
        startingTime = time.time()
        clear_hash(turn_count)
        state_key = compute_hash(board_matrix)
        if state_key in hash_table:
            state_data = hash_table[state_key]
            if state_data[6] < 2:
                max_depth = 2
            else:
                max_depth = state_data[6]
        else:
            max_depth = 2
        if players[i][1].upper() == "WHITE":
            game_state = [board_matrix, white_queens_setup, black_queen_setup, "black", board_size]
        else:
            game_state = [board_matrix, black_queen_setup, white_queens_setup, "white", board_size]

        move = ai_algorithm_to_run(turn_count, game_state)
        current_queen_position, new_queen_position, arrow_position = move
        print(move)
        ai_move(current_queen_position, new_queen_position, arrow_position, players[i][1])
        move_string = SI.translate_cordinate(current_queen_position, new_queen_position, arrow_position)

        elapsedTime = time.time() - startingTime
        ai_time -= elapsedTime
        print_board()
        print(SI.move_output(move_string, depth_found, elapsedTime))
        # Here we need to print another technical data (What we got from our function)
        ## UNCOMMENT THIS--- SI.PrintExtraData(depth, PV, PVEvaluation, pruningData, hashAccessNumbers)

        if ai_time <= 0:
            print("AI time has ended, {0} win!!!".format(players[i][1]))

    if is_game_ended(player_turn[i]):
        print("{0} has won!!!!".format(player_turn[(i + 1) % 2]))
        break

    i = (i + 1) % 2


