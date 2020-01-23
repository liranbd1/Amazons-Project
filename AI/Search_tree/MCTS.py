import numpy as np
from random import randint
from AI.Enchantments.MoveGenerator import move_generator
from Game_Enginge.StringInput import translate_cordinate, translating_move
from Game_Enginge.Constants import EMPTY_SPACE, WHITE_QUEEN, BLACK_QUEEN, ARROW_SPACE
import random

# Game tree node
class MCTS_Node:
    def __init__(self, state, parent=None, statistics={}):
        self.state = state
        self.parent = parent
        self.children = {}
        self.statistics = statistics

    def expand(self, action, next_state):
        child = MCTS_Node(next_state, parent=self)
        self.children[action] = child
        return child


class MCTS_Tree:
    def __init__(self, state, C=1):
        self.C = C
        self.root = MCTS_Node(state, statistics={" visits ": 0, " reward ": np.zeros(2)})

    def is_fully_expanded(self, node):
        return len(self.get_actions(node.state)) == len(list(node.children))

    def best_action(self, node):
        children = list(node.children.values())
        visits = np.array(([child.statistics[" visits "] for child in children]))
        rewards = np.array(([child.statistics[" reward "] for child in children]))
        total_rollouts = node.statistics[" visits "]
        pid = self.get_current_player_id(node.state)
        # calculate UCB1 value for all child nodes
        ucb = (rewards[:, pid] / visits + self.C * np.sqrt(2 * np.log(total_rollouts) / visits))
        best_ucb_ind = np.random.choice(np.flatnonzero(ucb == ucb.max()))
        return list(node.children.keys())[best_ucb_ind]

    def tree_policy(self, node):
        while not self.is_terminal(node.state):
            if not self.is_fully_expanded(node):
                act_set = np.setdiff1d(self.get_actions(node.state), list(node.children.keys()))
                action = act_set[randint(0, len(act_set) - 1)]
                newstate = self.perform_action(action, node.state)
                childnode = node.expand(action, newstate)  # <- expansion
                childnode.statistics = {" visits ": 0, " reward ": np.zeros(2)}

                return childnode
            else:
                node = node.children[self.best_action(node)]  # <- selection
        return node

    def rollout(self, node):
        roll_state = node.state.copy()
        while not self.is_terminal(roll_state):
            act_set = self.get_actions(roll_state)
            if len(act_set) == 1 :
                print("HI")
            action = act_set[randint(0, len(act_set) - 1)]
            roll_state = self.perform_action(action, roll_state)
        return self.reward(roll_state)

    def backup(self, node, reward):
        while not node is None:
            node.statistics[" visits "] += 1
            node.statistics[" reward "] += reward
            node = node.parent

    def start_mcts_search(self, iterations):
        # Vanilla MCTS loop
        for i in range(iterations):
            selected_node = self.tree_policy(self.root)  # selection + expansion
            reward = self.rollout(selected_node)  # rollout
            self.backup(selected_node, reward)  # backup
        return self.best_action(self.root)

    def get_actions(self, state):
        moves_string_list = []
        moves = move_generator(state[1], state[0], state[4])
        for move in moves:
            moves_string_list.append(translate_cordinate(move[0], move[1], move[2]))

        return moves_string_list

    def get_current_player_id(self, state):
        if state[3].upper() == "WHITE":
            return 0
        else:
            return 1

    def is_terminal(self, state):
        board = state[0]
        queens = state[1]
        size = int(state[4])
        for queen in queens:
            (row, col) = queen.get_position()
            if row + 1 < size:
                if board[row + 1][col] != EMPTY_SPACE:
                    return False
            else:
                return False
            if col + 1 < size:
                if board[row][col + 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row - 1 > 0:
                if board[row - 1][col] != EMPTY_SPACE:
                    return False
            else:
                return False
            if col - 1 > 0:
                if board[row][col - 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row + 1 < size and col + 1 < size:
                if board[row + 1][col + 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row + 1 < size and col - 1 > 0:
                if board[row + 1][col - 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row - 1 > 0 and col - 1 > 0:
                if board[row - 1][col - 1] != EMPTY_SPACE:
                    return False
            else:
                return False
            if row - 1 > 0 and col + 1 < size:
                if board[row - 1][col + 1] != EMPTY_SPACE:
                    return False
            else:
                return False
        return True

    def perform_action(self, action, state):
        old_queen, new_queen, arrow = translating_move(action)
        queens = state[1]
        if queens[0].get_color().upper() == "WHITE":
            color = WHITE_QUEEN
            player = "white"
        else:
            color = BLACK_QUEEN
            player = "black"
        board_state = state[0]
        for queen in queens:
            if old_queen == queen.get_position():
                queen.set_new_position(new_queen)
                board_state[old_queen[0]][old_queen[1]] = EMPTY_SPACE
                board_state[new_queen[0]][new_queen[1]] = color
                board_state[arrow[0]][arrow[1]] = ARROW_SPACE
                break
        newstate = [board_state, queens, state[2], player, state[4]]
        return newstate

    def reward(self, state):
        return random.randint(0, 1)

