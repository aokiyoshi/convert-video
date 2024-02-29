# pylint: disable=missing-module-docstring
# pylint: disable=import-error
import customtkinter as ctk
from app_class import App

from params import Params, VideoInfo


class PathSelectorFrame(ctk.CTkFrame):
    """PathSelectorFrame"""
    # pylint: disable=too-many-ancestors

    def __init__(self, master):
        # Init ctk frame
        super().__init__(master, bg_color="transparent")
        self.entry = ctk.CTkEntry(
            self, placeholder_text="Path", justify="center")
        self.button = ctk.CTkButton(
            self,
            text="Browse"
        )
        # Init ui elements
        self.entry.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.button.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        # Configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class InputFrame(ctk.CTkFrame):
    """InputFrame"""
    # pylint: disable=too-many-ancestors

    def __init__(self, master, frame_label="Input"):
        # Init ctk frame
        super().__init__(master)

        # Init ui elements
        self.frame_label = ctk.CTkLabel(
            self, text=frame_label, compound="left")
        self.path_selector = PathSelectorFrame(self)

        # Configure elements
        self.frame_label.grid(row=0, padx=0, pady=0)
        self.path_selector.grid(row=1, padx=20, pady=20, sticky="nsew")

        # Configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class ConfigBlock(ctk.CTkFrame):
    """ConfigBlock"""
    # pylint: disable=too-many-ancestors

    def __init__(self, master):
        # Init ctk frame
        super().__init__(master, bg_color="transparent")

        # Init ui elements
        self.input_w = ctk.CTkEntry(self, placeholder_text="Width")
        self.input_h = ctk.CTkEntry(self, placeholder_text="Height")
        self.input_fps = ctk.CTkEntry(self, placeholder_text="FPS")
        self.use_gpu = ctk.CTkCheckBox(self, text="Use GPU")

        # Configure elements
        self.input_w.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.input_h.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.input_fps.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.use_gpu.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # Configure grid system
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)


class ConfigFrame(ctk.CTkFrame):
    """ConfigFrame"""
    # pylint: disable=too-many-ancestors

    def __init__(self, master):
        super().__init__(master)
        self.frame_label = ctk.CTkLabel(
            self, text="Convert Settings", compound="left")
        self.config_block = ConfigBlock(self)
        self.frame_label.grid(row=0, padx=0, pady=0)
        self.config_block.grid(row=1, padx=20, pady=20, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)


class ConvertFrame(ctk.CTkFrame):
    """ConvertFrame"""
    # pylint: disable=too-many-ancestors

    def __init__(self, master):

        # Init ctk frame
        super().__init__(master)

        # Create ui elements
        self.frame_label = ctk.CTkLabel(self, text="Convert", compound="left")
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.button = ctk.CTkButton(
            self,
            text="Convert",
            anchor="right",
        )

        # Configure elements
        self.frame_label.grid(
            row=0, column=0, padx=(0, 0), pady=0, columnspan=4)
        self.progress_bar.grid(row=1, column=0, padx=20,
                               pady=20, sticky="nsew")
        # self.progress_bar.configure(mode="intermediate")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.button.configure(state="disabled") # set convert button disabled by default

        # Configure grid
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)


