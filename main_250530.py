# app.py

import tkinter as tk
import time
import sys
from flask import Flask, request
import requests
from server_api import post_flow_value, get_flow_value

from tkinter import PhotoImage, Canvas, Button
from pathlib import Path

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x480")
        self.resizable(False, False)
        self.title("VAST KIT")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        self.shared_data = {}

        for F in (HomePage, IntroPage, DiameterPage, FlowRatePage, TargetPage, StabilizingPage, SystemReadyPage, CountdownPage, DurationPage, PhotoPage1, PreviewPage1, MeasurePage1, PhotoPage2, PreviewPage2, MeasurePage2, RestorePage, OverviewPage, EvaluationPage, InfoPage1, InfoPage2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

# Asset paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_HOME = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame0")
ASSETS_FLOW = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame1")
ASSETS_INTRO = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame2")
ASSETS_DIAMETER = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame3")
ASSETS_STABLE = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame5")
ASSETS_READY = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame4")
ASSETS_TIME = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame8")
# ASSETS_PHOTO = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame9")
ASSETS_OVERVIEW = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame10")
ASSETS_EVAL = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets\frame12")

# Assets paths revision (2)
ASSETS_DIAMETER2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame9")
ASSETS_PHOTO1 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame0")
ASSETS_PREV1 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame1")
ASSETS_MEASURE1 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame6")
ASSETS_PHOTO2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame5")
ASSETS_PREV2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame4")
ASSETS_MEASURE2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame7")
ASSETS_OVERVIEW2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame8")
ASSETS_INFO1 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame2")
ASSETS_INFO2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame3")
ASSETS_ANIMATIONS = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_2\frame10")

# Assets paths revision (3)
ASSETS_HOME2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_3\frame1")
ASSETS_INTRO2 = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_3\frame2")
ASSETS_TARGET = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_3\frame3")
ASSETS_RESTORE = OUTPUT_PATH / Path(r"D:\Tkinter-Designer-master\fix\build\assets_3\frame0")


def relative_to_assets_home(path: str) -> Path:
    return ASSETS_HOME / Path(path)

def relative_to_assets_home_2(path: str) -> Path:
    return ASSETS_HOME2 / Path(path)

def relative_to_assets_flow(path: str) -> Path:
    return ASSETS_FLOW / Path(path)

def relative_to_assets_intro(path: str) -> Path:
    return ASSETS_INTRO / Path(path)

def relative_to_assets_intro_2(path: str) -> Path:
    return ASSETS_INTRO2 / Path(path)

def relative_to_assets_diameter(path: str) -> Path:
    return ASSETS_DIAMETER / Path(path)

def relative_to_assets_diameter_2(path: str) -> Path:
    return ASSETS_DIAMETER2 / Path(path)

def relative_to_assets_target(path: str) -> Path:
    return ASSETS_TARGET / Path(path)

def relative_to_assets_stable(path: str) -> Path:
    return ASSETS_STABLE / Path(path)

def relative_to_assets_ready(path: str) -> Path:
    return ASSETS_READY / Path(path)

def relative_to_assets_time(path: str) -> Path:
    return ASSETS_TIME / Path(path)

def relative_to_assets_photo_1(path: str) -> Path:
    return ASSETS_PHOTO1 / Path(path)

def relative_to_assets_preview_1(path: str) -> Path:
    return ASSETS_PREV1 / Path(path)

def relative_to_assets_measure_1(path: str) -> Path:
    return ASSETS_MEASURE1 / Path(path)

def relative_to_assets_photo_2(path: str) -> Path:
    return ASSETS_PHOTO2 / Path(path)

def relative_to_assets_preview_2(path: str) -> Path:
    return ASSETS_PREV2 / Path(path)

def relative_to_assets_measure_2(path: str) -> Path:
    return ASSETS_MEASURE2 / Path(path)

def relative_to_assets_restore(path: str) -> Path:
    return ASSETS_RESTORE / Path(path)

def relative_to_assets_overview(path: str) -> Path:
    return ASSETS_OVERVIEW / Path(path)

def relative_to_assets_overview_2(path: str) -> Path:
    return ASSETS_OVERVIEW2 / Path(path)

def relative_to_assets_eval(path: str) -> Path:
    return ASSETS_EVAL / Path(path)

def relative_to_assets_info_1(path: str) -> Path:
    return ASSETS_INFO1 / Path(path)

def relative_to_assets_info_2(path: str) -> Path:
    return ASSETS_INFO2 / Path(path)

def relative_to_assets_animations(path: str) -> Path:
    return ASSETS_ANIMATIONS / Path(path)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.canvas.bind("<Button-1>", lambda e: controller.show_frame("IntroPage"))

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_home("image_1.png"))
        image_1 = self.canvas.create_image(
            535.0,
            361.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_home("image_2.png"))
        image_2 = self.canvas.create_image(
            399.0,
            228.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_home("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            240.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_home("image_4.png"))
        image_4 = self.canvas.create_image(
            401.0,
            228.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_home_2("image_5.png"))
        image_5 = self.canvas.create_image(
            397.0,
            270.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_home("image_6.png"))
        image_6 = self.canvas.create_image(
            401.0,
            444.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_home("image_7.png"))
        image_7 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_home("image_8.png"))
        image_8 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_8
        )

        #self.bind_all("<Button-1>", lambda e: controller.show_frame("FlowRatePage"))

class IntroPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_intro_2("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_intro_2("image_2.png"))
        image_2 = self.canvas.create_image(
            692.0,
            382.0,
            image=self.image_image_2
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_intro_2("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=642.0,
            y=347.0,
            width=100.0,
            height=70.0
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_intro_2("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_intro_2("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_intro_2("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_intro_2("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_intro_2("image_7.png"))
        image_7 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_intro_2("image_8.png"))
        image_8 = self.canvas.create_image(
            405.0,
            240.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_intro_2("image_9.png"))
        image_9 = self.canvas.create_image(
            569.0,
            240.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_intro_2("image_10.png"))
        image_10 = self.canvas.create_image(
            230.0,
            121.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_intro_2("image_11.png"))
        image_11 = self.canvas.create_image(
            165.0,
            167.0,
            image=self.image_image_11
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets_intro_2("image_12.png"))
        image_11 = self.canvas.create_image(
            364.0,
            312.0,
            image=self.image_image_12
        )

        self.image_image_13 = PhotoImage(
            file=relative_to_assets_intro_2("image_13.png"))
        image_11 = self.canvas.create_image(
            230.0,
            240.0,
            image=self.image_image_13
        )

        button_1.config(command=lambda: controller.show_frame("DiameterPage"))

class DiameterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_diameter("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_diameter("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_diameter("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_diameter("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_diameter("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_diameter("image_6.png"))
        image_6 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_diameter("image_7.png"))
        image_7 = self.canvas.create_image(
            400.0,
            165.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_diameter("image_8.png"))
        image_8 = self.canvas.create_image(
            163.0,
            263.0,
            image=self.image_image_8
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_diameter("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=84.0,
            y=225.0,
            width=158.0,
            height=79.0
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_diameter_2("image_9.png"))
        image_9 = self.canvas.create_image(
            400.0,
            263.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_diameter_2("image_10.png"))
        image_10 = self.canvas.create_image(
            637.0,
            263.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_diameter_2("image_11.png"))
        image_11 = self.canvas.create_image(
            400.0,
            321.0,
        image=self.image_image_11
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets_diameter_2("image_12.png"))
        image_12 = self.canvas.create_image(
            638.0,
            321.0,
            image=self.image_image_12
        )

        button_1.config(command=lambda: controller.show_frame("FlowRatePage"))

class FlowRatePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.text_var = ""

        def update_text(value):
            self.text_var += str(value)
            self.canvas.itemconfig(self.text_display, text=self.text_var)

        def delete_last():
            self.text_var = self.text_var[:-1]
            self.canvas.itemconfig(self.text_display, text=self.text_var)

        def flash_invalid_input():
            self.canvas.itemconfig(self.warning_display, text="out of range", fill="red")
            steps = 2
            delay = 1000  # milliseconds

            def flash(step):
                if step < steps:
                    color = "red" if step % 2 == 0 else ""  # Toggle visibility
                    self.canvas.itemconfig(self.warning_display, fill=color)
                    self.after(delay, lambda: flash(step + 1))
                else:
                    self.canvas.itemconfig(self.warning_display, text="")  # Clear after flashing

            flash(0)

            # Fade the input color
            steps_fade = 30

            def fade(step):
                if step <= steps_fade:
                    progress = step / steps_fade
                    r = int(255 * (1 - progress))
                    hex_color = f'#{r:02x}0000'
                    self.canvas.itemconfig(self.text_display, fill=hex_color)
                    self.after(25, lambda: fade(step + 1))
                else:
                    self.canvas.itemconfig(self.text_display, fill="black")

            fade(0)

        def validate_and_proceed():
            try:
                value = int(self.text_var)
                if 31 <= value <= 61:
                    # Send to localhost server
                    try:
                        post_flow_value(value)
                        print("Server response:", value)
                    except requests.exceptions.RequestException as e:
                        print("Error sending data:", e)

                    # Proceed to next frame
                    self.controller.show_frame("TargetPage")
                else:
                    flash_invalid_input()
            except ValueError:
                flash_invalid_input()

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_flow("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_flow("image_2.png"))
        image_2 = self.canvas.create_image(
            566.0,
            127.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_flow("image_3.png"))
        image_3 = self.canvas.create_image(
            567.0,
            290.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_flow("image_4.png"))
        image_4 = self.canvas.create_image(
            566.0,
            165.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_flow("image_5.png"))
        image_5 = self.canvas.create_image(
            98.0,
            127.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_flow("image_6.png"))
        image_6 = self.canvas.create_image(
            198.0,
            127.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_flow("image_7.png"))
        image_7 = self.canvas.create_image(
            298.0,
            127.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_flow("image_8.png"))
        image_8 = self.canvas.create_image(
            98.0,
            212.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_flow("image_9.png"))
        image_9 = self.canvas.create_image(
            198.0,
            212.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_flow("image_10.png"))
        image_10 = self.canvas.create_image(
            298.0,
            212.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_flow("image_11.png"))
        image_11 = self.canvas.create_image(
            98.0,
            297.0,
            image=self.image_image_11
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets_flow("image_12.png"))
        image_12 = self.canvas.create_image(
            198.0,
            297.0,
            image=self.image_image_12
        )

        self.image_image_13 = PhotoImage(
            file=relative_to_assets_flow("image_13.png"))
        image_13 = self.canvas.create_image(
            298.0,
            297.0,
            image=self.image_image_13
        )

        self.image_image_14 = PhotoImage(
            file=relative_to_assets_flow("image_14.png"))
        image_14 = self.canvas.create_image(
            198.0,
            382.0,
            image=self.image_image_14
        )

        self.image_image_15 = PhotoImage(
            file=relative_to_assets_flow("image_15.png"))
        image_15 = self.canvas.create_image(
            298.0,
            382.0,
            image=self.image_image_15
        )

        self.image_image_16 = PhotoImage(
            file=relative_to_assets_flow("image_16.png"))
        image_16 = self.canvas.create_image(
            566.0,
            227.0,
            image=self.image_image_16
        )

        self.image_image_17 = PhotoImage(
            file=relative_to_assets_flow("image_17.png"))
        image_17 = self.canvas.create_image(
            692.0,
            382.0,
            image=self.image_image_17
        )

        self.image_image_18 = PhotoImage(
            file=relative_to_assets_flow("image_18.png"))
        image_18 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_18
        )

        self.image_image_19 = PhotoImage(
            file=relative_to_assets_flow("image_19.png"))
        image_19 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_19
        )

        self.image_image_20 = PhotoImage(
            file=relative_to_assets_flow("image_20.png"))
        image_20 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_20
        )

        self.image_image_21 = PhotoImage(
            file=relative_to_assets_flow("image_21.png"))
        image_21 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_21
        )

        self.image_image_22 = PhotoImage(
            file=relative_to_assets_flow("image_22.png"))
        image_22 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_22
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_flow("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(1),
            relief="flat"
        )
        button_1.place(
            x=58.0,
            y=92.0,
            width=80.0,
            height=70.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_flow("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(2),
            relief="flat"
        )
        button_2.place(
            x=158.0,
            y=92.0,
            width=80.0,
            height=70.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets_flow("button_3.png"))
        button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(3),
            relief="flat"
        )
        button_3.place(
            x=258.0,
            y=92.0,
            width=80.0,
            height=70.0
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets_flow("button_4.png"))
        button_4 = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(4),
            relief="flat"
        )
        button_4.place(
            x=58.0,
            y=177.0,
            width=80.0,
            height=70.0
        )

        self.button_image_5 = PhotoImage(
            file=relative_to_assets_flow("button_5.png"))
        button_5 = Button(
            self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(5),
            relief="flat"
        )
        button_5.place(
            x=158.0,
            y=177.0,
            width=80.0,
            height=70.0
        )

        self.button_image_6 = PhotoImage(
            file=relative_to_assets_flow("button_6.png"))
        button_6 = Button(
            self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(6),
            relief="flat"
        )
        button_6.place(
            x=258.0,
            y=177.0,
            width=80.0,
            height=70.0
        )

        self.button_image_7 = PhotoImage(
            file=relative_to_assets_flow("button_7.png"))
        button_7 = Button(
            self,
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(7),
            relief="flat"
        )
        button_7.place(
            x=58.0,
            y=262.0,
            width=80.0,
            height=70.0
        )

        self.button_image_8 = PhotoImage(
            file=relative_to_assets_flow("button_8.png"))
        button_8 = Button(
            self,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(8),
            relief="flat"
        )
        button_8.place(
            x=158.0,
            y=262.0,
            width=80.0,
            height=70.0
        )

        self.button_image_9 = PhotoImage(
            file=relative_to_assets_flow("button_9.png"))
        button_9 = Button(
            self,
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(9),
            relief="flat"
        )
        button_9.place(
            x=258.0,
            y=262.0,
            width=80.0,
            height=70.0
        )

        self.button_image_10 = PhotoImage(
            file=relative_to_assets_flow("button_10.png"))
        button_10 = Button(
            self,
            image=self.button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: update_text(0),
            relief="flat"
        )
        button_10.place(
            x=158.0,
            y=347.0,
            width=80.0,
            height=70.0
        )

        self.button_image_11 = PhotoImage(
            file=relative_to_assets_flow("button_11.png"))
        button_11 = Button(
            self,
            image=self.button_image_11,
            borderwidth=0,
            highlightthickness=0,
            command=delete_last,
            relief="flat"
        )
        button_11.place(
            x=258.0,
            y=347.0,
            width=80.0,
            height=70.0
        )

        self.image_image_16 = PhotoImage(
            file=relative_to_assets_flow("image_16.png"))
        image_4 = self.canvas.create_image(
            566.0,
            227.0,
            image=self.image_image_16
        )

        self.image_image_17 = PhotoImage(
            file=relative_to_assets_flow("image_17.png"))
        image_17 = self.canvas.create_image(
            692.0,
            382.0,
            image=self.image_image_17
        )

        self.button_image_12 = PhotoImage(
            file=relative_to_assets_flow("button_12.png"))
        button_12 = Button(
            self,
            image=self.button_image_12,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        button_12.place(
            x=642.0,
            y=347.0,
            width=100.0,
            height=70.0
        )

        self.image_image_18 = PhotoImage(
            file=relative_to_assets_flow("image_18.png"))
        image_5 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_18
        )

        self.image_image_19 = PhotoImage(
            file=relative_to_assets_flow("image_19.png"))
        image_6 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_19
        )

        self.image_image_20 = PhotoImage(
            file=relative_to_assets_flow("image_20.png"))
        image_7 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_20
        )

        self.image_image_21 = PhotoImage(
            file=relative_to_assets_flow("image_21.png"))
        image_8 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_21
        )

        self.image_image_22 = PhotoImage(
            file=relative_to_assets_flow("image_22.png"))
        image_9 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_22
        )

        # Create a text display area
        self.text_display = self.canvas.create_text(
            565.0,
            225.0,
            anchor="center",
            text=self.text_var,
            fill="#000000",
            font=("Inter SemiBold", 30 * -1)
        )

        self.warning_display = self.canvas.create_text(
            565.0,
            252.0,
            anchor="center",
            text="",
            fill="red",
            font=("Inter Bold", 15 * -1)
        )

        button_12.config(command=validate_and_proceed)

    def on_show(self):
        self.text_var = ""
        self.canvas.itemconfig(self.text_display, text=self.text_var)
        self.canvas.itemconfig(self.text_display, fill="black")  # Reset text color too if needed
    
class TargetPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_target("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_target("image_2.png"))
        image_2 = self.canvas.create_image(
            692.0,
            382.0,
            image=self.image_image_2
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_target("button_1.png"))
        button_1 = Button(
            self, 
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=642.0,
            y=347.0,
            width=100.0,
            height=70.0
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_target("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_target("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_target("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_target("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_target("image_7.png"))
        image_7 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_target("image_8.png"))
        image_8 = self.canvas.create_image(
            132.0,
            143.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_target("image_9.png"))
        image_9 = self.canvas.create_image(
            447.0,
            143.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_target("image_10.png"))
        image_10 = self.canvas.create_image(
            121.0,
            206.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_target("image_11.png"))
        image_11 = self.canvas.create_image(
            126.0,
            247.0,
            image=self.image_image_11
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets_target("image_12.png"))
        image_12 = self.canvas.create_image(
            94.0,
            287.0,
            image=self.image_image_12
        )

        self.canvas.create_rectangle(
            222.0,
            190.0,
            284.0,
            222.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            252.0,
            205.0,
            anchor="center",
            text="1",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.image_image_13 = PhotoImage(
            file=relative_to_assets_target("image_13.png"))
        image_13 = self.canvas.create_image(
            315.0,
            206.0,
            image=self.image_image_13
        )

        self.image_image_14 = PhotoImage(
            file=relative_to_assets_target("image_14.png"))
        image_14 = self.canvas.create_image(
            315.0,
            247.0,
            image=self.image_image_14
        )

        self.image_image_15 = PhotoImage(
            file=relative_to_assets_target("image_15.png"))
        image_15 = self.canvas.create_image(
            329.0,
            288.0,
            image=self.image_image_15
        )

        self.canvas.create_rectangle(
            222.0,
            231.0,
            284.0,
            263.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            252.0,
            246.0,
            anchor="center",
            text="0.1",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.canvas.create_rectangle(
            222.0,
            272.0,
            284.0,
            304.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            252.0,
            287.0,
            anchor="center",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.image_image_16 = PhotoImage(
            file=relative_to_assets_target("image_16.png"))
        image_16 = self.canvas.create_image(
            462.0,
            206.0,
            image=self.image_image_16
        )

        self.image_image_17 = PhotoImage(
            file=relative_to_assets_target("image_17.png"))
        self.image_17 = self.canvas.create_image(
            440.0,
            247.0,
            image=self.image_image_17
        )

        self.image_image_18 = PhotoImage(
            file=relative_to_assets_target("image_18.png"))
        self.image_18 = self.canvas.create_image(
            437.0,
            287.0,
            image=self.image_image_18
        )

        self.canvas.create_rectangle(
            541.0,
            190.0,
            603.0,
            222.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            572.0,
            205.0,
            anchor="center",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.image_image_19 = PhotoImage(
            file=relative_to_assets_target("image_19.png"))
        self.image_19 = self.canvas.create_image(
            721.0,
            206.0,
            image=self.image_image_19
        )

        self.image_image_20 = PhotoImage(
            file=relative_to_assets_target("image_20.png"))
        self.image_20 = self.canvas.create_image(
            617.0,
            206.0,
            image=self.image_image_20
        )

        self.image_image_21 = PhotoImage(
            file=relative_to_assets_target("image_21.png"))
        self.image_21 = self.canvas.create_image(
            617.0,
            246.0,
            image=self.image_image_21
        )

        self.image_image_22 = PhotoImage(
            file=relative_to_assets_target("image_22.png"))
        self.image_22 = self.canvas.create_image(
            735.0,
            247.0,
            image=self.image_image_22
        )

        self.image_image_23 = PhotoImage(
            file=relative_to_assets_target("image_23.png"))
        self.image_23 = self.canvas.create_image(
            634.0,
            288.0,
            image=self.image_image_23
        )

        self.canvas.create_rectangle(
            541.0,
            231.0,
            603.0,
            263.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            572.0,
            246.0,
            anchor="center",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.canvas.create_rectangle(
            541.0,
            272.0,
            603.0,
            304.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            572.0,
            287.0,
            anchor="center",
            text="20",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.canvas.create_rectangle(
            631.0,
            190.0,
            693.0,
            222.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            661.0,
            205.0,
            anchor="center",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.canvas.create_rectangle(
            631.0,
            231.0,
            693.0,
            263.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            661.0,
            246.0,
            anchor="center",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 18 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_target("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=58.0,
            y=347.0,
            width=100.0,
            height=70.0
        )

        button_1.config(command=lambda: controller.show_frame("StabilizingPage"))
        button_2.config(command=lambda: controller.show_frame("DiameterPage"))

class StabilizingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        # def flow_stable()

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        #self.canvas.bind("<Button-1>", lambda e: controller.show_frame("SystemReadyPage"))

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_stable("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_stable("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_stable("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_stable("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_stable("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_stable("image_6.png"))
        image_6 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_6
        )

        self.frames = [
            PhotoImage(file=relative_to_assets_animations(f"image_{i}.png"))
            for i in range(1, 12)
        ]

    def on_show(self):
        self.image_on_canvas = self.canvas.create_image(399.0, 240.0, image=self.frames[0])

        self.start_time = time.time()
        self.frame_index = 0

        self.animate()

    def animate(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time < 4:  # loop for 10 seconds
            self.canvas.itemconfig(self.image_on_canvas, image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.after(200, self.animate)  # 0.2 seconds per frame
        else:
            self.controller.show_frame("SystemReadyPage")

class SystemReadyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_ready("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_ready("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_ready("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_ready("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_ready("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_ready("image_6.png"))
        image_6 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_ready("image_7.png"))
        image_7 = self.canvas.create_image(
            400.0,
            138.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_ready("image_8.png"))
        image_8 = self.canvas.create_image(
            472.0,
            398.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_ready("image_9.png"))
        image_9 = self.canvas.create_image(
            472.0,
            374.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_ready("image_10.png"))
        image_10 = self.canvas.create_image(
            108.0,
            382.0,
            image=self.image_image_10
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_ready("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=58.0,
            y=347.0,
            width=100.0,
            height=70.0
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_ready("image_11.png"))
        image_11 = self.canvas.create_image(
            400.0,
            226.0,
            image=self.image_image_11
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_ready("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        button_2.place(
            x=150.0,
            y=176.0,
            width=500.0,
            height=100.0
        )

        self.canvas.create_text(
            610.0,
            400.0,
            anchor="center",
            text="20",
            fill="#000000",
            font=("Inter SemiBold", 20 * -1)
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets_ready("image_12.png"))
        image_12 = self.canvas.create_image(
            693.0,
            398.0,
            image=self.image_image_12
        )

        self.nilai_flow_display = self.canvas.create_text(
            610.0,
            375.0,
            anchor="center",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 20 * -1)
        )

        self.image_image_13 = PhotoImage(
            file=relative_to_assets_ready("image_13.png"))
        image_13 = self.canvas.create_image(
            693.0,
            374.0,
            image=self.image_image_13
        )

        button_1.config(command=lambda: controller.show_frame("FlowRatePage"))
        button_2.config(command=lambda: controller.show_frame("CountdownPage"))


    def update_nilai_flow(self):
        try:
            self.nilai_flow = get_flow_value()   
            print("Get response:", self.nilai_flow)
            self.canvas.itemconfig(self.nilai_flow_display, text=self.nilai_flow)
            self.controller.shared_data["desired_flow"] = self.nilai_flow
        except requests.exceptions.RequestException:
            self.canvas.itemconfig(self.nilai_flow_display, text="Connection Error")

    def on_show(self):
        self.update_nilai_flow()

class CountdownPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_stable("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_stable("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_stable("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_stable("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_stable("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_stable("image_6.png"))
        image_6 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_6
        )

        self.frames = [
            PhotoImage(file=relative_to_assets_animations(f"image_{i}.png"))
            for i in range(26, 21, -1)
        ]

    def on_show(self):
        self.animation_image = self.canvas.create_image(399.0, 240.0, image=self.frames[0])

        self.frame_index = 0

        self.animate()

    def animate(self):
        if self.frame_index < len(self.frames):
            # Update image
            self.canvas.itemconfig(self.animation_image, image=self.frames[self.frame_index])
            self.frame_index += 1
            self.after(1000, self.animate)  # 1 second = 1000 ms
        else:
            self.controller.show_frame("DurationPage")

class DurationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.start_time = None
        self.running = False

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_time("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_time("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_time("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_time("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_time("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_time("image_6.png"))
        image_6 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_time("image_7.png"))
        image_7 = self.canvas.create_image(
            402.0,
            183.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_time("image_8.png"))
        image_8 = self.canvas.create_image(
            225.0,
            183.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_time("image_9.png"))
        image_9 = self.canvas.create_image(
            539.0,
            309.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_time("image_10.png"))
        image_10 = self.canvas.create_image(
            318.0,
            309.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_time("image_11.png"))
        image_11 = self.canvas.create_image(
            400.0,
            382.0,
            image=self.image_image_11
        )

        # Stopwatch
        self.stopwatch_text = self.canvas.create_text(
            360.0,
            145.0,
            anchor="nw",
            text="00:00:00",
            fill="#000000",
            font=("RobotoMono Bold", 60 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_time("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_duration,
            relief="flat"
        )
        button_1.place(
            x=250.0,
            y=347.0,
            width=300.0,
            height=70.0
        )

        self.canvas.create_text(
            426.0,
            297.0,
            anchor="nw",
            text=" ",
            fill="#000000",
            font=("Inter SemiBold", 20 * -1)
        )

    def on_show(self):
        self.start_time = time.time()
        self.running = True
        self.update_stopwatch()
        
        desired_flow = self.controller.shared_data.get("desired_flow", "0")
        print("Desired flow:", desired_flow)

    def update_stopwatch(self):
        if self.running:
            elapsed = int(time.time() - self.start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.canvas.itemconfig(self.stopwatch_text, text=time_string)
            self.after(1000, self.update_stopwatch)

    def save_duration(self):
        duration = self.canvas.itemcget(self.stopwatch_text, "text")
        print("Saved Duration:", duration)
        self.running = False  # stop updating
        self.controller.shared_data["duration"] = duration
        self.controller.show_frame("PhotoPage1")

class PhotoPage1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_photo_1("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_photo_1("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_photo_1("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_photo_1("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_photo_1("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_photo_1("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_photo_1("image_7.png"))
        image_7 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_7
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_photo_1("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=276.0,
            y=372.0,
            width=248.0,
            height=70.0
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_photo_1("image_8.png"))
        image_8 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_8
        )

        button_1.config(command=lambda: controller.show_frame("PreviewPage1"))

class PreviewPage1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_preview_1("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_preview_1("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_preview_1("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_preview_1("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_preview_1("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_preview_1("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_preview_1("image_7.png"))
        image_7 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_preview_1("image_8.png"))
        image_8 = self.canvas.create_image(
            108.0,
            406.0,
            image=self.image_image_8
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_preview_1("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=68.0,
            y=371.0,
            width=80.0,
            height=70.0
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_preview_1("image_9.png"))
        image_9 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_9
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_preview_1("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=642.0,
            y=371.0,
            width=100.0,
            height=70.0
        )

        button_1.config(command=lambda: controller.show_frame("PhotoPage1"))
        button_2.config(command=lambda: controller.show_frame("PhotoPage2"))

class PhotoPage2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_photo_2("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_photo_2("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_photo_2("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_photo_2("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_photo_2("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_photo_2("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_photo_2("image_7.png"))
        image_7 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_7
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_photo_2("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=276.0,
            y=372.0,
            width=248.0,
            height=70.0
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_photo_2("image_8.png"))
        image_8 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_8
        )

        button_1.config(command=lambda: controller.show_frame("PreviewPage2"))

class PreviewPage2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_preview_2("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_preview_2("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_preview_2("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_preview_2("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_preview_2("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_preview_2("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_preview_2("image_7.png"))
        image_7 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_preview_2("image_8.png"))
        image_8 = self.canvas.create_image(
            108.0,
            406.0,
            image=self.image_image_8
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_preview_2("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=68.0,
            y=371.0,
            width=80.0,
            height=70.0
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_preview_2("image_9.png"))
        image_9 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_9
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_preview_2("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=642.0,
            y=371.0,
            width=100.0,
            height=70.0
        )

        button_1.config(command=lambda: controller.show_frame("PhotoPage2"))
        button_2.config(command=lambda: controller.show_frame("MeasurePage1"))

class MeasurePage1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_measure_1("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_measure_1("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_preview_2("button_2.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=680.0,
            y=356.0,
            width=100.0,
            height=70.0
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_measure_1("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_measure_1("image_4.png"))
        image_4 = self.canvas.create_image(
            400.0,
            460.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_measure_1("image_5.png"))
        image_5 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_measure_1("image_6.png"))
        image_6 = self.canvas.create_image(
            400.0,
            460.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_measure_1("image_7.png"))
        image_7 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_measure_1("image_8.png"))
        image_8 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_measure_1("image_9.png"))
        image_9 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_measure_1("image_10.png"))
        image_10 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_10
        )

        button_1.config(command=lambda: controller.show_frame("MeasurePage2"))

class MeasurePage2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_measure_2("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_measure_2("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_preview_2("button_2.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=680.0,
            y=356.0,
            width=100.0,
            height=70.0
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_measure_2("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_measure_2("image_4.png"))
        image_4 = self.canvas.create_image(
            400.0,
            460.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_measure_2("image_5.png"))
        image_5 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_measure_2("image_6.png"))
        image_6 = self.canvas.create_image(
            400.0,
            460.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_measure_2("image_7.png"))
        image_7 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_measure_2("image_8.png"))
        image_8 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_measure_2("image_9.png"))
        image_9 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_measure_2("image_10.png"))
        image_10 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_10
        )

        button_1.config(command=lambda: controller.show_frame("RestorePage"))

class RestorePage(tk.Frame): 
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_restore("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_restore("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_restore("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_restore("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_restore("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_restore("image_6.png"))
        image_6 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_restore("image_7.png"))
        image_7 = self.canvas.create_image(
            247.0,
            248.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_restore("image_8.png"))
        image_8 = self.canvas.create_image(
            552.0,
            248.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_restore("image_9.png"))
        image_9 = self.canvas.create_image(
            288.0,
            267.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_restore("image_10.png"))
        image_10 = self.canvas.create_image(
            248.0,
            231.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_restore("image_11.png"))
        image_11 = self.canvas.create_image(
            400.0,
            141.0,
            image=self.image_image_11
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets_restore("image_12.png"))
        image_12 = self.canvas.create_image(
            552.0,
            229.0,
            image=self.image_image_12
        )

        self.canvas.create_text(
            202.0,
            266.0,
            anchor="center",
            text="10",
            fill="#000000",
            font=("Inter SemiBold", 20 * -1)
        )

        self.canvas.create_text(
            550.0,
            265.0,
            anchor="center",
            text="23:59:59",
            fill="#000000",
            font=("RobotoMono Bold", 30 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_restore("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=205.0,
            y=351.0,
            width=389.0,
            height=70.0
        )

        button_1.config(command=lambda: controller.show_frame("OverviewPage"))

    def on_show(self):
        duration = self.controller.shared_data.get("duration", "00:00:00")
        self.canvas.itemconfig(self.duration_text_id, text=duration)

class OverviewPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_overview_2("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_overview_2("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_overview_2("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_overview_2("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_overview_2("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_overview_2("image_6.png"))
        image_6 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_overview_2("image_7.png"))
        image_7 = self.canvas.create_image(
            400.0,
            94.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_overview_2("image_8.png"))
        image_8 = self.canvas.create_image(
            171.0,
            197.0,
            image=self.image_image_8
        )

        self.canvas.create_text(
            107.0,
            183.0,
            anchor="nw",
            text="100%",
            fill="#000000",
            font=("Inter SemiBold", 50 * -1)
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_overview_2("image_9.png"))
        image_9 = self.canvas.create_image(
            519.0,
            188.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_overview_2("image_10.png"))
        image_10 = self.canvas.create_image(
            171.0,
            306.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets_overview_2("image_11.png"))
        image_11 = self.canvas.create_image(
            519.0,
            296.0,
            image=self.image_image_11
        )

        self.canvas.create_text(
            339.0,
            178.0,
            anchor="nw",
            text="100%",
            fill="#000000",
            font=("Inter SemiBold", 40 * -1)
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets_overview_2("image_12.png"))
        image_12 = self.canvas.create_image(
            173.0,
            167.0,
            image=self.image_image_12
        )

        self.image_image_13 = PhotoImage(
            file=relative_to_assets_overview_2("image_13.png"))
        image_13 = self.canvas.create_image(
            392.0,
            163.0,
            image=self.image_image_13
        )

        self.canvas.create_text(
            339.0,
            283.0,
            anchor="nw",
            text="100%",
            fill="#000000",
            font=("Inter SemiBold", 40 * -1)
        )

        self.image_image_14 = PhotoImage(
            file=relative_to_assets_overview_2("image_14.png"))
        image_14 = self.canvas.create_image(
            393.0,
            272.0,
            image=self.image_image_14
        )

        self.image_image_15 = PhotoImage(
            file=relative_to_assets_overview_2("image_15.png"))
        image_15 = self.canvas.create_image(
            572.0,
            188.0,
            image=self.image_image_15
        )

        self.canvas.create_text(
            675.0,
            179.0,
            anchor="nw",
            text="4/10",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.image_image_16 = PhotoImage(
            file=relative_to_assets_overview_2("image_16.png"))
        image_16 = self.canvas.create_image(
            578.0,
            212.0,
            image=self.image_image_16
        )

        self.canvas.create_text(
            675.0,
            203.0,
            anchor="nw",
            text="6/10",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.image_image_17 = PhotoImage(
            file=relative_to_assets_overview_2("image_17.png"))
        image_17 = self.canvas.create_image(
            538.0,
            285.0,
            image=self.image_image_17
        )

        self.image_image_18 = PhotoImage(
            file=relative_to_assets_overview_2("image_18.png"))
        image_18 = self.canvas.create_image(
            685.0,
            285.0,
            image=self.image_image_18
        )

        self.image_image_19 = PhotoImage(
            file=relative_to_assets_overview_2("image_19.png"))
        image_19 = self.canvas.create_image(
            534.0,
            310.0,
            image=self.image_image_19
        )

        self.canvas.create_text(
            598.0,
            301.0,
            anchor="nw",
            text="12234",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.canvas.create_text(
            598.0,
            276.0,
            anchor="nw",
            text="12234",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.image_image_20 = PhotoImage(
            file=relative_to_assets_overview_2("image_20.png"))
        image_20 = self.canvas.create_image(
            685.0,
            310.0,
            image=self.image_image_20
        )

        self.duration_text_id = self.canvas.create_text(
            170.0,
            300.0,
            anchor="center",
            text="00:00:00",
            fill="#000000",
            font=("RobotoMono Bold", 30 * -1)
        )

        self.image_image_21 = PhotoImage(
            file=relative_to_assets_overview_2("image_21.png"))
        image_21 = self.canvas.create_image(
            225.0,
            390.0,
            image=self.image_image_21
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_overview_2("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=58.0,
            y=355.0,
            width=335.0,
            height=70.0
        )

        self.image_image_22 = PhotoImage(
            file=relative_to_assets_overview_2("image_22.png"))
        image_22 = self.canvas.create_image(
            574.0,
            390.0,
            image=self.image_image_22
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_overview_2("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=407.0,
            y=355.0,
            width=335.0,
            height=70.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets_overview_2("button_3.png"))
        button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        button_3.place(
            x=648.0,
            y=143.0,
            width=82.0,
            height=18.0
        )

        button_1.config(command=lambda: controller.show_frame("HomePage"))
        button_2.config(command=lambda: controller.show_frame("EvaluationPage"))
        button_3.config(command=lambda: controller.show_frame("InfoPage1"))

    def on_show(self):
        duration = self.controller.shared_data.get("duration", "00:00:00")
        self.canvas.itemconfig(self.duration_text_id, text=duration)

class EvaluationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_eval("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_eval("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_eval("image_3.png"))
        image_3 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_eval("image_4.png"))
        image_4 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_eval("image_5.png"))
        image_5 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_eval("image_6.png"))
        image_6 = self.canvas.create_image(
            673.0,
            28.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_eval("image_7.png"))
        image_7 = self.canvas.create_image(
            399.0,
            94.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_eval("image_8.png"))
        image_8 = self.canvas.create_image(
            400.0,
            236.0,
            image=self.image_image_8
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets_eval("image_9.png"))
        image_9 = self.canvas.create_image(
            225.0,
            390.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets_eval("image_10.png"))
        image_10 = self.canvas.create_image(
            574.0,
            390.0,
            image=self.image_image_10
        )

        self.canvas.create_text(
            87.0,
            154.0,
            anchor="nw",
            text="lorem ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum lorem ipsum ipsum lorem ipsum ipsum lorem ipsum lorem ipsum",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1),
            width=625
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_eval("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=58.0,
            y=355.0,
            width=335.0,
            height=70.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_eval("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=407.0,
            y=355.0,
            width=335.0,
            height=70.0
        )

        button_1.config(command=lambda: controller.show_frame("HomePage"))
        button_2.config(command=lambda: controller.show_frame("OverviewPage"))

class InfoPage1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets_info_1("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_info_1("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.canvas.create_text(
            58.0,
            116.0,
            anchor="nw",
            text="Point 1 to 2 = 0.2 mm\nPoint 2 to 3 = 0.2 mm\nPoint 3 to 4 = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_info_1("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=58.0,
            y=371.0,
            width=144.0,
            height=70.0
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_info_1("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_info_1("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_info_1("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_info_1("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_info_1("image_7.png"))
        image_7 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_info_1("image_8.png"))
        image_8 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_8
        )

        self.canvas.create_text(
            58.0,
            83.0,
            anchor="nw",
            text="Ideal Interval = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_info_1("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=642.0,
            y=371.0,
            width=100.0,
            height=70.0
        )

        button_1.config(command=lambda: controller.show_frame("OverviewPage"))
        button_2.config(command=lambda: controller.show_frame("InfoPage2"))

class InfoPage2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg = "#E5E5E5",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets_info_2("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets_info_2("image_2.png"))
        image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=self.image_image_2
        )

        self.canvas.create_text(
            58.0,
            116.0,
            anchor="nw",
            text="Point 1 to 2 = 0.2 mm\nPoint 2 to 3 = 0.2 mm\nPoint 3 to 4 = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets_info_2("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=58.0,
            y=371.0,
            width=144.0,
            height=70.0
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets_info_2("image_3.png"))
        image_3 = self.canvas.create_image(
            400.0,
            27.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets_info_2("image_4.png"))
        image_4 = self.canvas.create_image(
            88.0,
            28.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets_info_2("image_5.png"))
        image_5 = self.canvas.create_image(
            764.0,
            27.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets_info_2("image_6.png"))
        image_6 = self.canvas.create_image(
            35.0,
            27.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets_info_2("image_7.png"))
        image_7 = self.canvas.create_image(
            672.0,
            28.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=relative_to_assets_info_2("image_8.png"))
        image_8 = self.canvas.create_image(
            399.0,
            27.0,
            image=self.image_image_8
        )

        self.canvas.create_text(
            58.0,
            83.0,
            anchor="nw",
            text="Ideal Interval = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets_info_2("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=642.0,
            y=371.0,
            width=100.0,
            height=70.0
        )

        button_1.config(command=lambda: controller.show_frame("OverviewPage"))
        button_2.config(command=lambda: controller.show_frame("InfoPage1"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
