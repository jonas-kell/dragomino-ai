import tkinter as tk

from board_helpers import *
from PlayerWindow import PlayerWindow
from MainWindow import MainWindow
from game_logic import action_player_injector, action_injector
from window_geometry import window_geometry

main_window = None
player_windows = [None] * PLAYER_COUNT


def main(mode):
    global main_window
    global player_windows

    game_state = init_empty_game_state()

    root = tk.Tk()
    root.title("Dragomino")

    main_window = MainWindow(
        root, game_state, action_injector(force_redraw, game_state)
    )
    root.geometry(window_geometry[mode][0])

    for i in range(PLAYER_COUNT):
        player_windows[i] = PlayerWindow(
            root,
            "Player " + str(i),
            i,
            game_state,
            action_player_injector(force_redraw, i, game_state),
        )
        player_windows[i].tkwindow.geometry(window_geometry[mode][i + 1])

    # main draw loop
    root.mainloop()


def force_redraw():
    main_window.force_redraw()
    for i in range(PLAYER_COUNT):
        player_windows[i].force_redraw()