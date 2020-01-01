import treelib
from AI import treeNode

MINVALUE = -1000
MAXVALUE = 1000


class gameTree(treelib):
    # constructor
    def __init__(self, _root):
        self.create_node("root", _root)
        self.depth = 0
        self.evaluation = 0
        super().__init__()

    # Here we will define the alphabeta algorithm. we will search recursively true the children of a
    # given node, and stop search in the sub tree if alphabeta condition is apply
    def alphaBetaPrun(self, node, nodeDepth, alpha, beta, isMaxPlayer):
        # first we will check if it is a root or a leaf node
        if nodeDepth == 0 or self.is_branch(node) is None:
            return node.getValue()
        if isMaxPlayer:
            tempVal = -10000
            for children in self.tree.is_branch(
                node
            ):  # here we will check for every children if it should be pruned
                tempVal = max(
                    tempVal,
                    self.alphaBetaPrun(children, nodeDepth - 1, alpha, beta, True),
                )
                alpha = max(alpha, tempVal)
                if (
                    beta <= alpha
                ):  # if beta <= alpha we will make a cut of because min will not choose him
                    break
                node.setValue(tempVal)
                return
        else:  # if its min turn
            tempVal = 1000
            for children in self.is_branch(
                node
            ):  # here we will check for every children if it should be pruned
                tempVal = min(
                    tempVal,
                    self.alphaBetaPrun(children, nodeDepth - 1, alpha, beta, True),
                )
                beta = min(beta, tempVal)
                if (
                    beta <= alpha
                ):  # if beta <= alpha we will make a cut of because max will not choose him
                    break
                node.setValue(tempVal)
                return
        return

    # starting alphabeta inside the tree to make some cutoffs
    def startAlphaBeta(self):
        evaluation = 0
        depth = self.depth
        self.alphaBetaPrun(self.root, depth, MINVALUE, MAXVALUE, True)

    def getBestMove(self):
        max = MINVALUE
        best = None

    # here is the function to make a move
    def makeMove(self):
        self.startAlphaBeta()
        bestMove = self.getBestMove()
