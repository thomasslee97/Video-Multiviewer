import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, GstBase, Gtk, GstVideo

from src.video_source import VideoSource

class Pipeline:
    '''Stores the properties of a video pipeline.

    Attributes:
        widget_id (str): ID of the widget to draw to.
        names (str): Names used for Gst elements.
        pipeline (Gst Pipeline): Pipeline.
        compositor (Gst Compositor): Video compositor.
        audio_mixer (Gst AudioMixer): Audio mixer.
        video_sink (Gst VideoSink): Video sink.
        audio_sink (Gst AudioSink): Audio sink.

    '''

    def __init__(self, widget_id):
        # Set widget ID to draw to.
        self.widget_id = widget_id

        # Initialise Gst.
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

    def stop(self):
        '''Stops the video pipeline.

        '''

        # Set pipline state as playing.
        self.pipeline.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, message):
        '''Called when sync message is recieved.

        Args:
            bus: Bus the message was sent on.
            message: Message recieved.

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

        Args:
            bus: Bus the message was sent on.
            message: Message recieved.

        '''

        # Print error and debug info.
        err, dbg = message.parse_error()
        print("ERROR: " + message.src.get_name() + ":" + err.message)
        if dbg:
            print("Debug info:", dbg)

    def on_state_change(self, bus, message):
        '''Called when the state changes.

        Args:
            bus: Bus the message was sent on.
            message: Message recieved.

        '''

        # Print old and new state.
        old, new, pending = message.parse_state_changed()
        print("State change from {0} to {1}".format(Gst.Element.state_get_name(old), Gst.Element.state_get_name(new)))

    def add_video(self, uri, width, height, xpos, ypos, comp_sink=None, mixer_sink=None):
        ''' Adds a video to the compositor.

        Params:
            uri (str): URI of the file to load.
            width (int): Width of the video to add.
            height (int): Height of the video to add.
            xpos (int): Position of the video (left edge).
            ypos (int): Position of the video (top edge).
            comp_sink (Gst Pad): Video sink to add the video to.
            mixer_sinl (Gst Pad): Audio sink to add the audio to.

        Returns:
            comp_sink, mixer_sink: (Gst Pad)
            src: (VideoSource)

        '''

        # Create new video source.
        src = VideoSource(self.pipeline, uri, self.get_unique_name(uri))

        # If the sinks have not been defined, get new pads.
        if comp_sink == None and mixer_sink == None:
            comp_sink, mixer_sink = self.get_new_video_pads()

        # Set pad width, height, and position.
        comp_sink.set_property("width", width)
        comp_sink.set_property("height", height)
        comp_sink.set_property("xpos", xpos)
        comp_sink.set_property("ypos", ypos)

        # Link the video and audio pads.
        src.video_convert.get_static_pad("src").link(comp_sink)
        src.audio_convert.get_static_pad("src").link(mixer_sink)

        # Return pads and VideoSource.
        return comp_sink, mixer_sink, src

    def get_new_video_pads(self):
        '''Gets a new set of video and audio pads.

        '''

        video_pad = self.compositor.get_request_pad("sink_%u")
        audio_pad = self.audio_mixer.get_request_pad("sink_%u")

        return video_pad, audio_pad

    def get_unique_name(self, uri):
        '''Returns a unique name that is safe to use to create new Gst elements.

        Args:
            uri (str): URI to use as the base name.

        Returns:
            name (str): Unique name.

        '''

        uri = str(uri)
        if not (uri in self.names):
            self.names.append(uri)
            return uri
        else:
            return self.get_unique_name(uri + "_1")
