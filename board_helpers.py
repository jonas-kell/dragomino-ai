import numpy as np
from game_constants import *

BIOM_INDEX = 0
EGG_INDEX = 1
SECOND_TILE_TURN_INDEX = 2
USED_TILE_INDEX = 0
SELECTED_TILE_INDEX = 1


def init_empty_game_state():
    players = [None] * (PLAYER_COUNT + 1)

    for i in range(PLAYER_COUNT):
        players[i] = [
            np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8),  # bioms
            np.zeros((GRID_SIZE * 2, GRID_SIZE), dtype=np.uint8),  # eggs/dragons
            [0, 1],  # turning: [y-offset, x-offset]
        ]

        # add starting tile
        players[i][BIOM_INDEX][GRID_CENTER, GRID_CENTER - 1] = STARTING_TILE[
            TILE_INDEX_FIRST
        ]
        players[i][BIOM_INDEX][GRID_CENTER, GRID_CENTER] = STARTING_TILE[
            TILE_INDEX_SECOND
        ]

        # add test dragon/shell
        players[i][EGG_INDEX][GRID_CENTER, GRID_CENTER] = DESSERT
        players[i][EGG_INDEX][GRID_CENTER + 1, GRID_CENTER] = VULCANO
        players[i][EGG_INDEX][GRID_CENTER, GRID_CENTER + 1] = SNOW
        players[i][EGG_INDEX][GRID_CENTER + 1, GRID_CENTER + 1] = MOUNTAINS
        players[i][EGG_INDEX][2 * GRID_CENTER, GRID_CENTER] = DESSERT + EMPTY_SHELL
        players[i][EGG_INDEX][2 * GRID_CENTER + 1, GRID_CENTER] = VULCANO + EMPTY_SHELL
        players[i][EGG_INDEX][2 * GRID_CENTER, GRID_CENTER + 1] = SNOW + EMPTY_SHELL
        players[i][EGG_INDEX][2 * GRID_CENTER + 1, GRID_CENTER + 1] = (
            MOUNTAINS + EMPTY_SHELL
        )

    players[PLAYER_COUNT] = [
        [],  # used tiles
        [],  # selected_tiles
    ]

    return players