import numpy as np
from game_constants import *

ACTION_SET_TILE = "ACTION_SET_TILE"


def action_handler(global_update_callback, player, game_state, action, **args):
    print("Player " + str(player) + " wants action: " + action)

    # print(game_state)

    if action == ACTION_SET_TILE:
        tile = TILES[23]
        game_state[player][0][args["gy"], args["gx"]] = tile[0]
        game_state[player][0][args["gy"], args["gx"] + 1] = tile[1]
    else:
        raise Exception("Unsupported Action: " + action)

    # print(game_state)

    # trigger global update
    global_update_callback()


def action_player_injector(global_update_callback, player, game_state):
    return lambda action, **args: action_handler(
        global_update_callback, player, game_state, action, **args
    )


def game_description(player_index, game_state):
    player_game_board_bioms = game_state[player_index][0]
    tiles_placed = np.count_nonzero(player_game_board_bioms) // 2

    description_string = "Placed: " + str(tiles_placed) + "\n\n"

    description_string += "Own Dragons/Own Shells: \n"
    dragons, eggs = calc_own_scores(player_index, game_state)
    description_string += str(dragons) + "/" + str(eggs) + "\n\n"

    description_string += "Dg Left/Eggs -> Chance\n"
    egg_count = calc_eggs_opened(game_state)
    for biom in BIOMS:
        nr_dragons = egg_count[biom]
        nr_empty_eggs = egg_count[biom + EMPTY_SHELL]
        nr_dragons_left = NR_DRAGONS_IN_EGGS[biom] - nr_dragons
        nr_eggs_left = NR_TOTAL_EGGS[biom] - nr_dragons - nr_empty_eggs

        description_string += (
            BIOM_NAMES[biom]
            + ": "
            + str(nr_dragons_left)
            + "/"
            + str(nr_eggs_left)
            + "->"
            + str(int(nr_dragons_left / nr_eggs_left * 100))
            + "%\n"
        )

    return description_string


def calc_eggs_opened(game_state):
    eggs = [0] * (2 * EMPTY_SHELL)

    for i in range(PLAYER_COUNT):
        player_game_board_eggs = game_state[i][1]

        eggs += np.bincount(player_game_board_eggs.flatten(), minlength=2 * EMPTY_SHELL)

    return eggs


def calc_own_scores(player_index, game_state):
    player_game_board_eggs = game_state[player_index][1]

    info = np.bincount(player_game_board_eggs.flatten(), minlength=2 * EMPTY_SHELL)

    eggs = 0
    shells = 0
    for biom in BIOMS:
        eggs += info[biom]
        shells += info[biom + EMPTY_SHELL]

    return eggs, shells