class MainWindow(ctk.CTk):
    """Main app class"""
    # pylint: disable=too-many-ancestors
    # pylint: disable=too-many-instance-attributes

    def __init__(self, label, logic=App()):
        # Init Ctk root
        super().__init__()

        # Some useful vars
        self.logic = logic
        self.is_closed = False
        self.input_file_exists = False
        self.ouput_file_exists = False

        # Init window
        self.title(label)
        self.resizable(False, False)

        # Input video frame
        self.frame = InputFrame(master=self, frame_label="Input")
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Output video frame
        self.frame_2 = InputFrame(master=self, frame_label="Output")
        self.frame_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Config frame
        self.config_frame = ConfigFrame(master=self)
        self.config_frame.grid(row=2, column=0, padx=10,
                               pady=10, sticky="nsew")

        # Convert frame
        self.convert_frame = ConvertFrame(master=self)
        self.convert_frame.grid(
            row=3, column=0, padx=20, pady=20, sticky="nsew")

        # Configure grid system
        # self.geometry(f"{w}x{h}")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # Commands
        self.convert_frame.button.configure(command=self.get_params)
        self.frame.path_selector.button.configure(command=self.openfile_input)
        self.frame_2.path_selector.button.configure(
            command=self.openfile_output)
        self.convert_frame.button.configure(command=self.convert)

        # Events
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def openfile_input(self):
        """Askopenfilename"""
        # Get path from file dialog
        path = ctk.filedialog.askopenfilename()

        # Return if path empty
        if not path:
            return

        # Set variable
        self.input_file_exists = True

        # If input and output path exist enable button
        if all((self.input_file_exists, self.ouput_file_exists)):
            self.convert_frame.button.configure(state="normal")

        # Get probe
        video_info: VideoInfo = self.logic.get_probe(path)

        # Set values in forms
        self.frame.path_selector.entry.delete(0, 'end')
        self.config_frame.config_block.input_w.delete(0, 'end')
        self.config_frame.config_block.input_h.delete(0, 'end')
        self.config_frame.config_block.input_fps.delete(0, 'end')
        self.config_frame.config_block.input_w.insert(0, video_info.width)
        self.config_frame.config_block.input_h.insert(0, video_info.height)
        self.config_frame.config_block.input_fps.insert(0, video_info.fps)
        self.frame.path_selector.entry.insert(0, path)

    def get_params(self):
        """Get params"""

        return Params(
            input_path=self.frame.path_selector.entry.get(),
            output_path=self.frame_2.path_selector.entry.get(),
            width=self.config_frame.config_block.input_w.get(),
            height=self.config_frame.config_block.input_h.get(),
            fps=self.config_frame.config_block.input_fps.get(),
            gpu=self.config_frame.config_block.use_gpu.get(),
        )

    def openfile_output(self):
        """Askopenfilename"""
        # Open file
        output_file = ctk.filedialog.asksaveasfilename()

        # Return if ouputfile empty
        if not output_file:
            return

        # Set variable
        self.ouput_file_exists = True

        # Check can we enable button for convert
        if all((self.input_file_exists, self.ouput_file_exists)):
            self.convert_frame.button.configure(state="normal")

        # Set entry value
        self.frame_2.path_selector.entry.delete(0, 'end')
        self.frame_2.path_selector.entry.insert(
            index=0,
            string=output_file
        )

    def stop_progress_bar(self, *args, **kwargs): # pylint: disable=unused-argument
        """
        Stop progress bar callback
        We need *args, **kwargs because it passed from
        asyncio coroutine, but we don't use them.
        """
        self.convert_frame.button.configure(state="normal")
        self.convert_frame.progress_bar.stop()

    def set_status_bar_value(
            self, value, max_value, *args, **kwargs
        ): # pylint: disable=unused-argument
        """Set status bar value"""
        self.convert_frame.progress_bar.set(value/max_value)

    def update_ui(self, *args, **kwargs): # pylint: disable=unused-argument
        """
        Update UI. Same logic as stop_progress_bar,
        Function returns is_closed boolean and asyncio loop checks it every 
        time. If True it breaks loop.
        """
        self.update_idletasks()
        self.update()
        return self.is_closed

    def on_closing(self):
        """
        On closing command for Ctk window, when the window closed 
        we set is_closed to True and pass this value to asyncio loop.
        """
        self.is_closed = True

    def convert(self):
        """Bind logic class to convert command"""
        self.convert_frame.button.configure(state="disabled")
        # self.convert_frame.progress_bar.start()
        self.logic.convert(
            self.get_params(),
            self.stop_progress_bar,
            self.set_status_bar_value
        )

    def run(self):
        """
        Call funciton from "logic" class to create and run eventloop
        """
        self.logic.start_app_loop(self.update_ui)
