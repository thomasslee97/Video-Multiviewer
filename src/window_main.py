import tkinter as tk
from src.pipeline import Pipeline
from src.video_player import VideoPlayer
from src.settings_panel import SettingsPanel
from src.multiview import Tile

# Size of the video player.
PREVIEW_WIDTH = 1280
PREVIEW_HEIGHT = 720

# Height of the settings panel.
CONTROL_PANEL_HEIGHT = 200

# Window sizes.
WINDOW_WIDTH = PREVIEW_WIDTH
WINDOW_HEIGHT = PREVIEW_HEIGHT + CONTROL_PANEL_HEIGHT

class MainWindow(tk.Frame):
    '''Stores the main window properties.

    Attributes:
        parent (tk.Tk): Parent window.
        video_panel (VideoPlayer): Video player frame.
        panel_settings (SettingsPanel): Settings frame.

    '''

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # Create video panel.
        self.video_panel = VideoPlayer(0, 0, PREVIEW_WIDTH, PREVIEW_HEIGHT)

        # Create settings panel.
        self.panel_settings = SettingsPanel(WINDOW_WIDTH * 0.01, PREVIEW_HEIGHT, WINDOW_WIDTH * 0.98, CONTROL_PANEL_HEIGHT)

        # Link settings panel to video panel.
        self.video_panel.link_settings_panel(self.panel_settings)

        # Link video panel to settings panel.
        self.panel_settings.link_video_panel(self.video_panel)

        # Add new, empty video to the video panel.
        pad_video, pad_audio, video_source = self.video_panel.pipeline.add_video("", PREVIEW_WIDTH, PREVIEW_HEIGHT, 0, 0)

        # Create root tile covering entire video panel.
        tile_root = Tile(self.video_panel.multiview.get_next_id())
        tile_root.width = PREVIEW_WIDTH
        tile_root.height = PREVIEW_HEIGHT
        tile_root.xpos = 0
        tile_root.ypos = 0
        tile_root.pad_video = pad_video
        tile_root.pad_audio = pad_audio
        tile_root.video_source = video_source
        tile_root.uri = None
        tile_root.audio_enabled = False

        # Add the new tile.
        self.video_panel.multiview.add_tile(tile_root)

        # Select the new tile.
        self.video_panel.select_tile(tile_root)
