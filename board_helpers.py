import numpy as np
from game_constants import *


def init_empty_game_state():
    players = [0 for i in range(PLAYER_COUNT)]

    for i in range(PLAYER_COUNT):
        players[i] = [
            np.zeros((GRID_SIZE, GRID_SIZE)),  # fields
            np.zeros((GRID_SIZE, GRID_SIZE)),  # eggs/daragons
        ]

    return players