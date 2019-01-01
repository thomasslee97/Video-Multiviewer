import tkinter as tk
import tkinter.ttk as ttk
import os
import threading

from src.multiview import *
from src.window_main import *

root = tk.Tk()

root.title("RTMP Multiviewer")

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(0, 0)

root.option_add("*Button.Background", "black")
root.option_add("*Button.Foreground", "white")
# root.tk_setPalette(background='black', foreground='white')

MainWindow(root).pack(side="top", fill="both", expand=True)

root.mainloop()
