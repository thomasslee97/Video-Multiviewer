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
        self.split_by_direction(Direction.HORIZONTAL)
    
    def split_vertically(self):
        '''Splits a tile vertically.

        '''
        
        print("Split Vertical at: " + str(self.selected_x) + "_" + str(self.selected_y))
        self.split_by_direction(Direction.VERTIAL)

    def split_by_direction(self, direction):
        '''Splits a tile in a given direction.

        Args:
            direction (Direction): Direction to split the selected tile.

        '''

        # Find the selected tile.
        tile = self.multiview.find_tile_at_pos(self.selected_x, self.selected_y)

        # Get the tile position/size.
        tile_x = tile.xpos
        tile_y = tile.ypos
        tile_width = tile.width
        tile_height = tile.height

        # Create a new tile.
        new_tile = Tile(self.multiview.get_next_id())

        # If horizontal, split height.
        if direction == Direction.HORIZONTAL:
            new_tile.ypos = tile_y + (tile_height / 2)
            tile_height = tile_height / 2
        else:
            new_tile.ypos = tile_y
        
        # If vertical, split vertical.
        if direction == Direction.VERTIAL:
            new_tile.xpos = tile_x + (tile_width / 2)
            tile_width = tile_width / 2
        else:
            new_tile.xpos = tile_y            

        # Set tile dimensions.
        tile.width = tile_width
        tile.height = tile_height
        new_tile.width = tile_width
        new_tile.height = tile_height

        # Add new, empty video to the video panel.
        pad_video, pad_audio, video_source = self.pipeline.add_video(tile.uri, new_tile.width, new_tile.height, 0, 0)

        # Set video pad/source properties.
        new_tile.pad_video = pad_video
        new_tile.pad_audio = pad_audio
        new_tile.video_source = video_source
        new_tile.uri = tile.uri

        # Stop the pipeline.
        self.pipeline.stop()

        # Set new tile pad properties.
        new_tile.pad_video.set_property("width", new_tile.width)
        new_tile.pad_video.set_property("height", new_tile.height)
        new_tile.pad_video.set_property("xpos", new_tile.xpos)
        new_tile.pad_video.set_property("ypos", new_tile.ypos)

        # Set tile pad properties.
        tile.pad_video.set_property("width", tile.width)
        tile.pad_video.set_property("height", tile.height)
        tile.pad_video.set_property("xpos", tile.xpos)
        tile.pad_video.set_property("ypos", tile.ypos)

        # Start the pipeline.
        self.pipeline.start()
        
        # Update multiview.
        self.multiview.tiles[tile.id] = tile
        self.multiview.add_tile(new_tile)
