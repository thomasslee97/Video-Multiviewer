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

        # Splits video.
        self.video_tee = Gst.ElementFactory.make("tee", "videotee")
        # Splits audio.
        self.audio_tee = Gst.ElementFactory.make("tee", "audiotee")

        # Consumes video.
        self.video_sink = Gst.ElementFactory.make("autovideosink", "videosink")
        # Consumes audio.
        self.audio_sink = Gst.ElementFactory.make("autoaudiosink", "audiosink")

        # Encode video as x264.
        self.x264_enc = Gst.ElementFactory.make("x264enc", "x264enc")

        # Decode x264 for preview.
        self.decodebin = Gst.ElementFactory.make("decodebin", "decodebin_post_x264")
        self.decodebin.connect('pad-added', self.decode_src_created)

        # FLV muxer.
        self.flvmux = Gst.ElementFactory.make("flvmux", "flvmux")
        self.flvmux.set_property("streamable", True)

        # RTMP sink.
        self.rtmp_sink = Gst.ElementFactory.make("rtmpsink", "rtmpsink")

        # Queues to prevent pipeline blocking.
        self.queue_post_x264_enc = Gst.ElementFactory.make("queue", "queue_post_x264_enc")
        self.queue_pre_decodebin = Gst.ElementFactory.make("queue", "queue_pre_decodebin")
        self.queue_post_decodebin = Gst.ElementFactory.make("queue", "queue_post_decodebin")
        self.queue_pre_flvmux = Gst.ElementFactory.make("queue", "queue_pre_flvmux")
        self.queue_post_flvmux = Gst.ElementFactory.make("queue", "queue_post_flvmux")
        self.queue_audio_sink = Gst.ElementFactory.make("queue", "queue_audio_sink")
        self.queue_audio_flvmux = Gst.ElementFactory.make("queue", "queue_audio_flvmux")

        # Mixer/ compositor.
        self.pipeline.add(self.compositor)
        self.pipeline.add(self.audio_mixer)

        # Video encoding.
        self.pipeline.add(self.x264_enc)
        self.pipeline.add(self.queue_post_x264_enc)
        self.pipeline.add(self.video_tee)

        # Decode x264 for preview.
        self.pipeline.add(self.queue_pre_decodebin)
        self.pipeline.add(self.decodebin)
        self.pipeline.add(self.queue_post_decodebin)

        # Mux audio and video.
        self.pipeline.add(self.queue_pre_flvmux)
        self.pipeline.add(self.flvmux)
        self.pipeline.add(self.queue_post_flvmux)

        # Audio tee.
        self.pipeline.add(self.audio_tee)
        self.pipeline.add(self.queue_audio_sink)
        self.pipeline.add(self.queue_audio_flvmux)

        # Sinks.
        self.pipeline.add(self.video_sink)
        self.pipeline.add(self.audio_sink)
        self.pipeline.add(self.rtmp_sink)

        # Encode video.
        self.compositor.link(self.x264_enc)
        self.x264_enc.link(self.queue_post_x264_enc)
        self.queue_post_x264_enc.link(self.video_tee)

        # Decode video for preview.
        self.video_tee.link(self.queue_pre_decodebin)
        self.queue_pre_decodebin.link(self.decodebin)
        self.queue_post_decodebin.link(self.video_sink)

        # Tee audio.
        self.audio_mixer.link(self.audio_tee)

        # Mux video and audio into FLV stream.
        self.video_tee.link(self.queue_pre_flvmux)
        self.queue_pre_flvmux.link(self.flvmux)
        self.flvmux.link(self.queue_post_flvmux)
        # Audio.
        self.audio_tee.link(self.queue_audio_flvmux)
        self.queue_audio_flvmux.link(self.flvmux)
        # Output.
        self.queue_post_flvmux.link(self.rtmp_sink)
        
        # Audio preview sink.
        self.audio_tee.link(self.queue_audio_sink)
        self.queue_audio_sink.link(self.audio_sink)

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

    def decode_src_created(self, element, pad):
        '''Called when a decode src is created on the decodebin.

        '''

        # Create representation of our video capabilities.
        video_caps = Gst.caps_from_string("video/x-raw")
        
        # Set video pad.
        if Gst.Caps.is_always_compatible(pad.get_current_caps(), video_caps):
            pad.link(self.queue_post_decodebin.get_static_pad("sink"))

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

        # Mute volume.
        mixer_sink.set_property("volume", 0)

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

    def enable_output(self, url):
        '''Enables the RTMP output. Restarts the pipeline.

        Args:
            url (str): URL to stream to.

        '''

        self.stop()
        self.rtmp_sink.set_property("location", str(url))
        self.start()

    def disable_output(self):
        '''Disables the RTMP output. Restarts the pipeline.

        '''

        self.stop()
        self.rtmp_sink.set_property("location", None)
        self.start()
