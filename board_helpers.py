import numpy as np
from game_constants import *


def init_empty_game_state():
    players = [0 for i in range(PLAYER_COUNT)]

    for i in range(PLAYER_COUNT):
        players[i] = [
            np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8),  # bioms
            np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8),  # eggs/dragons
        ]
        # add starting tile
        players[i][0][GRID_CENTER, GRID_CENTER - 1] = STARTING_TILE[1]
        players[i][0][GRID_CENTER, GRID_CENTER] = STARTING_TILE[2]

    return players