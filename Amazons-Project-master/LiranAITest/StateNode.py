import treelib


class StateNode(treelib.Node):

    def __init__(self, p_queens, np_queens, board_matrix, board_size):
        super(StateNode, self).__init__()
        self.player_queen_setup = p_queens
        self.non_player_queen_setup = np_queens
        self.board_matrix = board_matrix
        self.board_size = board_size
        self.move = []

    def get_turn_queens(self):
        return self.player_queen_setup

    def get_non_turn_queens(self):
        return self.non_player_queen_setup

    def get_board_matrix(self):
        return self.board_matrix

    def get_size(self):
        return  self.board_size

    def set_move(self, move):
        self.move = move

    def get_move(self):
        return self.move
