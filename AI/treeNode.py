# here we will make a node
# we want every node to have few important properties:
# queen - which queen is in the node (if it is not empty)
# arrow - if there is an arrow in the node
# heuristicValue - the heuristic value of the node
# rules - object that storing the game current state by 'board.py'
# IsMoveLegal


class treeNode:
    def __init__(self, _queen, _arrow, _heuristicValue, _board):
        self.queen = _queen
        self.arrow = _arrow
        self.heuristicValue = _heuristicValue
        self.board = _board
        super().__init__()

    def getQueen(self):
        return self.queen

    def getArrow(self):
        return self.arrow

    def getValue(self):
        return self.heuristicValue

    def setValue(self, newH):
        self.heuristicValue = newH

    # here we will return all the legal states to a given one, represented by nodes
    # xQueen, yQueen, xArrow, yArrow
    # queen.GetPosition returning coordinates

    def findLegalArrows(self, origX, origY, x, y):
        queenMoves = []
        # right
        for i in range(1, 10):
            if y + i > 9:
                break
            elif self.board.matrix[x][y + i].state == ".":
                queenMoves.append([origX, origY, x, y + i])
            else:
                break

        # left
        for i in range(1, 10):
            if y - i < 0:
                break
            elif self.board.matrix[x][y - i].state == ".":
                queenMoves.append([origX, origY, x, y - i])
            else:
                break

        # down
        for i in range(1, 10):
            if x + i > 9:
                break
            elif self.board.matrix[x + i][y].state == ".":
                queenMoves.append([origX, origY, x + i, y])
            else:
                break

        # top
        for i in range(1, 10):
            if x - i < 0:
                break
            elif self.board.matrix[x - i][y].state == ".":
                queenMoves.append([origX, origY, x - i, y])
            else:
                break

        # topleft
        for i in range(1, 10):
            if x - i < 0 or y - i < 0:
                break
            elif self.board.matrix[x - i][y - i].state == ".":
                queenMoves.append([origX, origY, x - i, y - i])
            else:
                break

        # downleft
        for i in range(1, 10):
            if x + i > 9 or y - i < 0:
                break
            elif self.board.matrix[x + i][y - i].state == ".":
                queenMoves.append([origX, origY, x + i, y - i])
            else:
                break

        # topright
        for i in range(1, 10):
            if x - i < 0 or y + i > 9:
                break
            elif self.board.matrix[x - i][y + i].state == ".":
                queenMoves.append([origX, origY, x - i, y + i])
            else:
                break

        # downright
        for i in range(1, 10):
            if x + i > 9 or y + i > 9:
                break
            elif self.board.matrix[x + i][y + i].state == ".":
                queenMoves.append([origX, origY, x + i, y + i])
            else:
                break
        return queenMoves

    def getSuccesors(self):
        successors = []
        for queen in queens:
            queenMoves = []
            [x, y] = queen.GetPosition
        # right
        for i in range(1, 10):
            if y + i > 9:
                break
            elif self.board.matrix[x][y + i].state == ".":
                self.findLegalArrows(x, y + i, x, y + i)
            else:
                break

        # left
        for i in range(1, 10):
            if y - i < 0:
                break
            elif self.board.matrix[x][y - i].state == ".":
                self.findLegalArrows(x, y - i, x, y - i)
            else:
                break

        # down
        for i in range(1, 10):
            if x + i > 9:
                break
            elif self.board.matrix[x + i][y].state == ".":
                self.findLegalArrows(x + i, y, x + i, y)
            else:
                break

        # top
        for i in range(1, 10):
            if x - i < 0:
                break
            elif self.board.matrix[x - i][y].state == ".":
                self.findLegalArrows(x - i, y, x - i, y)
            else:
                break

        # topleft
        for i in range(1, 10):
            if x - i < 0 or y - i < 0:
                break
            elif self.board.matrix[x - i][y - i].state == ".":
                self.findLegalArrows(x - i, y - i, x - i, y - i)
            else:
                break

        # downleft
        for i in range(1, 10):
            if x + i > 9 or y - i < 0:
                break
            elif self.board.matrix[x + i][y - i].state == ".":
                self.findLegalArrows(x + i, y - i, x + i, y - i)
            else:
                break

        # topright
        for i in range(1, 10):
            if x - i < 0 or y + i > 9:
                break
            elif self.board.matrix[x - i][y + i].state == ".":
                self.findLegalArrows(x - i, y + i, x - i, y + i)
            else:
                break

        # downright
        for i in range(1, 10):
            if x + i > 9 or y + i > 9:
                break
            elif self.board.matrix[x + i][y + i].state == ".":
                self.findLegalArrows(x + i, y + i, x + i, y + i)
            else:
                break
