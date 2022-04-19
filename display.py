import tkinter as tk
from matplotlib.pyplot import margins
import numpy as np

GRID_SIZE = 10
GRID_CENTER = GRID_SIZE // 2
PLAYER_COUNT = 1

COLOR = "#222222"
BACKGROUND = "grey"


class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        self.bg = BACKGROUND
        kwargs.setdefault("bg", self.bg)
        tk.Canvas.__init__(self, parent, **kwargs)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.color = COLOR
        self.linewidth = 1

        self.bind("<Configure>", self.resize)
        self.bind("<ButtonRelease-1>", self.handle_click)

        self.init_empty_game_state()  # presets empty arrays
        self.fill_from_game_state()

    def init_empty_game_state(self):
        self.players = [0 for i in range(PLAYER_COUNT)]

        for i in range(PLAYER_COUNT):
            self.players = [
                np.zeros((GRID_SIZE, GRID_SIZE)),  # fields
                np.zeros((GRID_SIZE, GRID_SIZE)),  # eggs/daragons
            ]

    def fill_from_game_state(self):
        self.clear()  # draws board stuff

        # cell_width = self.width / self.rows
        # cell_height = self.height / self.rows
        # padding_factor = 0.2
        # cell_width_padding = self.width / self.rows * padding_factor
        # cell_height_padding = self.height / self.rows * padding_factor

    def handle_click(self, event):
        grid_x = int(((float(event.x) / self.width) * GRID_SIZE) // 1)
        grid_y = int(((float(event.y) / self.height) * GRID_SIZE) // 1)

        print(grid_x, grid_y)

    def clear(self):
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

    def resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)


def main():
    canvas_width_su = 30
    stats_width_su = 20
    total_height_su = 20

    root = tk.Tk()
    root.title("DRAGOMINO")

    myframe = tk.Frame(
        root, width=canvas_width_su + stats_width_su, height=total_height_su
    )
    myframe.pack(fill=tk.BOTH, expand=tk.YES)

    # right aligned text box
    stats = tk.Label(
        myframe,
        width=stats_width_su,
        height=total_height_su,
        text="Test Text \n asd\n asdasd",
    )
    stats.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

    # canvas to fill space
    mycanvas = ResizingCanvas(
        myframe,
        highlightthickness=0,
    )
    mycanvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    # tag all of the drawn widgets (later reference)
    mycanvas.addtag_all("all")

    # main draw loop
    root.mainloop()


if __name__ == "__main__":
    main()
