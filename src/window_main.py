import tkinter as tk
from src.pipeline import Pipeline
from src.video_player import VideoPlayer
from src.settings_panel import SettingsPanel
from src.multiview import Tile

PREVIEW_WIDTH = 1280
PREVIEW_HEIGHT = 720

CONTROL_PANEL_HEIGHT = 200

WINDOW_WIDTH = PREVIEW_WIDTH
WINDOW_HEIGHT = PREVIEW_HEIGHT + CONTROL_PANEL_HEIGHT

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.video_panel = VideoPlayer(0, 0, PREVIEW_WIDTH, PREVIEW_HEIGHT)
        self.panel_settings = SettingsPanel(0, PREVIEW_HEIGHT, WINDOW_WIDTH, CONTROL_PANEL_HEIGHT)
        self.video_panel.link_settings_panel(self.panel_settings)

        pad_video, pad_audio, video_source = self.video_panel.pipeline.add_video("", PREVIEW_WIDTH, PREVIEW_HEIGHT, 0, 0)
        tile_root = Tile()
        tile_root.width = PREVIEW_WIDTH
        tile_root.height = PREVIEW_HEIGHT
        tile_root.xpos = 0
        tile_root.ypos = 0
        tile_root.pad_video = pad_video
        tile_root.pad_audio = pad_audio
        tile_root.video_source = video_source
        tile_root.uri = None
        tile_root.audio_enabled = False
        self.video_panel.multiview.add_tile(tile_root)
        self.video_panel.select_tile(tile_root)
