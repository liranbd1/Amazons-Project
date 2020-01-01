from Constants import EMPTY_SPACE


def CheckStraightMovement(bigger, smaller, constant, direction, boardMatrix):
    delta = bigger - smaller
    symbol = ""
    for i in range(delta):
        if i == 0:
            continue
        if direction == "Down":
            symbol = boardMatrix[smaller + i][constant]
        elif direction == "Up":
            symbol = boardMatrix[bigger - i][constant]
        elif direction == "Right":
            symbol = boardMatrix[constant][smaller + i]
        elif direction == "Left":
            symbol = boardMatrix[constant][bigger - i]
        if symbol != EMPTY_SPACE:
          #  print("We got {0} in the way".format(symbol))
            return False
    # print("Move accepted")
    return True


def CheckDiagonalMovement(cPx, cPy, delta, direction, boardMatrix):
    symbol = ""
    for i in range(delta):
        if i == 0:
            continue
        elif direction == "Up-Left":
            symbol = boardMatrix[cPx - i][cPy - i]
        elif direction == "Down-Right":
            symbol = boardMatrix[cPx + i][cPy + i]
        elif direction == "Up-Right":
            symbol = boardMatrix[cPx - i][cPy + i]
        elif direction == "Down-Left":
            symbol = boardMatrix[cPx + i][cPy - i]
        if symbol != EMPTY_SPACE:
      #      print("We got {0} in the way".format(symbol))
            return False
    # print("Move accepted")
    return True


def IsMoveLegal(currentPosition, newPosition, boardSize, boardMatrix):

    # Check if new position is in the board
    if (
        newPosition[0] > int(boardSize) - 1
        or newPosition[0] < 0
        or newPosition[1] > int(boardSize) - 1
        or newPosition[1] < 0
    ):
      #  print("Please choose a position in the board")
        return False

    # Check if the new position is free (Also includes the check that the queen is not moving in place)
    if boardMatrix[newPosition[0]][newPosition[1]] != EMPTY_SPACE:
     #   print("Please enter a valid position for the queen")
        return False

    # Check if the move is possible by this queen (Moving like a queen not a horse)
    cPx, cPy = currentPosition
    nPx, nPy = newPosition
    # Check Up and Down (moving on the letters)
    if cPy == nPy and cPx != nPx:
        # Going down
        if nPx > cPx:
            return CheckStraightMovement(nPx, cPx, cPy, "Down", boardMatrix)

        # Going up
        else:
            return CheckStraightMovement(cPx, nPx, cPy, "Up", boardMatrix)

    # Check Left or Right (moving on the numbers)
    if cPx == nPx and cPy != nPy:
        # Going right
        if nPy > cPy:
            return CheckStraightMovement(nPy, cPy, cPx, "Right", boardMatrix)

        # Going left
        else:
            return CheckStraightMovement(cPy, nPy, cPx, "Left", boardMatrix)

    # Check diagonals (We got four diagonals to check [up-left, up-right, down-left, down-right]
    deltaX = cPx - nPx
    deltaY = cPy - nPy
    if abs(deltaX) != abs(deltaY):
      #  print("You can only move like a queen")
        return False

    # Up-Left
    if deltaX == deltaY > 0:
        return CheckDiagonalMovement(cPx, cPy, deltaX, "Up-Left", boardMatrix)

    # Down-Right
    elif deltaX == deltaY < 0:
        return CheckDiagonalMovement(cPx, cPy, deltaY, "Down-Right", boardMatrix)

    else:
        # Up-Right
        if deltaX > 0:
            return CheckDiagonalMovement(cPx, cPy, deltaX, "Up-Right", boardMatrix)
        # Down-Left
        if deltaY > 0:
            return CheckDiagonalMovement(cPx, cPy, deltaY, "Down-Left", boardMatrix)
