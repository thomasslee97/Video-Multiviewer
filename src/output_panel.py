import tkinter as tk
from tkinter import ttk

class OutputPanel(tk.Frame):
    '''Creates an output settings panel.

    Attributes:
        output_enabled_text (tk.StringVar): Text to display on output_toggle.
        output_enabled (bool): Whether the output is enabled.
        label_title (tk.Label): Title of the panel.
        lable_output (tk.Label): Lables the URL entry box.
        entry_output_url (tk.Entry): Entry used to input the output URL. Is disabled when the output is enabled.
        button_output_toggle (tk.Button): Button used to toggle the RTMP output.
        video_panel (VideoPlayer): Video panel to control.

    '''

    def __init__(self, x, y, relwidth):
        '''Initialise the output panel.

        Args:
            x (int): x position of the frame.
            y (int): y position of the frame.
            relwidth (float): Relative width of the frame.

        '''

        tk.Frame.__init__(self)
        self.place(x=x, y=y, relwidth=relwidth)

        # Stores the text on the enable/ disable button.
        self.output_enabled_text = tk.StringVar(value="Enable Output")
        # Whether the output is enabled.
        self.output_enabled = False
        
        # Panel title.
        self.label_title = tk.Label(self, text="Output Options", font=("Arial", 14))
        self.label_title.grid(sticky="WE", row=0, column=0)

        # Labels the URL entry field.
        self.label_output = tk.Label(self, text="RTMP Output URL:")
        self.label_output.grid(sticky="WE", row=1, column=0)

        # URL entry field.
        self.entry_output_url = tk.Entry(self, width=20, state=tk.NORMAL)
        self.entry_output_url.grid(sticky="WE", row=1, column=1)

        # Set placeholder text.
        self.entry_output_url.delete(0, tk.END)
        self.entry_output_url.insert(0, "rtmp://...")

        # Add enable/ disable button.
        self.button_output_toggle = tk.Button(self, textvariable=self.output_enabled_text, command=self.toggle_output)
        self.button_output_toggle.grid(sticky="WE", row=1, column=2)

    def toggle_output(self):
        '''Toggles RTMP output on/ off.

        '''

        # Get the url to use
        url = self.entry_output_url.get()
        if url.upper() != "RTMP://...":
            # Switch output.
            self.output_enabled = not self.output_enabled

            # Set button text.
            self.output_enabled_text.set("Disable Output") if self.output_enabled else self.output_enabled_text.set("Enable Output")

            # Call video panel.
            if self.output_enabled:
                self.entry_output_url.config(state=tk.DISABLED)
                self.video_panel.pipeline.enable_output(url)
            else:
                self.entry_output_url.config(state=tk.NORMAL)
                self.video_panel.pipeline.disable_output()

    def link_video_panel(self, panel):
        '''Links the video panel to the settings panel.

        '''

        self.video_panel = panel
