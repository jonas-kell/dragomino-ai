import tkinter as tk

from ResizingCanvas import ResizingCanvas
from game_constants import *
from game_logic import ACTION_PICK_TILE

CANVAS_WIDTH_SU = 30
STATS_WIDTH_SU = 20
TOTAL_HEIGHT_SU = 20

SPRING_SIZE = 0.88
SEPERATION = 0.1
ROWS = 4


class MainCanvas(ResizingCanvas):
    def __init__(self, parent, game_board_state, action_callback, **kwargs):
        ResizingCanvas.__init__(self, parent, self.handle_click, **kwargs)

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
                # left square
                self.create_rectangle(
                    int(width_segment * j + width_segment * SEPERATION),
                    int(height_segment * i + height_segment * SEPERATION),
                    int(width_segment * (j + 0.5)),
                    int(height_segment * (i + 1) - height_segment * SEPERATION),
                    fill=COLORS[TILES[j * tiles_per_row + i][1] % SPRING],
                )
                # left spring
                if TILES[j * tiles_per_row + i][1] >= SPRING:
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
                    fill=COLORS[TILES[j * tiles_per_row + i][2] % SPRING],
                )
                # right spring
                if TILES[j * tiles_per_row + i][2] >= SPRING:
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