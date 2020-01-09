letters_dictionary = {}


def SetLettersDictionary(dictionary):
    global letters_dictionary
    letters_dictionary = dictionary


def TranslatingMove(moveInput):
    queen = moveInput.split("-")
    arrow = moveInput.split("/")
    currentQueenPosition = TranslatePosition(queen[0])
    newQueenPosition = queen[1].split("/")
    newQueenPosition = TranslatePosition(newQueenPosition[0])
    arrowPosition = TranslatePosition(arrow[1])
    return currentQueenPosition, newQueenPosition, arrowPosition


def TranslatePosition(position):
    px = letters_dictionary.get(position[0].upper())
    if len(position) == 3:
        py = 9
    else:
        py = int(position[1]) - 1
    return [px, py]


def TranslateCordinates(currentPosition, newPosition, ArrowPosition):
    currentPositionString = GetKey(currentPosition[0]) + str(currentPosition[1]+1)
    newPositionString = GetKey(newPosition[0]) + str(newPosition[1]+1)
    arrowPositionString = GetKey(ArrowPosition[0]) + str(ArrowPosition[1]+1)
    outputString = (
        currentPositionString + "-" + newPositionString + "/" + arrowPositionString
    )
    return outputString


def GetKey(value):
    for key, val in letters_dictionary.items():
        if value == val:
            return key


def MoveOutput(move, evaluation, time):
    return str(move) + "/" + str(evaluation) + "/" + str(time)


def PrintExtraData(depth, PV, PVEvaluation, pruningData, hashAccessNumbers):
    print("Depth searched: {0}".format(depth))
    print("Main PV: {0}".format(PV))
    print("PV evaluation: {0}".format(PVEvaluation))
    print("Cutoff data(?): {0}".format(pruningData))
    print("Hash accessed: {0} times".format(hashAccessNumbers))
