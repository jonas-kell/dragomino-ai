import tkinter as tk

from ResizingCanvas import ResizingCanvas
from board_helpers import BIOM_INDEX, BIOM_INDEX_PREVIEW, EGG_INDEX
from game_constants import *
from game_logic import (
    ACTION_PREVIEW_TILE,
    ACTION_SET_TILE,
    ACTION_TOGGLE_EGGS,
    ACTION_TURN_TILE,
    tile_is_being_placed,
)
from game_logic import game_description

CANVAS_WIDTH_SU = 30
STATS_WIDTH_SU = 20
TOTAL_HEIGHT_SU = 20

SPRING_SIZE = 0.7
DRAGON_SIZE = 0.25
SHELL_SIZE = 0.1


class PlayerCanvas(ResizingCanvas):
    def __init__(
        self, parent, player_index, game_board_state, action_callback, **kwargs
    ):
        ResizingCanvas.__init__(
            self,
            parent,
            self.handle_l_click,
            self.handle_r_click,
            self.handle_motion,
            **kwargs,
        )

        self.game_board_state = game_board_state
        self.player_board_state = game_board_state[player_index]
        self.action_callback = action_callback

        self.fill_from_player_board_state()

    def fill_from_player_board_state(self):
        self.clear()  # clears canvas and draws board stuff

        # draw tiles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.draw_biom_tile(self.player_board_state[BIOM_INDEX][i, j], j, i)

        # draw preview
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.draw_biom_tile(
                    self.player_board_state[BIOM_INDEX_PREVIEW][i, j], j, i, True
                )

        # draw dragons and shells
        for i in range(GRID_SIZE * 2):  # double the possibilities
            for j in range(GRID_SIZE):
                if self.player_board_state[EGG_INDEX][i, j] > 0:

                    index_center_x = j + 0.5 if i % 2 == 0 else j
                    index_center_y = i / 2.0

                    if self.player_board_state[EGG_INDEX][i, j] < EMPTY_SHELL:
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
                            fill=COLORS[self.player_board_state[EGG_INDEX][i, j]],
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
                            fill=COLORS[
                                self.player_board_state[EGG_INDEX][i, j] % EMPTY_SHELL
                            ],
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
                            fill=COLORS[
                                self.player_board_state[EGG_INDEX][i, j] % EMPTY_SHELL
                            ],
                            width=2,
                        )

    def draw_biom_tile(self, biom_index, x_index, y_index, preview=False):
        if biom_index > 0:
            self.create_rectangle(
                int(self.width / GRID_SIZE * x_index),
                int(self.height / GRID_SIZE * y_index),
                int(self.width / GRID_SIZE * (x_index + 1)),
                int(self.height / GRID_SIZE * (y_index + 1)),
                fill=COLORS[(biom_index) % SPRING],
                stipple="gray50" if preview else "",
            )

            # draw springs
            if biom_index >= SPRING:
                self.create_oval(
                    int(
                        self.width / GRID_SIZE * x_index
                        + self.width / GRID_SIZE * (1 - SPRING_SIZE)
                    ),
                    int(
                        self.height / GRID_SIZE * y_index
                        + self.height / GRID_SIZE * (1 - SPRING_SIZE)
                    ),
                    int(
                        self.width / GRID_SIZE * (x_index + 1)
                        - self.width / GRID_SIZE * (1 - SPRING_SIZE)
                    ),
                    int(
                        self.height / GRID_SIZE * (y_index + 1)
                        - self.height / GRID_SIZE * (1 - SPRING_SIZE)
                    ),
                    fill="#0c008f",
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

    def handle_l_click(self, event):
        grid_x, grid_y = self.event_to_index(event)

        self.action_callback(ACTION_SET_TILE, gx=grid_x, gy=grid_y)

    def handle_r_click(self, event):
        if tile_is_being_placed(self.game_board_state):
            grid_x, grid_y = self.event_to_index(event)

            self.action_callback(ACTION_TURN_TILE, gx=grid_x, gy=grid_y)
        else:
            ex, ey, t_1_x, t_1_y, t_2_x, t_2_y = self.event_to_egg_index(event)

            self.action_callback(
                ACTION_TOGGLE_EGGS,
                ex=ex,
                ey=ey,
                t1x=t_1_x,
                t1y=t_1_y,
                t2x=t_2_x,
                t2y=t_2_y,
            )

    def handle_motion(self, event):
        grid_x, grid_y = self.event_to_index(event)

        self.action_callback(ACTION_PREVIEW_TILE, gx=grid_x, gy=grid_y)

    def event_to_index(self, event):
        grid_x = int(((float(event.x) / self.width) * GRID_SIZE) // 1)
        grid_y = int(((float(event.y) / self.height) * GRID_SIZE) // 1)

        return grid_x, grid_y

    def event_to_egg_index(self, event):
        # get first tile (the one hovered over)
        tile_1_index_x, tile_1_index_y = self.event_to_index(event)

        # get second tile (the one closest)
        center_x = (tile_1_index_x + 0.5) * (self.width / GRID_SIZE)
        center_y = (tile_1_index_y + 0.5) * (self.height / GRID_SIZE)
        difference_x = center_x - event.x
        difference_y = center_y - event.y
        y_more_important = abs(difference_y) > abs(difference_x)
        if y_more_important:
            tile_2_index_x = tile_1_index_x
            tile_2_index_y = tile_1_index_y + (-1 if difference_y > 0 else 1)
        else:
            tile_2_index_x = tile_1_index_x + (-1 if difference_x > 0 else 1)
            tile_2_index_y = tile_1_index_y

        # swap, to let the more top left one in index 1
        if tile_1_index_x > tile_2_index_x:
            swap = tile_2_index_x
            tile_2_index_x = tile_1_index_x
            tile_1_index_x = swap

        if tile_1_index_y > tile_2_index_y:
            swap = tile_2_index_y
            tile_2_index_y = tile_1_index_y
            tile_1_index_y = swap

        # translate the tile indicees to egg index
        egg_index_x = tile_2_index_x
        egg_index_y = tile_1_index_y + tile_2_index_y + 1

        return (
            egg_index_x,
            egg_index_y,
            tile_1_index_x,
            tile_1_index_y,
            tile_2_index_x,
            tile_2_index_y,
        )

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
            width=CANVAS_WIDTH_SU + STATS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
        )
        self.tkwindow.title(title)

        # right aligned text box
        self.description = tk.StringVar()
        self.description.set(game_description(self.player_index, self.game_board_state))
        self.stats = tk.Label(
            self.tkwindow,
            width=STATS_WIDTH_SU,
            height=TOTAL_HEIGHT_SU,
            textvariable=self.description,
        )
        self.stats.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        # canvas to fill space
        self.canvas = PlayerCanvas(
            self.tkwindow,
            self.player_index,
            self.game_board_state,
            self.action_callback,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def force_redraw(self):
        self.description.set(game_description(self.player_index, self.game_board_state))
        self.canvas.force_redraw()