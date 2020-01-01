from Constants import *
import time
from Queen import *
import StringInput as SI
import Rules
from LiranAITest.AlphaBetaPruning import start_alpha_beta
import copy
from LiranAITest.ZorbistHashing import init_zobrist_table
# Variables to create the board initial state
boardSize = 0
# (y,x)
boardMatrix = []
whiteQueensSetup = []
blackQueensSetup = []
arrowsPosition = []
aiTime = 0
playerTurn = ["White", "Black"]
players = [["", playerTurn[0]], ["", playerTurn[1]]]


def SetBoardSize():
    global boardSize
    while True:
        size = input("Please enter size, 10 or 6: ")
        if (int(size) == 10) or (int(size) == 6):
            boardSize = size
            if int(boardSize) == 10:
                SI.SetLettersDictionary(LETTERS_DICTIONARY_10)
            elif int(boardSize) == 6:
                SI.SetLettersDictionary(LETTERS_DICTIONARY_06)
            break

        print("Please enter a valid size")


def CreateBoardMatrix():
    global boardMatrix
    boardMatrix = [
        [EMPTY_SPACE for x in range(int(boardSize))] for y in range(int(boardSize))
    ]


def SetupBoard():
    QueenPositionsSetup()
    for wq in whiteQueensSetup:
        position = wq.GetPosition()
        boardMatrix[int(position[0])][int(position[1])] = WHITE_QUEEN

    for bq in blackQueensSetup:
        position = bq.GetPosition()
        boardMatrix[int(position[0])][int(position[1])] = BLACK_QUEEN


def QueenPositionsSetup():
    global whiteQueensSetup
    global blackQueensSetup

    if int(boardSize) == 10:
        for i in range(4):
            whiteQueenPosition = WHITE_QUEENS_START_10[i]
            whiteQueenToAdd = Queen(
                [whiteQueenPosition[0], whiteQueenPosition[1]], "White"
            )
            whiteQueensSetup.insert(i, whiteQueenToAdd)
            blackQueenPosition = BLACK_QUEENS_START_10[i]
            blackQueenToAdd = Queen(
                [blackQueenPosition[0], blackQueenPosition[1]], "Black"
            )
            blackQueensSetup.insert(i, blackQueenToAdd)
    else:
        for i in range(2):
            whiteQueenPosition = WHITE_QUEENS_START_06[i]
            whiteQueenToAdd = Queen(
                [whiteQueenPosition[0], whiteQueenPosition[1]], "White"
            )
            whiteQueensSetup.insert(i, whiteQueenToAdd)
            blackQueenPosition = BLACK_QUEENS_START_06[i]
            blackQueenToAdd = Queen(
                [blackQueenPosition[0], blackQueenPosition[1]], "Black"
            )
            blackQueensSetup.insert(i, blackQueenToAdd)


def PlayerMove(player):
    global arrowsPosition
    if player == "White":
        queenToDraw = WHITE_QUEEN
    else:
        queenToDraw = BLACK_QUEEN
    while True:
        moveInput = input("Please enter a move")  # According to the rules QM-WTM/AP
        currentPosition, newPosition, arrowPosition = SI.TranslatingMove(moveInput)
       # print(currentPosition, newPosition, arrowPosition)
        queenToMove = FindQueen(currentPosition, player)
        # Check if queen is chosen
        if queenToMove == "No legal queen":
            print("Please choose a queen")
        # Check if queen is free
        elif not queenToMove.IsQueenFree(boardMatrix, boardSize):
            print("Queen is not free")
        # Queen move is legal
        elif Rules.IsMoveLegal(currentPosition, newPosition, boardSize, boardMatrix):
            boardMatrix[currentPosition[0]][currentPosition[1]] = EMPTY_SPACE
            if Rules.IsMoveLegal(newPosition, arrowPosition, boardSize, boardMatrix):
                boardMatrix[newPosition[0]][newPosition[1]] = queenToDraw
                queenToMove.SetNewPosition(newPosition)
                boardMatrix[arrowPosition[0]][arrowPosition[1]] = ARROW_SPACE
                arrowsPosition.append(arrowPosition)
                break
            else:
                boardMatrix[currentPosition[0]][currentPosition[1]] = queenToDraw
        else:
            print("Move not legal")
    PrintBoard()


