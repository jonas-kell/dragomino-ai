import tkinter as tk

COLOR = "#222222"
BACKGROUND = "grey"


class ResizingCanvas(tk.Canvas):
    def __init__(
        self, parent, l_click_callback, r_click_callback, motion_calback, **kwargs
    ):
        self.bg = BACKGROUND
        kwargs.setdefault("bg", self.bg)
        tk.Canvas.__init__(self, parent, **kwargs)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.color = COLOR
        self.linewidth = 2

        self.bind("<Configure>", self.resize)
        if l_click_callback is not None:
            self.bind("<ButtonRelease-1>", l_click_callback)
        if r_click_callback is not None:
            self.bind("<ButtonRelease-3>", r_click_callback)
        if motion_calback is not None:
            self.bind("<Motion>", motion_calback)

    def resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.addtag_all("all")
        self.scale("all", 0, 0, wscale, hscale)