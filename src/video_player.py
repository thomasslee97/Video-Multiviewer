import tkinter as tk
from src.multiview import *
from src.pipeline import *

class VideoPlayer(tk.Frame):
    '''Stores the video player properties.
    
    Attributes:
        settings_panel (tk.Frame): Panel containing settings.
        multiview (Multiview): Multiview properties.
        pipeline (Pipeline): Pipeline properties.
        popup_menu (tk.Menu): Right-click menu.

    '''

    def __init__(self, x, y, width, height):
        tk.Frame.__init__(self)
        self.place(x=x, y=y, width=width, height=height)
        self.config(background="black")

        self.settings_panel = None

        # Create multiview.
        self.multiview = Multiview(width, height)

        # Create pipeline.
        self.pipeline = Pipeline(self.winfo_id())

        # Create right-click popup menu.
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Split Horizontally", command=self.split_horizontally)
        self.popup_menu.add_command(label="Split Vertically", command=self.split_vertically)

        # Bind left click.
        self.bind("<Button-1>", self.player_clicked)

        # Bind right click.
        self.bind("<Button-3>", self.spilt_menu)

        # Start pipeline.
        self.pipeline.start()

    def link_settings_panel(self, panel):
        '''Sets the settings_panel.

        Args:
            panel (tk.Frame): Panel containing settings controls.

        '''
        self.settings_panel = panel

    def player_clicked(self, event):
        '''Called when the video player is clicked.

        Args:
            event: Click event.

        '''
        
        # Find the tile that was clicked and select it.
        self.select_tile(self.multiview.find_tile_at_pos(event.x, event.y))

    def select_tile(self, tile):
        '''Select a tile.

        Args:
            tile (Tile): Tile selected.

        '''

        self.settings_panel.set_selected_tile(tile)

    def spilt_menu(self, event):
        '''Shows the right-click menu.

        '''

        self.selected_x = event.x
        self.selected_y = event.y

        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def split_horizontally(self):
        '''Splits a tile horizontally.

        '''

        print("Split Horizontal at: " + str(self.selected_x) + "_" + str(self.selected_y))
    
    def split_vertically(self):
        '''Splits a tile vertically.

        '''
        
        print("Split Vertical at: " + str(self.selected_x) + "_" + str(self.selected_y))
