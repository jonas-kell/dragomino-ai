import numpy as np
from array_helpers import in_array
from board_helpers import (
    BIOM_INDEX,
    BIOM_INDEX_PREDICTION,
    BIOM_INDEX_PREVIEW,
    EGG_INDEX,
    SECOND_TILE_TURN_INDEX,
    SELECTED_TILE_INDEX,
    TURNING_OFFSETS,
    USED_TILE_INDEX,
    clear_predictions,
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
                update_predictions(game_state)  # update predictions after placing
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

        update_predictions(game_state)  # update predictions after selection change

    # !turn tile
    if action == ACTION_TURN_TILE:
        if game_state[player][SECOND_TILE_TURN_INDEX] == TURNING_OFFSETS[0]:
            game_state[player][SECOND_TILE_TURN_INDEX] = TURNING_OFFSETS[1]
        elif game_state[player][SECOND_TILE_TURN_INDEX] == TURNING_OFFSETS[1]:
            game_state[player][SECOND_TILE_TURN_INDEX] = TURNING_OFFSETS[2]
        elif game_state[player][SECOND_TILE_TURN_INDEX] == TURNING_OFFSETS[2]:
            game_state[player][SECOND_TILE_TURN_INDEX] = TURNING_OFFSETS[3]
        elif game_state[player][SECOND_TILE_TURN_INDEX] == TURNING_OFFSETS[3]:
            game_state[player][SECOND_TILE_TURN_INDEX] = TURNING_OFFSETS[0]

    # !toggle dragon eggs
    if action == ACTION_TOGGLE_EGGS:
        # check if fits on board
        if index_on_board(args["t1x"], args["t1y"]) and index_on_board(
            args["t2x"], args["t2y"]
        ):
            # check if tile-types match
            type1 = game_state[player][BIOM_INDEX][args["t1y"], args["t1x"]] % SPRING
            type2 = game_state[player][BIOM_INDEX][args["t2y"], args["t2x"]] % SPRING
            if type1 != 0 and type1 == type2:
                if game_state[player][EGG_INDEX][args["ey"], args["ex"]] == 0:
                    game_state[player][EGG_INDEX][args["ey"], args["ex"]] = type1
                elif (
                    game_state[player][EGG_INDEX][args["ey"], args["ex"]] < EMPTY_SHELL
                ):
                    game_state[player][EGG_INDEX][args["ey"], args["ex"]] = (
                        type1 + EMPTY_SHELL
                    )
                else:
                    game_state[player][EGG_INDEX][args["ey"], args["ex"]] = 0
            else:
                print("criteria for egg toggeling not met")
        else:
            print("egg toggeling out of bounds")

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
        global_update_callback, PLAYER_COUNT, game_state, action, **args
    )


def player_description(player_index, game_state):
    player_game_board_bioms = game_state[player_index][BIOM_INDEX]
    tiles_placed = np.count_nonzero(player_game_board_bioms) // 2

    description_string = "Placed: " + str(tiles_placed) + "\n\n"

    description_string += "Own Dragons/Own Shells: \n"
    dragons, eggs = calc_own_scores(player_index, game_state)
    description_string += str(dragons) + "/" + str(eggs) + "\n\n"

    description_string += "Dg Left/Eggs -> Chance\n"
    probabilities = calc_egg_probabilities(game_state)
    for biom_index in BIOMS:
        description_string += (
            BIOM_NAMES[biom_index]
            + ": "
            + str(probabilities[biom_index][PROB_INDEX_DRAGONS_LEFT])
            + "/"
            + str(probabilities[biom_index][PROB_INDEX_EGGS_UNOPENED])
            + "->"
            + str(int(probabilities[biom_index][PROB_INDEX_PROB] * 100))
            + "%\n"
        )

    return description_string


