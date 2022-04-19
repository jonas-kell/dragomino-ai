import tkinter as tk

from ResizingCanvas import ResizingCanvas
from game_constants import *
from game_logic import ACTION_SET_TILE

CANVAS_WIDTH_SU = 30
CANVAS_WIDTH_SU = 20
TOTAL_HEIGHT_SU = 20


class PlayerCanvas(ResizingCanvas):
    def __init__(self, parent, player_board_state, action_callback, **kwargs):
        ResizingCanvas.__init__(self, parent, self.handle_click, **kwargs)

        self.player_board_state = player_board_state
        self.action_callback = action_callback

        self.fill_from_player_board_state()

    def fill_from_player_board_state(self):
        self.clear()  # clears canvas and draws board stuff

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.player_board_state[0][i, j] > 0:
                    self.create_rectangle(
                        int(self.width / GRID_SIZE * j),
                        int(self.height / GRID_SIZE * i),
                        int(self.width / GRID_SIZE * (j + 1)),
                        int(self.height / GRID_SIZE * (i + 1)),
                        fill=COLORS[(self.player_board_state[0][i, j]) % SPRING],
                    )

    def clear(self):
        self.addtag_all("all")
        self.delete("all")
        self.init_grid()

    def init_grid(self):
        for i in range(1, GRID_SIZE):
            self.create_line(
                self.width / GRID_SIZE * i,
                0,
                self.width / GRID_SIZE * i,
                self.height,
                width=self.linewidth,
                fill=self.color,
            )
            self.create_line(
                0,
                self.height / GRID_SIZE * i,
                self.width,
                self.height / GRID_SIZE * i,
                width=self.linewidth,
                fill=self.color,
            )

    def handle_click(self, event):
        grid_x = int(((float(event.x) / self.width) * GRID_SIZE) // 1)
        grid_y = int(((float(event.y) / self.height) * GRID_SIZE) // 1)

        self.action_callback(ACTION_SET_TILE, gx=grid_x, gy=grid_y)


class PlayerWindow:
    def __init__(self, tk_root_window, title, player_board_state, action_callback):

        self.player_board_state = player_board_state
        self.action_callback = action_callback

        self.tkwindow = tk.Toplevel(
            tk_root_window,
            width=CANVAS_WIDTH_SU + CANVAS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
        )
        self.tkwindow.title(title)

        # right aligned text box
        self.stats = tk.Label(
            self.tkwindow,
            width=CANVAS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
            text="Test Text \n asd\n asdasd",
        )
        self.stats.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        # canvas to fill space
        self.canvas = PlayerCanvas(
            self.tkwindow,
            player_board_state,
            action_callback,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)