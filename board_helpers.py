import numpy as np
from game_constants import *

BIOM_INDEX = 0
BIOM_INDEX_PREVIEW = 1
EGG_INDEX = 2
SECOND_TILE_TURN_INDEX = 3
USED_TILE_INDEX = 0
SELECTED_TILE_INDEX = 1


def init_empty_game_state():
    players = [None] * (PLAYER_COUNT + 1)

    for i in range(PLAYER_COUNT):
        players[i] = [
            np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8),  # bioms
            np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8),  # bioms_preview
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

    players[PLAYER_COUNT] = [
        [],  # used tiles
        [],  # selected_tiles
    ]

    return players


def clear_previews(game_board_state):
    for i in range(PLAYER_COUNT):
        game_board_state[i][BIOM_INDEX_PREVIEW] = np.zeros(
            (GRID_SIZE, GRID_SIZE), dtype=np.uint8
        )
