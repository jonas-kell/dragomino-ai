import tkinter as tk

from board_helpers import *
from PlayerWindow import PlayerWindow
from game_logic import action_player_injector


def main():
    root = tk.Tk()
    root.title("DRAGOMINO")

    game_state = init_empty_game_state()

    for i in range(PLAYER_COUNT):
        PlayerWindow(
            root,
            "Player " + str(i),
            game_state[i],
            action_player_injector(i, game_state),
        )

    # main draw loop
    root.mainloop()