import tkinter as tk

class SettingsPanel(tk.Frame):
    '''Creates a settings panel.

    Attributes:
        audio_enabled_text (tk.StringVar): Text to put on button_audio_toggle.
        audio_enabled (bool): Whether audio is enabled for a tile.
        selected_tile (Tile): The tile selected by the user.
        vido_panel (VideoPlayer): The video player to control.
        label_video_settings (tk.Label): "Video Settings".
        label_video_input (tk.Label): "Video Source".
        entry_video_input (tk.Entry): URI entry field.
        button_play (tk.Button): When pressed, play the video in the selected tile.
        button_audio_toggle (tk.Button): When pressed, toggle audio on/off on the selected tile.

    '''

    def __init__(self, x, y, width, height):
        '''Initialise the settings panel.

        Args:
            x (int): x position of the frame.
            y (int): y position of the frame.
            width (int): width of the frame.
            height (int): height of the frame.

        '''

        tk.Frame.__init__(self, width=width, height=height)
        self.place(x=x, y=y, relwidth=1)

        self.audio_enabled_text = tk.StringVar(value="Enable Audio")
        self.audio_enabled = False

        self.selected_tile = None
        self.video_panel = None

        self.label_video_settings = tk.Label(self, text="Video Settings", font=("Arial", 14))
        self.label_video_settings.grid(sticky="WE", row=0, column=0)

        self.label_video_input = tk.Label(self, text="Video Source")
        self.label_video_input.grid(sticky="WE", row=1, column=0)

        self.entry_video_input = tk.Entry(self, width=20)
        self.entry_video_input.grid(sticky="WE", row=1, column=1)

        self.button_play = tk.Button(self, text="Play", command=self.play_video)
        self.button_play.grid(sticky="WE", row=1, column=2)

        self.button_audio_toggle = tk.Button(self, textvariable=self.audio_enabled_text, command=self.toggle_audio)
        self.button_audio_toggle.grid(sticky="WE", row=2, column=2)

    def link_video_panel(self, panel):
        '''Links the video panel to the settings panel.

        '''

        self.video_panel = panel

    def toggle_audio(self):
        '''Toggles audio on/off for the selected tile.

        '''
        self.audio_enabled = not self.audio_enabled
        
        self.audio_enabled_text.set("Disable Audio") if self.audio_enabled else self.audio_enabled_text.set("Enable Audio")

        if self.audio_enabled:
            self.selected_tile.pad_audio.set_property("volume", 1)
        else:
            self.selected_tile.pad_audio.set_property("volume", 0)

        self.selected_tile.audio_enabled = self.audio_enabled

        self.video_panel.multiview.tiles[self.selected_tile.id] = self.selected_tile

    def play_video(self):
        '''Plays a selected video tile.

        '''

        if self.selected_tile != None:
            uri = self.entry_video_input.get()
            if uri.upper() != "RTMP://...":
                # Update the selected tile URI.
                self.selected_tile.uri = uri

                # Update the tiles list.
                self.video_panel.multiview.tiles[self.selected_tile.id] = self.selected_tile

                # Set the uri of the video source.
                self.selected_tile.video_source.set_uri(uri)

    def set_selected_tile(self, tile):
        '''Set the currently selected tile.

        Args:
            tile (Tile): The tile to select.

        '''
        
        # Store the selected tile.
        self.selected_tile = tile

        # Use the tile URI if set, otherwise add placeholder.
        if tile.uri != None:
            self.entry_video_input.delete(0, tk.END)
            self.entry_video_input.insert(0, tile.uri)
        else:
            self.entry_video_input.delete(0, tk.END)
            self.entry_video_input.insert(0, "rtmp://...")

        # Set audio enabled buttons.
        if tile.audio_enabled == True:
            self.audio_enabled = tk.TRUE

            self.audio_enabled_text.set("Disable Audio")
        else:
            self.audio_enabled = tk.FALSE

            self.audio_enabled_text.set("Enable Audio")
