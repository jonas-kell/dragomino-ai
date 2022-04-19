import tkinter as tk

from board_helpers import *
from game_constants import *
from player_window import generate_player_window


def main():
    root = tk.Tk()
    root.title("DRAGOMINO")

    game_state = init_empty_game_state()

    for i in range(PLAYER_COUNT):
        generate_player_window(root, "Player " + str(i), game_state[i])

    # main draw loop
    root.mainloop()
