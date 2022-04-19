import tkinter as tk

from board_helpers import *
from PlayerWindow import PlayerWindow
from game_logic import action_player_injector

main_window = None
player_windows = [None] * PLAYER_COUNT


def main():
    root = tk.Tk()
    root.title("DRAGOMINO")

    game_state = init_empty_game_state()

    for i in range(PLAYER_COUNT):
        player_windows[i] = PlayerWindow(
            root,
            "Player " + str(i),
            i,
            game_state,
            action_player_injector(force_redraw, i, game_state),
        )

    # main draw loop
    root.mainloop()


def force_redraw():
    # main_window.force_redraw()

    for i in range(PLAYER_COUNT):
        player_windows[i].force_redraw()