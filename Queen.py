class Queen:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def GetPosition(self):
        return [self.position[0], self.position[1]]

    def GetColor(self):
        return self.color

    def CornerCheckUp(self, point1, point2, point3):
        if (point1 == " x ") and (point2 == " x ") and (point3 == " x "):
            return False

        elif (point1 != " . ") and (point2 != " . ") and (point3 != " . "):
            return False

        else:
            return True

    def WallCheckUp(self, frontRowPoints, sidePoints):
        if (
                (frontRowPoints[0] == " x ")
                and (frontRowPoints[1] == " x ")
                and (frontRowPoints[2] == " x ")
                and (sidePoints[0] == " x ")
                and (sidePoints[1] == " x ")
        ):
            return False

        elif (
                (frontRowPoints[0] != " . ")
                and (frontRowPoints[1] != " . ")
                and (frontRowPoints[2] != " . ")
                and (sidePoints[0] != " . ")
                and (sidePoints[1] != " . ")
        ):
            return False

        else:
            return True

    def IsQueenFree(self, board, size):
        px = int(self.position[0])
        py = int(self.position[1])
        size = int(size) - 1

        # Corners
        # Assume queen is in top left corner
        # Bottom spot
        if px == py == 0:
            # Right spot
            rightPoint = board[px][py + 1]
            # Bottom spot
            bottomPoint = board[px + 1][py]
            # Diagonal spot
            diagonalPoint = board[px + 1][py + 1]
            return self.CornerCheckUp(rightPoint, bottomPoint, diagonalPoint)

        # Assume queen is in bottom right corner
        elif px == py == size:
            # Top spot
            topPoint = board[px - 1][py]
            # Left spot
            leftPoint = board[px][py - 1]
            # Diagonal spot
            diagonalPoint = board[px - 1][py - 1]
            return self.CornerCheckUp(topPoint, leftPoint, diagonalPoint)

        # Assume queen is in top right corner
        elif (px == 0) and (py == size):
            # Left spot
            leftPoint = board[px][py - 1]
            bottomPoint = board[px + 1][py]
            # Diagonal spot
            diagonalPoint = board[px + 1][py - 1]
            return self.CornerCheckUp(leftPoint, bottomPoint, diagonalPoint)

        # Assume queen is in bottom left corner
        elif (px == size) and (py == 0):
            # Top spot
            topPoint = board[px - 1][py]
            # Right spot
            rightPoint = board[px][py + 1]
            # Diagonal spot
            diagonalPoint = board[px - 1][py + 1]
            return self.CornerCheckUp(topPoint, rightPoint, diagonalPoint)

        # Walls
        # Next to top wall
        elif px == 0:
            # Front row
            frontRowPoints = [board[1][py - 1], board[1][py], board[1][py + 1]]
            # Sides points
            sidePoints = [board[px][py - 1], board[px][py + 1]]
            return self.WallCheckUp(frontRowPoints, sidePoints)

        # Next to bottom wall
        elif px == size:
            # Front row
            frontRowPoints = [
                board[size - 1][py - 1],
                board[size - 1][py],
                board[size - 1][py + 1],
            ]
            # Sides points
            sidePoints = [board[px][py - 1], board[px][py + 1]]
            return self.WallCheckUp(frontRowPoints, sidePoints)

        # Next to left wall
        elif py == 0:
            # Front row
            frontRowPoints = [board[px - 1][1], board[px][1], board[px + 1][1]]
            # Sides points
            sidePoints = [board[px + 1][py], board[px - 1][py]]
            return self.WallCheckUp(frontRowPoints, sidePoints)

        # Next to right wall
        elif py == size:
            # Front row
            frontRowPoints = [
                board[px - 1][size - 1],
                board[px][size - 1],
                board[px + 1][size - 1],
            ]
            # Side points
            sidePoints = [board[px + 1][py], board[px - 1][py]]
            return self.WallCheckUp(frontRowPoints, sidePoints)

        # In a middle space
        else:
            arrowCount = 0
            positionNextToQueen = [
                # Front
                board[px - 1][py - 1],
                board[px - 1][py],
                board[px - 1][py + 1],
                # Back
                board[px + 1][py - 1],
                board[px + 1][py],
                board[px + 1][py + 1],
                # Sides
                board[px][py - 1],
                board[px][py + 1],
            ]

            for position in positionNextToQueen:
                if position == " . ":
                    return True

            return False

    def SetNewPosition(self, position):
        self.position = position
