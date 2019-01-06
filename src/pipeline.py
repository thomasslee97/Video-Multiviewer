import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, GstBase, Gtk, GstVideo

from src.video_source import VideoSource

class Pipeline:
    def __init__(self, widget_id):
        self.widget_id = widget_id

        Gst.init(None)

        self.names = []

        # Video pipeline.
        self.pipeline = Gst.Pipeline.new("player")

        # Video compositor.
        self.compositor = Gst.ElementFactory.make("compositor", "compositor")

        # Audio mixer.
        self.audio_mixer = Gst.ElementFactory.make("audiomixer", "audiomixer")

        # Consumes video.
        self.video_sink = Gst.ElementFactory.make("autovideosink", "videosink")
        # Consumes audio.
        self.audio_sink = Gst.ElementFactory.make("autoaudiosink", "audiosink")

        self.pipeline.add(self.compositor)
        self.pipeline.add(self.audio_mixer)
        self.pipeline.add(self.video_sink)  
        self.pipeline.add(self.audio_sink)

        # vidsrc = "file:///home/tom/media/AnotherWorldSony4k.webm"

        vidsrc = "file:///home/tom/media/in.mkv"
        self.src0 = VideoSource(self.pipeline, vidsrc, "source0")

        self.comp_sink_0 = self.compositor.get_request_pad("sink_%u")
        self.comp_sink_0.set_property("width", 320)
        self.comp_sink_0.set_property("height", 180)
        self.comp_sink_0.set_property("xpos", 0)
        self.comp_sink_0.set_property("ypos", 0)
        self.comp_sink_0.set_property("alpha", 0.5)

        self.mixer_sink_0 = self.audio_mixer.get_request_pad("sink_%u")

        self.src0.video_convert.get_static_pad("src").link(self.comp_sink_0)
        self.src0.audio_convert.get_static_pad("src").link(self.mixer_sink_0)

        self.src1 = VideoSource(self.pipeline, vidsrc, "source1")

        self.comp_sink_1 = self.compositor.get_request_pad("sink_%u")
        self.comp_sink_1.set_property("width", 320)
        self.comp_sink_1.set_property("height", 180)
        self.comp_sink_1.set_property("xpos", 320)
        self.comp_sink_1.set_property("ypos", 0)
        self.comp_sink_1.set_property("alpha", 1.0)

        self.mixer_sink_1 = self.audio_mixer.get_request_pad("sink_%u")

        self.src1.video_convert.get_static_pad("src").link(self.comp_sink_1)
        self.src1.audio_convert.get_static_pad("src").link(self.mixer_sink_1)
        
        self.src2 = VideoSource(self.pipeline, vidsrc, "source2")

        self.comp_sink_2 = self.compositor.get_request_pad("sink_%u")
        self.comp_sink_2.set_property("width", 320)
        self.comp_sink_2.set_property("height", 180)
        self.comp_sink_2.set_property("xpos", 0)
        self.comp_sink_2.set_property("ypos", 180)
        self.comp_sink_2.set_property("alpha", 1.0)

        self.mixer_sink_2 = self.audio_mixer.get_request_pad("sink_%u")

        self.src2.video_convert.get_static_pad("src").link(self.comp_sink_2)
        self.src2.audio_convert.get_static_pad("src").link(self.mixer_sink_2)

        vidsrc = "file:///home/tom/media/AronChupa Little Sis Nora - Rave in the Grave-Zokn4WDPcHE.mkv"

        self.src3 = VideoSource(self.pipeline, vidsrc, "source3")

        self.comp_sink_3 = self.compositor.get_request_pad("sink_%u")
        self.comp_sink_3.set_property("width", 320)
        self.comp_sink_3.set_property("height", 180)
        self.comp_sink_3.set_property("xpos", 320)
        self.comp_sink_3.set_property("ypos", 180)
        self.comp_sink_3.set_property("alpha", 1.0)

        self.mixer_sink_3 = self.audio_mixer.get_request_pad("sink_%u")

        self.src3.video_convert.get_static_pad("src").link(self.comp_sink_3)
        self.src3.audio_convert.get_static_pad("src").link(self.mixer_sink_3)

        self.compositor.link(self.video_sink)
        self.audio_mixer.link(self.audio_sink)

        # Get pipeline bus.
        bus = self.pipeline.get_bus()
        # Add signal watcher.
        bus.add_signal_watch()
        # Enable emission of sync messages.
        bus.enable_sync_message_emission()
        # Call on_sync_message on video sync.
        bus.connect("sync-message::element", self.on_sync_message)
        # Call on_error on error.
        bus.connect("message::error", self.on_error)
        # Call on_state_changed when state changes.
        bus.connect("message::state-changed", self.on_state_change)
    
    def start(self):
        '''Starts the video pipeline.

        '''

        # Set pipline state as playing.
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_sync_message(self, bus, message):
        '''Called when sync message is recieved.

        '''

        # Get message name.
        message_name = message.get_structure().get_name()
        
        if message_name == "prepare-window-handle":
            # Get sink.
            imagesink = message.src
            # Stretch image to aspect ratio.
            imagesink.set_property("force-aspect-ratio", True)
            # Draw image in target frame.
            imagesink.set_window_handle(self.widget_id)

    def on_error(self, bus, message):
        '''Called when an error message is recieved.

        '''

        # Print error and debug info.
        err, dbg = message.parse_error()
        print("ERROR: " + message.src.get_name() + ":" + err.message)
        if dbg:
            print("Debug info:", dbg)

    def on_state_change(self, bus, message):
        '''Called when the state changes.

        '''

        # Print old and new state.
        old, new, pending = message.parse_state_changed()
        print("State change from {0} to {1}".format(Gst.Element.state_get_name(old), Gst.Element.state_get_name(new)))

    def get_unique_name(self, uri):
        uri = str(uri)
        if not (uri in self.names):
            return uri
        else:
            self.get_unique_name(uri + "_1")
