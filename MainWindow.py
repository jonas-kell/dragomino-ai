import tkinter as tk

from ResizingCanvas import ResizingCanvas
from game_constants import *
from game_logic import ACTION_PICK_TILE

CANVAS_WIDTH_SU = 30
STATS_WIDTH_SU = 20
TOTAL_HEIGHT_SU = 20

SPRING_SIZE = 0.7
DRAGON_SIZE = 0.25
SHELL_SIZE = 0.1


class MainCanvas(ResizingCanvas):
    def __init__(self, parent, game_board_state, action_callback, **kwargs):
        ResizingCanvas.__init__(self, parent, self.handle_click, **kwargs)

        self.game_board_state = game_board_state
        self.action_callback = action_callback

        self.fill_from_game_board_state()

    def fill_from_game_board_state(self):
        self.clear()  # clears canvas

        # TODO

    def clear(self):
        self.addtag_all("all")
        self.delete("all")

    def handle_click(self, event):
        # grid_x = int(((float(event.x) / self.width) * GRID_SIZE) // 1)
        # grid_y = int(((float(event.y) / self.height) * GRID_SIZE) // 1)

        self.action_callback(ACTION_PICK_TILE, tile_index=1)

    def force_redraw(self):
        self.fill_from_game_board_state()


class MainWindow:
    def __init__(
        self,
        tk_root_window,
        game_board_state,
        action_callback,
    ):
        self.game_board_state = game_board_state
        self.action_callback = action_callback

        self.tkframe = tk.Frame(
            tk_root_window,
            width=CANVAS_WIDTH_SU + STATS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
        )
        self.tkframe.pack(fill=tk.BOTH, expand=tk.YES)

        # right aligned text box
        self.description = tk.StringVar()
        self.description.set("asd")
        self.stats = tk.Label(
            self.tkframe,
            width=STATS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
            textvariable=self.description,
        )
        self.stats.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        # canvas to fill space
        self.canvas = MainCanvas(
            self.tkframe,
            self.game_board_state,
            self.action_callback,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def force_redraw(self):
        self.description.set("asd")
        self.canvas.force_redraw()