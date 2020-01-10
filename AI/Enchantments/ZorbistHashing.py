from random import randint
from Game_Enginge.Constants import WHITE_QUEEN, BLACK_QUEEN, ARROW_SPACE, EMPTY_SPACE
zobrist_table = []
board_size = 0

hash_table = {}


def clear_hash(turn_count):
    for key in list(hash_table):
        data = hash_table[key]
        if data[3] < turn_count:
            hash_table.pop(key)


def indexing(piece):
    if piece == WHITE_QUEEN:
        return 0
    if piece == BLACK_QUEEN:
        return 1
    if piece == ARROW_SPACE:
        return 2
    else:
        return -1


def init_zobrist_table(size):
    global zobrist_table
    global board_size
    zobrist_table = [[[randint(1, 2**100 - 1)for i in range(4)]for j in range(int(size))]for k in range(int(size))]
    board_size = size


def compute_hash(board):
    h = 0
    for i in range(int(board_size)):
        for j in range(int(board_size)):
            if board[i][j] != EMPTY_SPACE:
                piece = indexing(board[i][j])
                h ^= zobrist_table[i][j][piece]
    return h
