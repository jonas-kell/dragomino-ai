import tkinter as tk

from ResizingCanvas import ResizingCanvas
from game_constants import *
from game_logic import ACTION_SET_TILE
from game_logic import game_description

CANVAS_WIDTH_SU = 30
CANVAS_WIDTH_SU = 20
TOTAL_HEIGHT_SU = 20

SPRING_SIZE = 0.7
DRAGON_SIZE = 0.25
SHELL_SIZE = 0.1


class PlayerCanvas(ResizingCanvas):
    def __init__(self, parent, player_board_state, action_callback, **kwargs):
        ResizingCanvas.__init__(self, parent, self.handle_click, **kwargs)

        self.player_board_state = player_board_state
        self.action_callback = action_callback

        self.fill_from_player_board_state()

    def fill_from_player_board_state(self):
        self.clear()  # clears canvas and draws board stuff

        # draw tiles
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

                    # draw springs
                    if self.player_board_state[0][i, j] >= SPRING:
                        self.create_oval(
                            int(
                                self.width / GRID_SIZE * j
                                + self.width / GRID_SIZE * (1 - SPRING_SIZE)
                            ),
                            int(
                                self.height / GRID_SIZE * i
                                + self.height / GRID_SIZE * (1 - SPRING_SIZE)
                            ),
                            int(
                                self.width / GRID_SIZE * (j + 1)
                                - self.width / GRID_SIZE * (1 - SPRING_SIZE)
                            ),
                            int(
                                self.height / GRID_SIZE * (i + 1)
                                - self.height / GRID_SIZE * (1 - SPRING_SIZE)
                            ),
                            fill="#0c008f",
                        )

        # draw dragons and shells
        for i in range(GRID_SIZE * 2):  # double the possibilities
            for j in range(GRID_SIZE):
                if self.player_board_state[1][i, j] > 0:

                    index_center_x = j + 0.5 if i % 2 == 0 else j
                    index_center_y = i / 2.0

                    if self.player_board_state[1][i, j] < EMPTY_SHELL:
                        # dragon
                        self.create_oval(
                            int(
                                self.width / GRID_SIZE * index_center_x
                                - self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                - self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.width / GRID_SIZE * index_center_x
                                + self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                + self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            fill=COLORS[self.player_board_state[1][i, j]],
                            outline="#222222",
                            width=3,
                        )
                    else:
                        # shell
                        self.create_line(
                            int(
                                self.width / GRID_SIZE * index_center_x
                                - self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                - self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.width / GRID_SIZE * index_center_x
                                + self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                + self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            fill="#222222",
                            width=4,
                        )
                        self.create_line(
                            int(
                                self.width / GRID_SIZE * index_center_x
                                - self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                - self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.width / GRID_SIZE * index_center_x
                                + self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                + self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            fill=COLORS[self.player_board_state[1][i, j] % EMPTY_SHELL],
                            width=2,
                        )
                        self.create_line(
                            int(
                                self.width / GRID_SIZE * index_center_x
                                + self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                - self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.width / GRID_SIZE * index_center_x
                                - self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                + self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            fill="#222222",
                            width=4,
                        )
                        self.create_line(
                            int(
                                self.width / GRID_SIZE * index_center_x
                                + self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                - self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.width / GRID_SIZE * index_center_x
                                - self.width / GRID_SIZE * DRAGON_SIZE
                            ),
                            int(
                                self.height / GRID_SIZE * index_center_y
                                + self.height / GRID_SIZE * DRAGON_SIZE
                            ),
                            fill=COLORS[self.player_board_state[1][i, j] % EMPTY_SHELL],
                            width=2,
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

    def force_redraw(self):
        self.fill_from_player_board_state()


class PlayerWindow:
    def __init__(
        self,
        tk_root_window,
        title,
        player_index,
        game_board_state,
        action_callback,
    ):

        self.player_index = player_index
        self.game_board_state = game_board_state
        self.action_callback = action_callback

        self.tkwindow = tk.Toplevel(
            tk_root_window,
            width=CANVAS_WIDTH_SU + CANVAS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
        )
        self.tkwindow.title(title)

        # right aligned text box
        self.description = tk.StringVar()
        self.description.set(game_description(self.player_index, self.game_board_state))
        self.stats = tk.Label(
            self.tkwindow,
            width=CANVAS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
            textvariable=self.description,
        )
        self.stats.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        # canvas to fill space
        self.canvas = PlayerCanvas(
            self.tkwindow,
            self.game_board_state[self.player_index],
            self.action_callback,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def force_redraw(self):
        self.description.set(game_description(self.player_index, self.game_board_state))
        self.canvas.force_redraw()