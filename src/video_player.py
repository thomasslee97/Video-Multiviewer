import tkinter as tk
from src.multiview import *
from src.pipeline import *

class VideoPlayer(tk.Frame):
    def __init__(self, x, y, width, height):
        tk.Frame.__init__(self)
        self.place(x=x, y=y, width=width, height=height)
        self.config(background="red")

        self.multiview = Multiview(width, height)

        self.pipeline = Pipeline(self.winfo_id())
        self.pipeline.start()

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Split Horizontally", command=self.split_horizontally)
        self.popup_menu.add_command(label="Split Vertically", command=self.split_vertically)

        # bind mouse events to window
        self.bind("<Button-1>", self.buttonPressed)

        self.bind("<Button-3>", self.spilt_menu)

    def buttonPressed(self, event):
        print(event.x, "_", event.y)
        print(self.multiview.find_tile_at_pos(event.x, event.y))

    def spilt_menu(self, event):
        self.selected_x = event.x
        self.selected_y = event.y

        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def split_horizontally(self):
        print("Split Horizontal at: " + str(self.selected_x) + "_" + str(self.selected_y))
    
    def split_vertically(self):
        print("Split Vertical at: " + str(self.selected_x) + "_" + str(self.selected_y))
