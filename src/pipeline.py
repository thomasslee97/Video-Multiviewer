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
        '''
        self.playbin = Gst.ElementFactory.make("playbin3", "player")
        self.playbin.set_property("uri", "file:///home/tom/media/in.mkv")

        self.videoflip = Gst.ElementFactory.make("videoflip", "videoflip")
        self.videoflip.set_property("method", "horizontal-flip")
        
        # self.playbin.add(self.videoflip)
        self.playbin.link()
        '''

        # Video pipeline.
        self.pipeline = Gst.Pipeline.new("player")

        '''
        # URI decode bin, reads file/rtmp.
        self.uri_decode_bin = Gst.ElementFactory.make("uridecodebin", "decodebin")
        # Call decode_src_added when the file has been loaded.
        self.uri_decode_bin.connect('pad-added', self.decode_src_created)

        # Converts raw video.
        self.video_convert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        # Queues video.
        self.queuevideo = Gst.ElementFactory.make("queue", "queuevideo")
        # Consumes video.
        self.video_sink = Gst.ElementFactory.make("autovideosink", "videosink")

        # Flip video horizontally.
        self.videoflip = Gst.ElementFactory.make("videoflip", "videoflip")
        self.videoflip.set_property("method", "horizontal-flip")

        # Converts raw audio.
        self.audio_convert = Gst.ElementFactory.make("audioconvert", "audioconvert")
        # Queues audio.
        self.queueaudio = Gst.ElementFactory.make("queue", "queueaudio")
        # Consumes audio.
        self.audio_sink = Gst.ElementFactory.make("autoaudiosink", "audiosink")
        
        # Add all objects to pipleine.
        self.pipeline.add(self.uri_decode_bin)
        self.pipeline.add(self.video_convert)
        # self.pipeline.add(self.videoflip)
        self.pipeline.add(self.queuevideo)
        self.pipeline.add(self.video_sink)
        self.pipeline.add(self.audio_convert)
        self.pipeline.add(self.queueaudio)
        self.pipeline.add(self.audio_sink)

        # Link video queue to converter.
        self.queuevideo.link(self.video_convert)
        # Link video converter to video flip.
        self.video_convert.link(self.video_sink)
        # Link video flip to video sink.
        # self.videoflip.link(self.video_sink)
        # Link audio queue to audio converter.
        self.queueaudio.link(self.audio_convert)
        # Link audio converter to audio sink.
        self.audio_convert.link(self.audio_sink)
        '''

        # Consumes video.
        self.video_sink = Gst.ElementFactory.make("autovideosink", "videosink")
        # Consumes audio.
        self.audio_sink = Gst.ElementFactory.make("autoaudiosink", "audiosink")

        self.pipeline.add(self.video_sink)  
        self.pipeline.add(self.audio_sink)

        src = VideoSource(self.pipeline, "", "source")

        src.video_convert.link(self.video_sink)
        src.audio_convert.link(self.audio_sink)

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

        # Load file to play.
        # self.uri_decode_bin.set_property("uri", "file:///home/tom/media/in.mkv")

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

    def decode_src_created(self, element, pad):
        '''Called when a decode source is created.

        '''

        # Create representation of our video capabilities.
        video_caps = Gst.caps_from_string("video/x-raw")

        # Create representation of our audio capabilities.
        audio_caps = Gst.caps_from_string("audio/x-raw")

        # Set audio and video pads.
        if Gst.Caps.is_always_compatible(pad.get_current_caps(), video_caps):
            pad.link(self.queuevideo.get_static_pad("sink"))
        elif Gst.Caps.is_always_compatible(pad.get_current_caps(), audio_caps):
            pad.link(self.queueaudio.get_static_pad("sink"))
