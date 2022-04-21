import numpy as np
from game_constants import *


def init_empty_game_state():
    players = [None] * (PLAYER_COUNT + 1)

    for i in range(PLAYER_COUNT):
        players[i] = [
            np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8),  # bioms
            np.zeros((GRID_SIZE * 2, GRID_SIZE), dtype=np.uint8),  # eggs/dragons
        ]

        # add starting tile
        players[i][0][GRID_CENTER, GRID_CENTER - 1] = STARTING_TILE[1]
        players[i][0][GRID_CENTER, GRID_CENTER] = STARTING_TILE[2]

        # add test dragon/shell
        players[i][1][GRID_CENTER, GRID_CENTER] = DESSERT
        players[i][1][GRID_CENTER + 1, GRID_CENTER] = VULCANO
        players[i][1][GRID_CENTER, GRID_CENTER + 1] = SNOW
        players[i][1][GRID_CENTER + 1, GRID_CENTER + 1] = MOUNTAINS
        players[i][1][2 * GRID_CENTER, GRID_CENTER] = DESSERT + EMPTY_SHELL
        players[i][1][2 * GRID_CENTER + 1, GRID_CENTER] = VULCANO + EMPTY_SHELL
        players[i][1][2 * GRID_CENTER, GRID_CENTER + 1] = SNOW + EMPTY_SHELL
        players[i][1][2 * GRID_CENTER + 1, GRID_CENTER + 1] = MOUNTAINS + EMPTY_SHELL

    players[PLAYER_COUNT] = [
        [],  # used tiles
        [],  # selected_tiles
    ]

    return players