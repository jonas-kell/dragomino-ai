import tkinter as tk

from ResizingCanvas import ResizingCanvas
from board_helpers import SELECTED_TILE_INDEX, USED_TILE_INDEX
from game_constants import *
from game_logic import ACTION_PICK_TILE, main_description

CANVAS_WIDTH_SU = 30
STATS_WIDTH_SU = 20
TOTAL_HEIGHT_SU = 20

SPRING_SIZE = 0.88
SEPERATION = 0.1
ROWS = 4


class MainCanvas(ResizingCanvas):
    def __init__(self, parent, game_board_state, action_callback, **kwargs):
        ResizingCanvas.__init__(self, parent, self.handle_l_click, None, None, **kwargs)

        self.game_board_state = game_board_state
        self.action_callback = action_callback

        self.fill_from_game_board_state()

    def fill_from_game_board_state(self):
        self.clear()  # clears canvas

        height_segment = float(self.height) / (len(TILES) // ROWS)
        width_segment = float(self.width) / ROWS

        tiles_per_row = len(TILES) // ROWS
        # draw tiles backlog
        for j in range(ROWS):
            for i in range(tiles_per_row):
                # draw used
                for tile in self.game_board_state[PLAYER_COUNT][USED_TILE_INDEX]:
                    if tile == 1 + j * tiles_per_row + i:
                        self.create_rectangle(
                            int(width_segment * j),
                            int(height_segment * i),
                            int(width_segment * (j + 1)),
                            int(height_segment * (i + 1)),
                            fill="#111111",
                        )
                # draw selected
                for tile in self.game_board_state[PLAYER_COUNT][SELECTED_TILE_INDEX]:
                    if tile == 1 + j * tiles_per_row + i:
                        self.create_rectangle(
                            int(width_segment * j),
                            int(height_segment * i),
                            int(width_segment * (j + 1)),
                            int(height_segment * (i + 1)),
                            fill="#26a8e8",
                        )

                # left square
                self.create_rectangle(
                    int(width_segment * j + width_segment * SEPERATION),
                    int(height_segment * i + height_segment * SEPERATION),
                    int(width_segment * (j + 0.5)),
                    int(height_segment * (i + 1) - height_segment * SEPERATION),
                    fill=COLORS[
                        TILES[1 + j * tiles_per_row + i][TILE_INDEX_FIRST] % SPRING
                    ],
                )
                # left spring
                if TILES[1 + j * tiles_per_row + i][TILE_INDEX_FIRST] >= SPRING:
                    self.create_oval(
                        int(
                            width_segment * j
                            + width_segment * SEPERATION
                            + width_segment * (1 - SPRING_SIZE)
                        ),
                        int(
                            height_segment * i
                            + height_segment * SEPERATION
                            + height_segment * (1 - SPRING_SIZE) * 2
                        ),
                        int(
                            width_segment * (j + 0.5)
                            - width_segment * (1 - SPRING_SIZE)
                        ),
                        int(
                            height_segment * (i + 1)
                            - height_segment * SEPERATION
                            - height_segment * (1 - SPRING_SIZE) * 2
                        ),
                        fill="#0c008f",
                    )
                # right square
                self.create_rectangle(
                    int(width_segment * (j + 0.5)),
                    int(height_segment * i + height_segment * SEPERATION),
                    int(width_segment * (j + 1) - width_segment * SEPERATION),
                    int(height_segment * (i + 1) - height_segment * SEPERATION),
                    fill=COLORS[
                        TILES[1 + j * tiles_per_row + i][TILE_INDEX_SECOND] % SPRING
                    ],
                )
                # right spring
                if TILES[1 + j * tiles_per_row + i][TILE_INDEX_SECOND] >= SPRING:
                    self.create_oval(
                        int(
                            width_segment * (j + 0.5)
                            + width_segment * (1 - SPRING_SIZE)
                        ),
                        int(
                            height_segment * i
                            + height_segment * SEPERATION
                            + height_segment * (1 - SPRING_SIZE) * 2
                        ),
                        int(
                            width_segment * (j + 1)
                            - width_segment * SEPERATION
                            - width_segment * (1 - SPRING_SIZE)
                        ),
                        int(
                            height_segment * (i + 1)
                            - height_segment * SEPERATION
                            - height_segment * (1 - SPRING_SIZE) * 2
                        ),
                        fill="#0c008f",
                    )

    def clear(self):
        self.addtag_all("all")
        self.delete("all")

    def handle_l_click(self, event):
        index = self.event_to_index(event)

        self.action_callback(ACTION_PICK_TILE, tile_index=index)

    def event_to_index(self, event):
        return int(
            (((float(event.x) / self.width) * ROWS) // 1) * (len(TILES) // ROWS)
            + (((float(event.y) / self.height) * (len(TILES) // ROWS)) // 1)
            + 1
        )

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
        self.description.set(main_description(self.game_board_state))
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
        self.description.set(main_description(self.game_board_state))
        self.canvas.force_redraw()