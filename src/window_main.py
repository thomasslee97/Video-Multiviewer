import tkinter as tk
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, GstBase, Gtk, GstVideo

PREVIEW_WIDTH = 1280
PREVIEW_HEIGHT = 720

CONTROL_PANEL_HEIGHT = 200

WINDOW_WIDTH = PREVIEW_WIDTH
WINDOW_HEIGHT = PREVIEW_HEIGHT + CONTROL_PANEL_HEIGHT

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.multiview_enabled_text = tk.StringVar(value="Show Multiview")
        self.ffmpeg_enabled_text = tk.StringVar(value="Enable FFMPEG Output")
        self.audio_enabled_text = tk.StringVar(value="Enable Audio")
        self.preview_stats_text = tk.StringVar(value="View Video Stats")
        self.multiview_enabled = False
        self.ffmpeg_enabled = False
        self.audio_enabled = False
        self.preview_stats_enabled = False

        # button_preview = tk.Button(self, text="Preview", command=lambda:self.action(0))
        # button_preview.place(x=0, y=0, width=PREVIEW_WIDTH, height=PREVIEW_HEIGHT)

        '''
        self.player = None
        self.canvas = tk.Canvas(self.video_panel)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        '''

        self.video_panel = tk.Frame(self, background="black")
        self.video_panel.place(x=0, y=0, width=PREVIEW_WIDTH, height=PREVIEW_HEIGHT)

        Gst.init(None)
        self.player = Gst.ElementFactory.make("playbin3", "player")
        fakesink = Gst.ElementFactory.make("fakesink", "novideo")
        self.player.set_property("video-sink", fakesink)

        self.mwin_id = self.video_panel.winfo_id()

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("sync-message::element", self.on_sync_message)

        panel_control = tk.Frame(self, width=WINDOW_WIDTH, height=CONTROL_PANEL_HEIGHT)
        panel_control.place(x=0, y=PREVIEW_HEIGHT)

        panel_settings = tk.Frame(panel_control, width=int(WINDOW_WIDTH / 2), height=CONTROL_PANEL_HEIGHT)
        panel_settings.place(x=0, y=0)

        label_settings = tk.Label(panel_settings, text="Settings")
        # label_settings.place(relx=0, rely=0)
        label_settings.grid(sticky="WE")

        button_multiview_toggle = tk.Button(panel_settings, textvariable=self.multiview_enabled_text, command=self.toggle_multiview)
        # button_multiview_toggle.place(relx=0, rely=0.1)
        button_multiview_toggle.grid(sticky="WE")

        label_ffmpeg_command = tk.Label(panel_settings, text="FFMPEG Command")
        # label_ffmpeg_command.place(relx=0, rely=0.3)
        label_ffmpeg_command.grid(sticky="WE")

        text_ffmpeg_command = tk.Entry(panel_settings, width=20)
        # text_ffmpeg_command.place(relx=0.2, rely=0.3)
        text_ffmpeg_command.grid(sticky="WE")
        text_ffmpeg_command.insert(0, "-c:v libx264 -c:a aac -f flv rtmp://...")

        button_ffmpeg_toggle = tk.Button(panel_settings, textvariable=self.ffmpeg_enabled_text, command=self.toggle_ffmpeg)
        # button_ffmpeg_toggle.place(relx=0, rely=0.5)
        button_ffmpeg_toggle.grid(sticky="WE")

        panel_video_settings = tk.Frame(panel_control, width=int(WINDOW_WIDTH / 2), height=CONTROL_PANEL_HEIGHT)
        panel_video_settings.place(relx=0.5, y=0)

        label_video_settings = tk.Label(panel_video_settings, text="Video Settings")
        # label_settings.place(relx=0, rely=0)
        label_video_settings.grid(sticky="WE")

        label_video_input = tk.Label(panel_video_settings, text="Video Source")
        # label_video_input.place(relx=0, rely=0.1)
        label_video_input.grid(sticky="WE")

        entry_video_input = tk.Entry(panel_video_settings, width=20)
        # entry_video_input.place(relx=0.2, rely=0.1)
        entry_video_input.grid(sticky="WE")
        entry_video_input.insert(0, "-i rtmp://...")

        button_audio_toggle = tk.Button(panel_video_settings, textvariable=self.audio_enabled_text, command=self.toggle_audio)
        # button_audio_toggle.place(relx=0, rely=0.3)
        button_audio_toggle.grid(sticky="WE")

        button_stats_toggle = tk.Button(panel_video_settings, textvariable=self.preview_stats_text, command=self.toggle_stats)
        # button_stats_toggle.place(relx=0, rely=0.5)
        button_stats_toggle.grid(sticky="WE")

        self.start()

    def start(self):
        self.player.set_property('video-sink', None)
        # self.player.set_property("uri", "file:///home/tom/media/in.mkv")
        self.player.set_property("uri", "rtmp://ystvstrm7.york.ac.uk/test/lol")
        self.player.set_state(Gst.State.PLAYING)

    def on_sync_message(self, bus, message):
        message_name = message.get_structure().get_name()
        print(message_name)
        # if message_name == "prepare-xwindow-id":
        if message_name == "prepare-window-handle":
            imagesink = message.src
            # print(dir(imagesink))
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.mwin_id)

    def action(self, number):
        print(number)

    def toggle_multiview(self):
        self.multiview_enabled = not self.multiview_enabled
        
        self.multiview_enabled_text.set("Hide Multiview") if self.multiview_enabled else self.multiview_enabled_text.set("Show Multiview")

    def toggle_ffmpeg(self):
        self.ffmpeg_enabled = not self.ffmpeg_enabled
        
        self.ffmpeg_enabled_text.set("Disable FFMPEG Output") if self.ffmpeg_enabled else self.ffmpeg_enabled_text.set("Enable FFMPEG Output")

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        
        self.audio_enabled_text.set("Disable Audio") if self.audio_enabled else self.audio_enabled_text.set("Enable Audio")

    def toggle_stats(self):
        self.preview_stats_enabled = not self.preview_stats_enabled
        
        self.preview_stats_text.set("Hide Video Stats") if self.preview_stats_enabled else self.preview_stats_text.set("View Video Stats")