def main_description(game_state):
    description_string = "Pl. -> Dragons/Shells \n"

    for player in range(PLAYER_COUNT):
        dragons, eggs = calc_own_scores(player, game_state)
        description_string += (
            str(player) + " -> " + str(dragons) + "/" + str(eggs) + "\n"
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


PROB_INDEX_PROB = 0
PROB_INDEX_DRAGONS_GONE = 1
PROB_INDEX_EMPTY_SHELLS = 2
PROB_INDEX_DRAGONS_LEFT = 3
PROB_INDEX_EGGS_UNOPENED = 4


# array per biom-index: [p(Egg is dragon), #dragons_opened, #empty_shells, #dragons_left, #eggs_unopened]
def calc_egg_probabilities(game_state):
    results = [0] * EMPTY_SHELL

    egg_count = calc_eggs_opened(game_state)
    for biom_index in BIOMS:
        nr_dragons = egg_count[biom_index]
        nr_empty_shells = egg_count[biom_index + EMPTY_SHELL]
        nr_dragons_left = NR_DRAGONS_IN_EGGS[biom_index] - nr_dragons
        nr_eggs_unopened = NR_TOTAL_EGGS[biom_index] - nr_dragons - nr_empty_shells

        results[biom_index] = [
            nr_dragons_left / nr_eggs_unopened,
            nr_dragons,
            nr_empty_shells,
            nr_dragons_left,
            nr_eggs_unopened,
        ]

    return results


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


def update_predictions(game_board_state):
    print("update predictions")
    clear_predictions(game_board_state)

    if len(game_board_state[PLAYER_COUNT][SELECTED_TILE_INDEX]) == 0:
        print("no selection to predict from")
    else:
        # global statistics over egg probabilities
        egg_probabilities = calc_egg_probabilities(game_board_state)

        # iterate over players predictions
        for player_index in range(PLAYER_COUNT):
            # ! real prediction logic
            tile_1_x_best = -1
            tile_1_y_best = -1
            tile_1_biom_index_best = -1
            tile_2_x_best = -1
            tile_2_y_best = -1
            tile_2_biom_index_best = -1
            # ! measurement
            score = -1

            # for all possible positions, see if better placement
            for possible_tile in game_board_state[PLAYER_COUNT][SELECTED_TILE_INDEX]:
                for row in range(GRID_SIZE):
                    for col in range(GRID_SIZE):
                        # only if starting position is valid
                        if game_board_state[player_index][BIOM_INDEX][row, col] == 0:
                            # test all offsets, if there is an adjacent tile
                            adjacent = False
                            for offset in TURNING_OFFSETS:
                                if (
                                    index_on_board(row + offset[0], col + offset[1])
                                    and game_board_state[player_index][BIOM_INDEX][
                                        row + offset[0], col + offset[1]
                                    ]
                                    != 0
                                ):
                                    adjacent = True
                            # only continue if an adjacent tile is there
                            if adjacent:
                                # now only try to place on the empty squares
                                for offset in TURNING_OFFSETS:
                                    if (
                                        index_on_board(row + offset[0], col + offset[1])
                                        and game_board_state[player_index][BIOM_INDEX][
                                            row + offset[0], col + offset[1]
                                        ]
                                        == 0
                                    ):
                                        # compare usefulness of tile positions
                                        new_score = 0
                                        tile_1_x_current = col
                                        tile_1_y_current = row
                                        tile_2_x_current = (
                                            col + offset[1]
                                        )  # make sure surrounding_biome_pairs() calculate this the same
                                        tile_2_y_current = (
                                            row + offset[0]
                                        )  # make sure surrounding_biome_pairs() calculate this the same

                                        # biome_pair [biome_index_1, biome_index_2]
                                        for biome_pair in surrounding_biome_pairs(
                                            possible_tile,
                                            game_board_state[player_index][BIOM_INDEX],
                                            tile_1_y_current,
                                            tile_1_x_current,
                                            offset,
                                        ):
                                            # judge biom pair as score
                                            if (
                                                biome_pair[0] != 0
                                                and biome_pair[0] % SPRING
                                                == biome_pair[1] % SPRING
                                            ):
                                                if (
                                                    biome_pair[0] >= SPRING
                                                    or biome_pair[1] >= SPRING
                                                ):
                                                    # spring tiles are valued approximately double
                                                    new_score += (
                                                        2
                                                        * egg_probabilities[
                                                            biome_pair[0] % SPRING
                                                        ][PROB_INDEX_PROB]
                                                    )
                                                else:
                                                    new_score += egg_probabilities[
                                                        biome_pair[0] % SPRING
                                                    ][PROB_INDEX_PROB]

                                        # update best tile storage
                                        if new_score > score:
                                            score = new_score
                                            tile_1_x_best = tile_1_x_current
                                            tile_1_y_best = tile_1_y_current
                                            tile_1_biom_index_best = TILES[
                                                possible_tile
                                            ][TILE_INDEX_FIRST]
                                            tile_2_x_best = tile_2_x_current
                                            tile_2_y_best = tile_2_y_current
                                            tile_2_biom_index_best = TILES[
                                                possible_tile
                                            ][TILE_INDEX_SECOND]

            # place prediction on board
            game_board_state[player_index][BIOM_INDEX_PREDICTION][
                tile_1_y_best, tile_1_x_best
            ] = tile_1_biom_index_best
            game_board_state[player_index][BIOM_INDEX_PREDICTION][
                tile_2_y_best, tile_2_x_best
            ] = tile_2_biom_index_best


def index_on_board(x, y):
    return x >= 0 and x < GRID_SIZE and y >= 0 and y < GRID_SIZE


# -> biome_pair [biome_index_1, biome_index_2]
# offset [off_y, off_x]
# start_y, start_x should describe X, second be H (as per offset), generates the Pairs X,O and H,M like:
#   O
# O X O
# M H M
#   M
def surrounding_biome_pairs(tile_index, player_biome_board, start_y, start_x, offset):
    second_y = start_y + offset[0]
    second_x = start_x + offset[1]

    # [first_biome_index, y_to_take_from_player, x_to_take_from_player]
    preform = [
        [
            TILES[tile_index][TILE_INDEX_FIRST],
            start_y - offset[0],
            start_x - offset[1],
        ],
        [
            TILES[tile_index][TILE_INDEX_FIRST],
            start_y + (abs(offset[0]) - 1),
            start_x + (abs(offset[1]) - 1),
        ],
        [
            TILES[tile_index][TILE_INDEX_FIRST],
            start_y - (abs(offset[0]) - 1),
            start_x - (abs(offset[1]) - 1),
        ],
        [
            TILES[tile_index][TILE_INDEX_SECOND],
            second_y + offset[0],
            second_x + offset[1],
        ],
        [
            TILES[tile_index][TILE_INDEX_SECOND],
            second_y + (abs(offset[0]) - 1),
            second_x + (abs(offset[1]) - 1),
        ],
        [
            TILES[tile_index][TILE_INDEX_SECOND],
            second_y - (abs(offset[0]) - 1),
            second_x - (abs(offset[1]) - 1),
        ],
    ]

    # biome_pair [biome_index_1, biome_index_2], where second biom index can be taken from board
    results = []
    for possibility in preform:
        if index_on_board(possibility[2], possibility[1]):
            results.append(
                [
                    possibility[0],  # preselected index
                    player_biome_board[
                        possibility[1],  # y_from_player_board
                        possibility[2],  # x_from_player_board
                    ],
                ]
            )

    return results
