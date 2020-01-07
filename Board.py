from Constants import *
import time
from Queen import *
import StringInput as SI
import Rules
import copy
from LiranAITest.ZorbistHashing import init_zobrist_table
from AI.IterativeDeepening import iterative_deepening_search, depth_found
# Variables to create the board initial state
board_size = 0
# (y,x)
board_matrix = []
white_queens_setup = []
black_queen_setup = []
arrowsPosition = []
ai_time = 0
player_turn = ["White", "Black"]
players = [["", player_turn[0]], ["", player_turn[1]]]
turn_count = 0


def set_board_size():
    global board_size
    while True:
        size = input("Please enter size, 10 or 6: ")
        if (int(size) == 10) or (int(size) == 6):
            board_size = size
            if int(board_size) == 10:
                SI.SetLettersDictionary(LETTERS_DICTIONARY_10)
            elif int(board_size) == 6:
                SI.SetLettersDictionary(LETTERS_DICTIONARY_06)
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
        position = wq.GetPosition()
        board_matrix[int(position[0])][int(position[1])] = WHITE_QUEEN

    for bq in black_queen_setup:
        position = bq.GetPosition()
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
    global arrowsPosition
    if player == "White":
        queen_to_draw = WHITE_QUEEN
    else:
        queen_to_draw = BLACK_QUEEN
    while True:
        move_input = input("Please enter a move")  # According to the rules QM-WTM/AP
        current_position, new_position, arrow = SI.TranslatingMove(move_input)
        queen_to_move = find_queen(current_position, player)
        # Check if queen is chosen
        if queen_to_move == "No legal queen":
            print("Please choose a queen")
        # Check if queen is free
        elif not queen_to_move.IsQueenFree(board_matrix, board_size):
            print("Queen is not free")
        # Queen move is legal
        elif Rules.IsMoveLegal(current_position, new_position, board_size, board_matrix):
            board_matrix[current_position[0]][current_position[1]] = EMPTY_SPACE
            if Rules.IsMoveLegal(new_position, arrow, board_size, board_matrix):
                board_matrix[new_position[0]][new_position[1]] = queen_to_draw
                queen_to_move.SetNewPosition(new_position)
                board_matrix[arrow[0]][arrow[1]] = ARROW_SPACE
                arrowsPosition.append(arrow)
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
            qpx, qpy = queen.GetPosition()
            if qpx == px and qpy == py:
                return queen

    elif player == "Black":
        for queen in black_queen_setup:
            qpx, qpy = queen.GetPosition()
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
    queen_to_move = find_queen(current_position, color)
    board_matrix[current_position[0]][current_position[1]] = EMPTY_SPACE
    board_matrix[new_position[0]][new_position[1]] = queen
    queen_to_move.SetNewPosition(new_position)
    board_matrix[arrow_pos[0]][arrow_pos[1]] = ARROW_SPACE
    arrowsPosition.append(arrow_pos)


def is_game_ended(player):
    if player == "White":
        queen_setup = white_queens_setup
    else:
        queen_setup = black_queen_setup

    for queen in queen_setup:
        if queen.IsQueenFree(board_matrix, board_size):
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


def initialize_board():
    set_board_size()
    create_board_matrix()
    setup_board()
    set_game_mode()
    set_timer()
    print_board()
    init_zobrist_table(board_size)


initialize_board()
i = 0
while True:
    turn_count += 1
    print(player_turn[i])
    if players[i][0].upper() == "HUMAN":
        player_move(player_turn[i])

    elif players[i][0].upper() == "AI":
        startingTime = time.time()
        if players[i][1].upper() == "WHITE":
            move = iterative_deepening_search(copy.deepcopy(board_matrix), 2, board_size, copy.deepcopy(white_queens_setup),
                                              copy.deepcopy(black_queen_setup), turn_count, ai_time / 10)
            #move = start_alpha_beta(copy.deepcopy(boardMatrix), 1, boardSize, copy.deepcopy(whiteQueensSetup),
             #                       copy.deepcopy(blackQueensSetup), turn_count)
        else:
            move = iterative_deepening_search(copy.deepcopy(board_matrix), 1, board_size, copy.deepcopy(black_queen_setup),
                                              copy.deepcopy(white_queens_setup), turn_count, ai_time / 10)
            #move = start_alpha_beta(copy.deepcopy(boardMatrix), 1, boardSize, copy.deepcopy(blackQueensSetup),
             #                       copy.deepcopy(whiteQueensSetup), turn_count)
        current_queen_position, new_queen_position, arrow_position = move
        ai_move(current_queen_position, new_queen_position, arrow_position, players[i][1])
        move_string = SI.TranslateCordinates(current_queen_position, new_queen_position, arrow_position)

        # should send the AI the boardMatrix and get in returning this data:
        # Current position - finding the queen
        # New position - where the queen should go
        # Arrow position - where the arrow was sent to
        # Evaluation of the move
        # Depth of the MinMax tree we made
        # PV (?)
        # evaluation of PV(?)
        # Data of Pruning or Extensions (Check what he means)
        # Number of access to Hash table
        ## UNCOMMENT THIS--- AIMove(currentPosition, newPosition, arrowPosition, playerTurn[i])
        ## UNCOMMENT THIS--- MoveString = SI.TranslateCordinates(currentPosition, newPosition, arrowPosition) ##
        elapsedTime = time.time() - startingTime
        # This should give me how much time has passed in seconds for the
        # whole turn
        ai_time -= elapsedTime
        print_board()
        print(SI.MoveOutput(move_string, depth_found, elapsedTime))
        ## UNCOMMENT THIS--- print(SI.MoveOutput(MoveString, evaluation, elapsedTime))
        # Here we need to print another technical data (What we got from our function)
        ## UNCOMMENT THIS--- SI.PrintExtraData(depth, PV, PVEvaluation, pruningData, hashAccessNumbers)

        if ai_time <= 0:
            print("AI time has ended, {0} win!!!".format(players[i][1]))
            break
    if is_game_ended(player_turn[i]):
        print("{0} has won!!!!".format(player_turn[(i + 1) % 2]))
        break

    i = (i + 1) % 2

# Change
