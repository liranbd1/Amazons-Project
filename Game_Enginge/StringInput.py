"""Translating strings back to actual moves and backwards"""
letters_dictionary = {}


def set_letters_dictionary(dictionary):
    global letters_dictionary
    letters_dictionary = dictionary


def translating_move(move_input):
    queen = move_input.split("-")
    arrow = move_input.split("/")
    current_queen_position = translate_position(queen[0])
    new_queen_position = queen[1].split("/")
    new_queen_position = translate_position(new_queen_position[0])
    arrow_position = translate_position(arrow[1])
    return current_queen_position, new_queen_position, arrow_position


def translate_position(position):
    px = letters_dictionary.get(position[0].upper())
    if len(position) == 3:
        py = 9
    else:
        py = int(position[1]) - 1
    return [px, py]


def translate_cordinate(current_position, new_position, arrow_position):
    current_position_string = get_key(current_position[0]) + str(current_position[1] + 1)
    new_position_string = get_key(new_position[0]) + str(new_position[1] + 1)
    arrow_position_string = get_key(arrow_position[0]) + str(arrow_position[1] + 1)
    output_string = (
        current_position_string + "-" + new_position_string + "/" + arrow_position_string
    )
    return output_string


def get_key(value):
    for key, val in letters_dictionary.items():
        if value == val:
            return key


def move_output(move, evaluation, time):
    return str(move) + "/" + str(evaluation) + "/" + str(time)


def print_extra_data_AB(depth, pruning_data, hash_access_number):
    print("Depth searched: {0}".format(depth))
    print("Number of cutoffs: {0}".format(pruning_data))
    print("Hash accessed: {0} times".format(hash_access_number))


def print_extra_data_MCTS(depth, simulations):
    print("Amount of simulation: {0}".format(simulations))
    print("Depth reached: {0}".format(depth))
