import numpy as np
from array_helpers import in_array
from board_helpers import (
    BIOM_INDEX,
    BIOM_INDEX_PREVIEW,
    EGG_INDEX,
    SECOND_TILE_TURN_INDEX,
    SELECTED_TILE_INDEX,
    USED_TILE_INDEX,
    clear_previews,
)
from game_constants import *

ACTION_SET_TILE = "ACTION_SET_TILE"
ACTION_PICK_TILE = "ACTION_PICK_TILE"
ACTION_TURN_TILE = "ACTION_TURN_TILE"
ACTION_PREVIEW_TILE = "ACTION_PREVIEW_TILE"
ACTION_TOGGLE_EGGS = "ACTION_TOGGLE_EGGS"


def action_handler(global_update_callback, player, game_state, action, **args):
    if action is not ACTION_PREVIEW_TILE:  # reduce spam
        print("Player " + str(player) + " wants action: " + action)

    # !set tile
    if action == ACTION_SET_TILE:
        if len(game_state[PLAYER_COUNT][SELECTED_TILE_INDEX]) > 0:
            if not fits_on_board(
                GRID_SIZE,
                args["gx"],
                args["gy"],
                game_state[player][SECOND_TILE_TURN_INDEX][1],
                game_state[player][SECOND_TILE_TURN_INDEX][0],
            ) or board_obstructed(
                game_state[player][BIOM_INDEX],
                args["gx"],
                args["gy"],
                game_state[player][SECOND_TILE_TURN_INDEX][1],
                game_state[player][SECOND_TILE_TURN_INDEX][0],
            ):
                print("placement doesn't fit")
            else:
                tile = TILES[game_state[PLAYER_COUNT][SELECTED_TILE_INDEX].pop(0)]

                game_state[player][BIOM_INDEX][args["gy"], args["gx"]] = tile[
                    TILE_INDEX_FIRST
                ]
                game_state[player][BIOM_INDEX][
                    args["gy"] + game_state[player][SECOND_TILE_TURN_INDEX][0],
                    args["gx"] + game_state[player][SECOND_TILE_TURN_INDEX][1],
                ] = tile[TILE_INDEX_SECOND]

                game_state[PLAYER_COUNT][USED_TILE_INDEX].append(tile[TILE_INDEX_INDEX])

                clear_previews(game_state)  # clear preview after placing
        else:
            print("no tile selected")

    # !pick tile
    if action == ACTION_PICK_TILE:
        if in_array(game_state[PLAYER_COUNT][SELECTED_TILE_INDEX], args["tile_index"]):
            game_state[PLAYER_COUNT][SELECTED_TILE_INDEX].remove(args["tile_index"])
        else:
            if in_array(game_state[PLAYER_COUNT][USED_TILE_INDEX], args["tile_index"]):
                print("tile already used up")
            else:
                game_state[PLAYER_COUNT][SELECTED_TILE_INDEX].append(args["tile_index"])

    # !turn tile
    if action == ACTION_TURN_TILE:
        if (
            game_state[player][SECOND_TILE_TURN_INDEX][0] == 0
            and game_state[player][SECOND_TILE_TURN_INDEX][1] == 1
        ):
            game_state[player][SECOND_TILE_TURN_INDEX] = [1, 0]
        elif (
            game_state[player][SECOND_TILE_TURN_INDEX][0] == 1
            and game_state[player][SECOND_TILE_TURN_INDEX][1] == 0
        ):
            game_state[player][SECOND_TILE_TURN_INDEX] = [0, -1]
        elif (
            game_state[player][SECOND_TILE_TURN_INDEX][0] == 0
            and game_state[player][SECOND_TILE_TURN_INDEX][1] == -1
        ):
            game_state[player][SECOND_TILE_TURN_INDEX] = [-1, 0]
        elif (
            game_state[player][SECOND_TILE_TURN_INDEX][0] == -1
            and game_state[player][SECOND_TILE_TURN_INDEX][1] == 0
        ):
            game_state[player][SECOND_TILE_TURN_INDEX] = [0, 1]

    # !toggle dragon eggs
    if action == ACTION_TOGGLE_EGGS:
        # check if tile-types match
        type1 = game_state[player][BIOM_INDEX][args["t1y"], args["t1x"]] % SPRING
        type2 = game_state[player][BIOM_INDEX][args["t2y"], args["t2x"]] % SPRING
        if type1 != 0 and type1 == type2:
            if game_state[player][EGG_INDEX][args["ey"], args["ex"]] == 0:
                game_state[player][EGG_INDEX][args["ey"], args["ex"]] = type1
            elif game_state[player][EGG_INDEX][args["ey"], args["ex"]] < EMPTY_SHELL:
                game_state[player][EGG_INDEX][args["ey"], args["ex"]] = (
                    type1 + EMPTY_SHELL
                )
            else:
                game_state[player][EGG_INDEX][args["ey"], args["ex"]] = 0
        else:
            print("criteria for egg toggeling not met")

    # !preview tile, also updates after turning and not moving
    if action == ACTION_PREVIEW_TILE or action == ACTION_TURN_TILE:
        if len(game_state[PLAYER_COUNT][SELECTED_TILE_INDEX]) > 0:
            if not fits_on_board(
                GRID_SIZE,
                args["gx"],
                args["gy"],
                game_state[player][SECOND_TILE_TURN_INDEX][1],
                game_state[player][SECOND_TILE_TURN_INDEX][0],
            ):
                print("preview doesn't fit")
            else:
                tile = TILES[game_state[PLAYER_COUNT][SELECTED_TILE_INDEX][0]]

                clear_previews(game_state)  # clear than overwrite

                game_state[player][BIOM_INDEX_PREVIEW][args["gy"], args["gx"]] = tile[
                    TILE_INDEX_FIRST
                ]
                game_state[player][BIOM_INDEX_PREVIEW][
                    args["gy"] + game_state[player][SECOND_TILE_TURN_INDEX][0],
                    args["gx"] + game_state[player][SECOND_TILE_TURN_INDEX][1],
                ] = tile[TILE_INDEX_SECOND]

    # trigger global update
    global_update_callback()


