import tkinter as tk

class SettingsPanel(tk.Frame):
    def __init__(self, x, y, width, height):
        tk.Frame.__init__(self)
        self.place(x=x, y=y, relwidth=0.5)

        self.audio_enabled_text = tk.StringVar(value="Enable Audio")
        self.preview_stats_text = tk.StringVar(value="View Video Stats")
        self.audio_enabled = False
        self.preview_stats_enabled = False

        self.selected_tile = None

        self.label_video_settings = tk.Label(self, text="Video Settings")
        self.label_video_settings.grid(sticky="WE")

        self.label_video_input = tk.Label(self, text="Video Source")
        self.label_video_input.grid(sticky="WE")

        self.entry_video_input = tk.Entry(self, width=20)
        self.entry_video_input.grid(sticky="WE")

        self.button_play = tk.Button(self, text="Play", command=self.play_video)
        self.button_play.grid(sticky="WE")

        self.button_audio_toggle = tk.Button(self, textvariable=self.audio_enabled_text, command=self.toggle_audio)
        self.button_audio_toggle.grid(sticky="WE")

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        
        self.audio_enabled_text.set("Disable Audio") if self.audio_enabled else self.audio_enabled_text.set("Enable Audio")

    def play_video(self):
        if self.selected_tile != None:
            uri = self.entry_video_input.get()
            if uri.upper() != "RTMP://...":
                print(uri)
                self.selected_tile.video_source.set_uri(uri)

    def set_selected_tile(self, tile):
        self.selected_tile = tile

        if tile.uri != None:
            self.entry_video_input.delete(0, tk.END)
            self.entry_video_input.insert(0, tile.uri)
        else:
            self.entry_video_input.delete(0, tk.END)
            self.entry_video_input.insert(0, "rtmp://...")

        if tile.audio_enabled == True:
            self.audio_enabled = tk.TRUE

            self.audio_enabled_text.set("Disable Audio")
        else:
            self.audio_enabled = tk.FALSE

            self.audio_enabled_text.set("Enable Audio")
