import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, GstBase, Gtk, GstVideo

class VideoSource:
    def __init__(self, pipeline, src, name):
        # Video pipeline.
        self.pipeline = pipeline
        self.src = str(src)
        self.name = str(name)

        # URI decode bin, reads file/rtmp.
        self.uri_decode_bin = Gst.ElementFactory.make("uridecodebin", "decodebin" + name)
        # Call decode_src_added when the file has been loaded.
        self.uri_decode_bin.connect('pad-added', self.decode_src_created)

        # Converts raw video.
        self.video_convert = Gst.ElementFactory.make("videoconvert", "videoconvert" + name)
        # Queues video.
        self.queuevideo = Gst.ElementFactory.make("queue", "queuevideo" + name)

        # Converts raw audio.
        self.audio_convert = Gst.ElementFactory.make("audioconvert", "audioconvert" + name)
        # Queues audio.
        self.queueaudio = Gst.ElementFactory.make("queue", "queueaudio" + name)
        
        # Add all objects to pipleine.
        self.pipeline.add(self.uri_decode_bin)
        self.pipeline.add(self.video_convert)
        self.pipeline.add(self.queuevideo)
        self.pipeline.add(self.audio_convert)
        self.pipeline.add(self.queueaudio)

        # Set video to play.
        self.uri_decode_bin.set_property("uri", src)

        # Link video queue to converter.
        self.queuevideo.link(self.video_convert)
        # Link audio queue to audio converter.
        self.queueaudio.link(self.audio_convert)

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