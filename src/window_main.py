import tkinter as tk
from src.pipeline import Pipeline

PREVIEW_WIDTH = 1280
PREVIEW_HEIGHT = 720

CONTROL_PANEL_HEIGHT = 200

WINDOW_WIDTH = PREVIEW_WIDTH
WINDOW_HEIGHT = PREVIEW_HEIGHT + CONTROL_PANEL_HEIGHT

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.audio_enabled_text = tk.StringVar(value="Enable Audio")
        self.preview_stats_text = tk.StringVar(value="View Video Stats")
        self.audio_enabled = False
        self.preview_stats_enabled = False

        self.video_panel = tk.Frame(self, background="black")
        self.video_panel.place(x=0, y=0, width=PREVIEW_WIDTH, height=PREVIEW_HEIGHT)

        panel_control = tk.Frame(self, width=WINDOW_WIDTH, height=CONTROL_PANEL_HEIGHT)
        panel_control.place(x=0, y=PREVIEW_HEIGHT)

        label_video_settings = tk.Label(panel_control, text="Video Settings")
        label_video_settings.grid(sticky="WE")

        label_video_input = tk.Label(panel_control, text="Video Source")
        label_video_input.grid(sticky="WE")

        entry_video_input = tk.Entry(panel_control, width=20)
        entry_video_input.grid(sticky="WE")
        entry_video_input.insert(0, "-i rtmp://...")

        button_audio_toggle = tk.Button(panel_control, textvariable=self.audio_enabled_text, command=self.toggle_audio)
        button_audio_toggle.grid(sticky="WE")

        button_stats_toggle = tk.Button(panel_control, textvariable=self.preview_stats_text, command=self.toggle_stats)
        button_stats_toggle.grid(sticky="WE")

        self.pipeline = Pipeline(self.video_panel.winfo_id())
        self.pipeline.start()

    def action(self, number):
        print(number)

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        
        self.audio_enabled_text.set("Disable Audio") if self.audio_enabled else self.audio_enabled_text.set("Enable Audio")

    def toggle_stats(self):
        self.preview_stats_enabled = not self.preview_stats_enabled
        
        self.preview_stats_text.set("Hide Video Stats") if self.preview_stats_enabled else self.preview_stats_text.set("View Video Stats")