def FindQueen(currentPosition, player):
    px, py = currentPosition
    if player == "White":
        for queen in whiteQueensSetup:
            qpx, qpy = queen.GetPosition()
            if qpx == px and qpy == py:
                return queen

    elif player == "Black":
        for queen in blackQueensSetup:
            qpx, qpy = queen.GetPosition()
            if qpx == px and qpy == py:
                return queen

    return "No legal queen"


def PrintBoard():
    i = int(boardSize) - 1
    for line in boardMatrix:
        print(LETTERS[i], end="")
        print(line)
        i -= 1

    for i in range(int(boardSize)):
        print("   {0}   ".format(i + 1), end="")
    print()


def SetTimer():
    global aiTime
    aiTime = input("Please enter timer for each player in minutes: ")
    aiTime = float(aiTime) * 60  # Converting to seconds


def AIMove(currentPosition, newPosition, ArrowPosition, color):
    if color == "White":
        queen = WHITE_QUEEN
    else:
        queen = BLACK_QUEEN
    queenToMove = FindQueen(currentPosition, color)
    boardMatrix[currentPosition[0]][currentPosition[1]] = EMPTY_SPACE
    boardMatrix[newPosition[0]][newPosition[1]] = queen
    queenToMove.SetNewPosition(newPosition)
    boardMatrix[ArrowPosition[0]][ArrowPosition[1]] = ARROW_SPACE
    arrowsPosition.append(ArrowPosition)


def IsGameEnded(player):
    if player == "White":
        queenSetup = whiteQueensSetup
    else:
        queenSetup = blackQueensSetup

    for queen in queenSetup:
        if queen.IsQueenFree(boardMatrix, boardSize):
            return False
    return True


def SetGameMode():
    while True:
        gameMode = input("PvE or EvE? ")
        if gameMode.upper() == "PVE":
            WhoStarts()
            break
        elif gameMode.upper() == "EVE":
            players[0][0] = "AI"
            players[1][0] = "AI"
            break
        elif gameMode.upper() == "PVP":
            players[0][0] = "Human"
            players[1][0] = "Human"
            break
        else:
            print("Please enter a valid input")


def WhoStarts():
    while True:
        colorOfChoice = input(
            "Please choose your color, white or black(white starts): "
        )
        if colorOfChoice.upper() == "WHITE":
            players[0][0] = "Human"
            players[1][0] = "AI"
            break
        elif colorOfChoice.upper() == "BLACK":
            players[0][0] = "AI"
            players[1][0] = "Human"
            break
        else:
            print("Please enter a valid input")


def InitialBoardSetup():
    SetBoardSize()
    CreateBoardMatrix()
    SetupBoard()
    SetGameMode()
    SetTimer()
    PrintBoard()
    init_zobrist_table(boardSize)


InitialBoardSetup()
i = 0
while True:
    print(playerTurn[i])
    if IsGameEnded(playerTurn[i]):
        print("{0} has won!!!!".format(playerTurn[(i + 1) % 2]))
        break
    if players[i][0].upper() == "HUMAN":
        PlayerMove(playerTurn[i])

    elif players[i][0].upper() == "AI":
        startingTime = time.time()
        if players[i][1].upper() == "WHITE":
            move = start_alpha_beta(copy.deepcopy(boardMatrix), 1, boardSize, copy.deepcopy(whiteQueensSetup),
                                    copy.deepcopy(blackQueensSetup))
        else:
            move = start_alpha_beta(copy.deepcopy(boardMatrix), 1, boardSize, copy.deepcopy(blackQueensSetup),
                                    copy.deepcopy(whiteQueensSetup))
        current_queen_position, new_queen_position, arrow_position = move
        AIMove(current_queen_position, new_queen_position, arrow_position, players[i][1])
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
        elapsedTime = (
            time.time() - startingTime
        )  # This should give me how much time has passed in seconds for the
        # whole turn
        aiTime -= elapsedTime
        PrintBoard()
        print(SI.MoveOutput(move_string, 1, elapsedTime))
        ## UNCOMMENT THIS--- print(SI.MoveOutput(MoveString, evaluation, elapsedTime))
        # Here we need to print another technical data (What we got from our function)
        ## UNCOMMENT THIS--- SI.PrintExtraData(depth, PV, PVEvaluation, pruningData, hashAccessNumbers)

        if aiTime <= 0:
            print("AI time has ended, {0} win!!!".format(players[i][1]))
            break

    i = (i + 1) % 2

# Change