def action_player_injector(global_update_callback, player, game_state):
    return lambda action, **args: action_handler(
        global_update_callback, player, game_state, action, **args
    )


def action_injector(global_update_callback, game_state):
    return lambda action, **args: action_handler(
        global_update_callback, -1, game_state, action, **args
    )


def game_description(player_index, game_state):
    player_game_board_bioms = game_state[player_index][BIOM_INDEX]
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
        player_game_board_eggs = game_state[i][EGG_INDEX]

        eggs += np.bincount(player_game_board_eggs.flatten(), minlength=2 * EMPTY_SHELL)

    return eggs


def calc_own_scores(player_index, game_state):
    player_game_board_eggs = game_state[player_index][EGG_INDEX]

    info = np.bincount(player_game_board_eggs.flatten(), minlength=2 * EMPTY_SHELL)

    eggs = 0
    shells = 0
    for biom in BIOMS:
        eggs += info[biom]
        shells += info[biom + EMPTY_SHELL]

    return eggs, shells


def fits_on_board(size, index_x, index_y, offset_index_x, offset_index_y):
    if size <= 0:
        return False

    if index_x < 0 or index_x >= size:
        return False

    if index_y < 0 or index_y >= size:
        return False

    if index_x + offset_index_x < 0 or index_x + offset_index_x >= size:
        return False

    if index_y + offset_index_y < 0 or index_y + offset_index_y >= size:
        return False

    return True


def board_obstructed(board_array, index_x, index_y, offset_index_x, offset_index_y):
    return (
        board_array[index_y, index_x] != 0
        or board_array[index_y + offset_index_y, index_x + offset_index_x] != 0
    )


def tile_is_being_placed(game_board_state):
    return len(game_board_state[PLAYER_COUNT][SELECTED_TILE_INDEX]) > 0
