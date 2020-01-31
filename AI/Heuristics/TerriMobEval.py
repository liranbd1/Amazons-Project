""" Territory Mobility Evaluation -
Territory: Assuming we know how fast each player can get to any space in the board we can check which player can
get to space A faster, the one who get faster has the control of the territory.
Using this with the mobility evaluation we can make the queens move to areas with more possible moves (the center
of the board) and give them the block enemy units in smaller territories.
Our heuristics has the cost of 4 to 1 favoring the territory heuristic"""
# Creating the evaluation function
# The evaluation function will find which player can get first to each tile
# In addition we will keep the moves that we can get by 1 step
# -- we will create 2 new matrices that in each position will be the minimum number of step
# -- that require to get there for each player

from Game_Enginge.Rules import is_move_legal
from copy import deepcopy


def TerritoryMobilityEvaluation(board, player_queens, enemy_queens, board_size):
    possible_squares = []
    player_territory = 0
    enemy_territory = 9
    player_mobility = 0
    enemy_mobility = 0
    for row in range(int(board_size)):
        for col in range(int(board_size)):
            possible_squares.append([row, col])
    player_squares = deepcopy(possible_squares)
    enemy_squares = possible_squares
    player_board = [[0 for x in range(int(board_size))] for y in range(int(board_size))]
    enemy_board = [[0 for x in range(int(board_size))] for y in range(int(board_size))]
    turn_1 = []
    turn_2 = []
    turn_3 = []
    turn_4 = []
    turn_5 = []
    enemy_turn_1 = []
    enemy_turn_2 = []
    enemy_turn_3 = []
    enemy_turn_4 = []
    enemy_turn_5 = []

    for queen in player_queens:
        queen_position = queen.get_position()
        x, y = queen_position
        for square in player_squares:
            if is_move_legal([x, y], square, board_size, board):
                px, py = square
                player_mobility += 1
                turn_1.append(square)
                player_squares.remove(square)
                player_board[px][py] = 1
    for base_square in turn_1:
        for target_square in player_squares:
            if is_move_legal(base_square, target_square, board_size, board):
                px, py = target_square
                turn_2.append(target_square)
                player_squares.remove(target_square)
                player_board[px][py] = 2
    for base_square in turn_2:
        for target_square in player_squares:
            if is_move_legal(base_square, target_square, board_size, board):
                px, py = target_square
                turn_3.append(target_square)
                player_squares.remove(target_square)
                player_board[px][py] = 3
    for base_square in turn_3:
        for target_square in player_squares:
            if is_move_legal(base_square, target_square, board_size, board):
                px, py = target_square
                turn_4.append(target_square)
                player_squares.remove(target_square)
                player_board[px][py] = 4
    if len(player_squares) is not 0:
        for base_square in player_squares:
            for target_square in turn_5:
                if is_move_legal(base_square, target_square, board_size, board):
                    turn_5.append(target_square)
                    player_squares.remove(target_square)
                    px, py = target_square
                    player_board[px][py] = 5

    for queen in enemy_queens:
        queen_position = queen.get_position()
        x, y = queen_position
        for square in enemy_squares:
            if is_move_legal([x, y], square, board_size, board):
                enemy_mobility += 1
                enemy_turn_1.append(square)
                enemy_squares.remove(square)
                px, py = square
                enemy_board[px][py] = 1
    for base_square in enemy_turn_1:
        for target_square in enemy_squares:
            if is_move_legal(base_square, target_square, board_size, board):
                enemy_turn_2.append(target_square)
                enemy_squares.remove(target_square)
                px, py = target_square
                enemy_board[px][py] = 2
    for base_square in enemy_turn_2:
        for target_square in enemy_squares:
            if is_move_legal(base_square, target_square, board_size, board):
                enemy_turn_3.append(target_square)
                enemy_squares.remove(target_square)
                px, py = target_square
                enemy_board[px][py] = 3
    for base_square in enemy_turn_3:
        for target_square in enemy_squares:
            if is_move_legal(base_square, target_square, board_size, board):
                enemy_turn_4.append(target_square)
                enemy_squares.remove(target_square)
                px, py = target_square
                enemy_board[px][py] = 4
    if len(enemy_squares) is not 0:
        for base_square in enemy_turn_4:
            for target_square in enemy_squares:
                if is_move_legal(base_square, target_square, board_size, board):
                    enemy_turn_5.append(target_square)
                    enemy_squares.remove(target_square)
                    px, py = target_square
                    enemy_board[px][py] = 5

    for row in range(int(board_size)):
        for col in range(int(board_size)):
            if enemy_board[row][col] < player_board[row][col]:
                enemy_territory += 1
            if player_board[row][col] < enemy_board[row][col]:
                player_territory += 1

    return player_territory-enemy_territory, player_mobility-enemy_mobility
