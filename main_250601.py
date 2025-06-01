# app.py

import tkinter as tk
import time
import signal
import sys
from flask import Flask, request
import requests
#from server_api import post_flow_value, get_flow_value
from server_api_2 import post_value, get_value
import subprocess
import os

#Camera
sys.path.append("/home/samuel")
from camera_integration import start_camera, stop_camera, get_camera_frame, save_current_frame, measure_image, calculate_resolution, compute_distances
from PIL import Image, ImageTk
import cv2
import math
import numpy as np

from tkinter import PhotoImage, Canvas, Button
from pathlib import Path

class App(tk.Tk):    
    def __init__(self):
        super().__init__()
        
        #self.server_process = subprocess.Popen(['python', '/home/samuel/sophie/code/server3.py'])
        self.server_process = subprocess.Popen(['python', '/home/samuel/sophie/code/server_TA.py'])

        # print(f"Server3.py started with PID: {self.server_process.pid}")
        print(f"Server_TA.py started with PID: {self.server_process.pid}")

        self.geometry("800x480")
        self.resizable(False, False)
        self.title("VAST KIT")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        self.shared_data = {}

        for F in (HomePage, IntroPage, DiameterPage, FlowRatePage, TargetPage, StabilizingPage, SystemReadyPage, CountdownPage, DurationPage, PhotoPage1, PreviewPage1, MeasurePage1, PhotoPage2, PreviewPage2, MeasurePage2, RestorePage, EvaluatingPage, OverviewPage, EvaluationPage, InfoPage1, InfoPage2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("HomePage")

    # def show_frame(self, page_name):
        # frame = self.frames[page_name]
        # frame.tkraise()
        # if hasattr(frame, "on_show"):
            # frame.on_show()

    def show_frame(self, page_name):
        current = [f for f in self.frames.values() if f.winfo_ismapped()]
        for f in current:
            if hasattr(f, "on_hide"):
                f.on_hide()

        frame = self.frames[page_name]

        if hasattr(frame, "on_show"):
            frame.on_show()

        frame.tkraise()


    def on_closing(self):
        """Handle the window close event by terminating the subprocess and closing the app."""
        print("Closing application...")
        if self.server_process:
            print("Terminating server process...")
            self.server_process.terminate()  # Send SIGTERM to the subprocess
            try:
                self.server_process.wait(timeout=5)  # Wait up to 5 seconds for the process to terminate
            except subprocess.TimeoutExpired:
                print("Server did not terminate in time, forcing kill...")
                self.server_process.kill()  # Force kill if it doesn't terminate
            print(f"Server process (PID: {self.server_process.pid}) terminated.")
        self.destroy()  # Close the Tkinter app
        
        global sensor_process
        if sensor_process is not None:
            sensor_process.terminate()
            try:
                sensor_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                sensor_process.kill()
            sensor_process = None
        
# Asset paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_HOME = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame0")
ASSETS_FLOW = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame1")
ASSETS_INTRO = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame2")
ASSETS_DIAMETER = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame3")
ASSETS_STABLE = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame5")
ASSETS_READY = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame4")
ASSETS_TIME = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame8")
ASSETS_PHOTO = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame9")
ASSETS_OVERVIEW = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame10")
ASSETS_EVAL = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets/frame12")

# Assets paths revision (2)
ASSETS_DIAMETER2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame9")
ASSETS_PHOTO1 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame0")
ASSETS_PREV1 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame1")
ASSETS_MEASURE1 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame6")
ASSETS_PHOTO2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame5")
ASSETS_PREV2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame4")
ASSETS_MEASURE2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame7")
ASSETS_OVERVIEW2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame8")
ASSETS_INFO1 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame2")
ASSETS_INFO2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame3")
ASSETS_ANIMATIONS = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_2/frame10")

# Assets paths revision (3)
ASSETS_HOME2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_3/frame1")
ASSETS_INTRO2 = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_3/frame2")
ASSETS_TARGET = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_3/frame3")
ASSETS_RESTORE = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build/assets_3/frame0")


# Sensor paths
sensor_process = None
ASSETS_FILE = OUTPUT_PATH / Path(r"/home/samuel/sophie/Tkinter-Designer-master/fix/build")


# Path
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
    
def relative_to_assets_photo(path: str) -> Path:
    return ASSETS_PHOTO / Path(path)

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
    
def relative_to_assets_file(path: str) -> Path:
    return ASSETS_FILE / Path(path)

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
                        # post_flow_value(value)
                        post_value("nilai_flow", "nilai_flow", value)
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
        self.canvas.itemconfig(self.text_display, fill="black") 
    
class TargetPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller

        self.thick = 0.1
        self.interval = (self.thick*2)
        
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
            text=self.thick,
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

        self.nilai_flow_display = self.canvas.create_text(
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
            text=self.interval,
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

        self.flow_target = self.canvas.create_text(
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

        self.galat_interval_display = self.canvas.create_text(
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

        self.galat_flow_display = self.canvas.create_text(
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

    def update_nilai(self):
        self.nilai_flow = get_value("nilai_flow", "nilai_flow")
        self.canvas.itemconfig(self.nilai_flow_display, text=self.nilai_flow)
        self.canvas.itemconfig(self.flow_target, text=self.nilai_flow)
        self.controller.shared_data["desired_flow"] = self.nilai_flow

        self.galat_interval = self.interval*10/100
        self.galat_flow = self.nilai_flow*10/100
        self.canvas.itemconfig(self.galat_interval_display, text=self.galat_interval)
        self.canvas.itemconfig(self.galat_flow_display, text=self.galat_flow)

    def on_show(self):
        self.update_nilai()

class StabilizingPage(tk.Frame):
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
            for i in range(1, 12)
        ]

    def on_show(self):
        global sensor_process
        if sensor_process is None or sensor_process.poll() is not None:
            sensor_process = subprocess.Popen(['/home/samuel/galih/flowsensor2'])
            
        self.image_on_canvas = self.canvas.create_image(399.0, 240.0, image=self.frames[0])

        self.start_time = time.time()
        self.frame_index = 0

        self.animate()

    def animate(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time < 8:  # loop for 8 seconds
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

        self.current_flow_display = self.canvas.create_text(
            610.0,
            400.0,
            anchor="center",
            text="0",
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
        button_2.config(command=self.save_flow)

    def save_flow(self):
        start_flow = self.canvas.itemcget(self.current_flow_display, "text")
        print("Start flow:", start_flow)
        self.controller.shared_data["start_flow"] = start_flow
        self.controller.show_frame("CountdownPage")

    def update_nilai_flow(self):
        self.nilai_flow = self.controller.shared_data.get("desired_flow", "0")       
        self.canvas.itemconfig(self.nilai_flow_display, text=self.nilai_flow)

    def update_current_flow(self):
        try:
            self.current_flow = get_value("current_flow", "current_flow")
            print("Get response:", self.current_flow)
            self.canvas.itemconfig(self.current_flow_display, text=self.current_flow)
            self.controller.shared_data["current_flow"] = self.current_flow
        except requests.exceptions.RequestException:
            self.canvas.itemconfig(self.current_flow_display, text="Connection Error")

        # panggil fungsi ini lagi setelah 1000 ms (1 detik)
        self.controller.after(1000, self.update_current_flow)
        
    def on_show(self):
        self.update_nilai_flow()
        self.update_current_flow()
    
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

        self.current_flow_display = self.canvas.create_text(
            426.0,
            297.0,
            anchor="nw",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 20 * -1)
        )

    def on_show(self):
        self.start_time = time.time()
        self.running = True
        self.update_stopwatch()
        self.update_current_flow()
        

    def update_current_flow(self):
        current_flow = self.controller.shared_data.get("current_flow", "0")        
        self.canvas.itemconfig(self.current_flow_display, text=current_flow)
        self.controller.after(1000, self.update_current_flow)
        
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
            file=relative_to_assets_photo_1("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )
        
        # self.placeholder = ImageTk.PhotoImage(Image.new("RGB", (640, 480), "gray"))
        # self.image_2 = self.canvas.create_image(
            # 400.0,
            # 255.0,
            # image=self.placeholder
        # )
        self.image_2 = self.canvas.create_image(400, 255, image=None)
        self.current_image = None  # for live preview frame


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

        
        button_1.config(command=self.capture)
        
    def update_preview(self):
        if not self.running:
            return  # Jangan update kalau tidak berjalan

        try:
            frame = get_camera_frame()
            frame = cv2.resize(frame, (800, 480))
            image = Image.fromarray(frame)
            self.tk_image = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.image_2, image=self.tk_image)
        except Exception as e:
            print("Error getting frame:", e)

        self.after(30, self.update_preview)
        
    def capture(self):
        # image1_path = relative_to_assets_file("photo1.jpg")
        # camera_integration.save_current_frame(image1_path)
        # # Store new image in shared_data
        # new_image = ImageTk.PhotoImage(Image.open(image1_path).resize((800, 480)))
        # self.controller.shared_data["photo1"] = new_image

        # image1_path = "photo1.jpg"
        # save_current_frame(image1_path)
        # self.controller.shared_data["photo1"] = ImageTk.PhotoImage(Image.open("photo1.jpg").resize((800, 480)))
        # self.controller.show_frame("PreviewPage1")

        image_path = "photo1.jpg"
        save_current_frame(image_path)
        img = Image.open(image_path).resize((800, 480))
        final_img = ImageTk.PhotoImage(img)
        self.controller.shared_data["photo1"] = final_img
        self.controller.shared_data["photo1_ref"] = final_img  # prevent GC
        self.controller.show_frame("PreviewPage1")


    def on_show(self):
        self.running = True
        start_camera()
        self.update_preview()
        
    def on_hide(self):
        self.running = False
        stop_camera()

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

        # self.placeholder = ImageTk.PhotoImage(Image.new("RGB", (640, 480), "gray"))
        # self.image_2 = self.canvas.create_image(
            # 400.0,
            # 255.0,
            # image=self.placeholder
        # )
        # self.current_image = self.placeholder 
        self.image_2 = self.canvas.create_image(400, 255, image=None)
        self.current_image = None
        
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

        # self.update_preview_image()
        button_1.config(command=lambda: controller.show_frame("PhotoPage1"))
        button_2.config(command=lambda: controller.show_frame("PhotoPage2"))


    def on_show(self):
        # Called when frame is shown
        photo = self.controller.shared_data.get("photo1")
        if photo:
            self.canvas.itemconfig(self.image_2, image=photo)
            self.current_image = photo  # keep reference
            self.photo_ref = photo  # keep reference

        else:
            print("No photo found in shared_data.")
    
class PhotoPage2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E5E5E5")
        self.controller = controller
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
            file=relative_to_assets_photo_2("image_1.png"))
        image_1 = self.canvas.create_image(
            491.0,
            276.0,
            image=self.image_image_1
        )

        # self.placeholder = ImageTk.PhotoImage(Image.new("RGB", (640, 480), "gray"))
        # self.image_2 = self.canvas.create_image(
            # 400.0,
            # 255.0,
            # image=self.placeholder
        # )
        self.image_2 = self.canvas.create_image(400, 255, image=None)
        self.current_image = None  # for live preview frame


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
        
        button_1.config(command=self.capture)
        
    def update_preview(self):       
        if not self.running:
            return  # Jangan update kalau tidak berjalan

        try:
            frame = get_camera_frame()
            frame = cv2.resize(frame, (800, 480))
            image = Image.fromarray(frame)
            self.tk_image = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.image_2, image=self.tk_image)
        except Exception as e:
            print("Error getting frame:", e)

        self.after(30, self.update_preview)
        
    def capture(self):
        # image2_path = "photo2.jpg"
        # save_current_frame(image2_path)
        # self.controller.shared_data["photo2"] = ImageTk.PhotoImage(Image.open("photo2.jpg").resize((800, 480)))
        # self.controller.show_frame("PreviewPage2")
        
        image_path = "photo2.jpg"
        save_current_frame(image_path)
        img = Image.open(image_path).resize((800, 480))
        final_img = ImageTk.PhotoImage(img)
        self.controller.shared_data["photo2"] = final_img
        self.controller.shared_data["photo2_ref"] = final_img  # prevent GC
        self.controller.show_frame("PreviewPage2")

    def on_show(self):
        self.running = True
        start_camera()
        self.update_preview()
        
    def on_hide(self):
        self.running = False
        stop_camera()

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

        # self.placeholder = ImageTk.PhotoImage(Image.new("RGB", (640, 480), "gray"))
        # self.image_2 = self.canvas.create_image(
            # 400.0,
            # 255.0,
            # image=self.placeholder
        # )
        # self.current_image = self.placeholder 
        self.image_2 = self.canvas.create_image(400, 255, image=None)
        self.current_image = None

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

    def on_show(self):
        # Called when frame is shown
        photo = self.controller.shared_data.get("photo2")
        if photo:
            self.canvas.itemconfig(self.image_2, image=photo)
            self.current_image = photo  # keep reference
            self.photo_ref = photo  # keep reference

        else:
            print("No photo found in shared_data.")

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

        # self.placeholder = ImageTk.PhotoImage(Image.new("RGB", (640, 480), "gray"))
        # self.image_2 = self.canvas.create_image(
            # 400.0,
            # 255.0,
            # image=self.placeholder
        # )
        # self.current_image = self.placeholder 
        
        self.image_2 = self.canvas.create_image(400.0, 255.0, image=None)  # Use itemconfig later

        # UI overlay image (in front of image_2)
        self.overlay_image = PhotoImage(file=relative_to_assets_measure_1("image_1.png"))
        self.canvas.create_image(491.0, 276.0, image=self.overlay_image)

        
        self.image_path = "photo1.jpg"
        self.clicked_points = []
        self.resolution = None
        self.distance_measured = []
        self.current_image = None  

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
        
        
        self.canvas.create_text(
            30.0,
            83.0,
            anchor="nw",
            text="Ideal Interval = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.measurement = self.canvas.create_text(
            40.0,
            116.0,
            anchor="nw",
            text=" ",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )
        
        self.canvas.bind("<Button-1>", self.on_click)

        # Buttons
        tk.Button(self, text="Reset", command=self.reset).place(x=30, y=400)
        tk.Button(self, text="Measure", command=self.measure).place(x=100, y=400)

        button_1.config(command=self.next_page)
        

    def on_show(self):
        self.reset()
        self.load_image()

    def load_image(self):
        # try:
            # image = Image.open(self.image_path).resize((800, 480))
            # self.current_image = ImageTk.PhotoImage(image)
            # self.canvas.itemconfig(self.image_2, image=self.current_image)
        # except Exception as e:
            # print("Error loading image:", e)

        if not self.current_image:
            try:
                pil_image = Image.open(self.image_path).resize((800, 480))
                self.current_image = ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print("Error loading image:", e)
                return
        self.canvas.itemconfig(self.image_2, image=self.current_image)

    def on_click(self, event):
        x, y = event.x, event.y
        self.clicked_points.append((x, y))
        print(f"Clicked: {x}, {y}")

        r = 4
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="")

        if len(self.clicked_points) > 1:
            x0, y0 = self.clicked_points[-2]
            self.canvas.create_line(x0, y0, x, y, fill="green", width=2)
        
    def measure(self):
        if len(self.clicked_points) < 4:
            self.canvas.itemconfig(self.measurement, text="Need at least 2 suture points and 2 reference points.")
            return

        self.resolution = calculate_resolution(self.clicked_points)
        if self.resolution is None:
            self.canvas.itemconfig(self.measurement, text="Invalid reference points.")
            return

        result_lines = ["--- Measurements ---"] #[f"Resolution: {self.resolution:.4f} mm/pixel", "--- Measurements ---"]

        self.distance_measured = compute_distances(
            self.clicked_points,
            self.resolution,
            canvas=self.canvas
        )

        for i, dist in enumerate(self.distance_measured):
            pt1 = self.clicked_points[i]
            pt2 = self.clicked_points[i+1]
            dist_px = np.linalg.norm(np.array(pt1) - np.array(pt2))
            result_lines.append(f"Point {i+1} to {i+2}: {dist_px:.2f} px = {dist:.2f} mm")

        # Combine and show the result on canvas
        self.result_text = "\n".join(result_lines)
        self.canvas.itemconfig(self.measurement, text=self.result_text)

    def suture_accuracy(self):
        if not self.distance_measured:
            self.canvas.itemconfig(self.measurement, text="Please measure first before checking accuracy.")
            return

        self.data = 0
        self.accurate = 0
        self.inaccurate = 0

        for dist in self.distance_measured:
            self.data += 1
            if 0.18 <= dist <= 0.22:
                self.accurate += 1
            else:
                self.inaccurate += 1

        print(f"\n\nAccuracy Summary:\n✓ Accurate: {self.accurate}/{self.data}\n✗ Inaccurate: {self.inaccurate}/{self.data}")
        
        # self.controller.shared_data["accurate_1"] = self.accurate
        # self.controller.shared_data["inaccurate_1"] = self.inaccurate
        
        self.controller.shared_data["accuracy_1"] = {
            "data": self.data,
            "accurate": self.accurate,
            "inaccurate": self.inaccurate
        }
    
    def reset(self):
        self.canvas.delete("all")
        self.clicked_points.clear()
        self.distance_measured.clear()
        self.resolution = None

        self.canvas.create_image(491.0, 276.0, image=self.image_image_1)

        self.canvas.create_image(491.0, 276.0, image=self.overlay_image)
        self.image_2 = self.canvas.create_image(400.0, 255.0, image=self.current_image)

        # --- Redraw overlay assets (same order as in __init__) ---
        # self.image_2 = self.canvas.create_image(400.0, 255.0, image=self.current_image)
        self.canvas.create_image(400.0, 27.0, image=self.image_image_3)
        self.canvas.create_image(400.0, 460.0, image=self.image_image_4)
        self.canvas.create_image(399.0, 27.0, image=self.image_image_5)
        self.canvas.create_image(400.0, 460.0, image=self.image_image_6)
        self.canvas.create_image(88.0, 28.0, image=self.image_image_7)
        self.canvas.create_image(764.0, 27.0, image=self.image_image_8)
        self.canvas.create_image(35.0, 27.0, image=self.image_image_9)
        self.canvas.create_image(672.0, 28.0, image=self.image_image_10)

        # --- Recreate text labels ---
        self.canvas.create_text(
            40.0,
            83.0,
            anchor="nw",
            text="Ideal Interval = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.measurement = self.canvas.create_text(
            40.0,
            116.0,
            anchor="nw",
            text=" ",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )
    
    def next_page(self):
        self.suture_accuracy()
        # Save current image and clicked points into shared_data
        self.controller.shared_data["measured_image_1"] = self.current_image
        self.controller.shared_data["clicked_points_1"] = self.clicked_points.copy()
        self.controller.shared_data["measurement_photo_1"] = self.result_text

        # Navigate to MeasurePage2
        self.controller.show_frame("MeasurePage2")

        
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

        # self.placeholder = ImageTk.PhotoImage(Image.new("RGB", (640, 480), "gray"))
        # self.image_2 = self.canvas.create_image(
            # 400.0,
            # 255.0,
            # image=self.placeholder
        # )
        # self.current_image = self.placeholder

        self.image_2 = self.canvas.create_image(400.0, 255.0, image=None)  # Use itemconfig later

        # UI overlay image (in front of image_2)
        self.overlay_image = PhotoImage(file=relative_to_assets_measure_1("image_1.png"))
        self.canvas.create_image(491.0, 276.0, image=self.overlay_image)

        self.image_path = "photo2.jpg"
        self.clicked_points = []
        self.resolution = None
        self.distance_measured = []
        self.current_image = None  

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

        self.canvas.create_text(
            30.0,
            83.0,
            anchor="nw",
            text="Ideal Interval = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.measurement = self.canvas.create_text(
            40.0,
            116.0,
            anchor="nw",
            text=" ",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )
        
        self.canvas.bind("<Button-1>", self.on_click)

        # Buttons
        tk.Button(self, text="Reset", command=self.reset).place(x=30, y=400)
        tk.Button(self, text="Measure", command=self.measure).place(x=100, y=400)

        button_1.config(command=self.next_page)

    def on_show(self):
        self.reset()
        self.load_image()

    def load_image(self):
        # try:
            # image = Image.open(self.image_path).resize((800, 480))
            # self.current_image = ImageTk.PhotoImage(image)
            # self.canvas.itemconfig(self.image_2, image=self.current_image)
        # except Exception as e:
            # print("Error loading image:", e)

        if not self.current_image:
            try:
                pil_image = Image.open(self.image_path).resize((800, 480))
                self.current_image = ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print("Error loading image:", e)
                return
        self.canvas.itemconfig(self.image_2, image=self.current_image)
        
        
        
    def on_click(self, event):
        x, y = event.x, event.y
        self.clicked_points.append((x, y))
        print(f"Clicked: {x}, {y}")

        r = 4
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="")

        if len(self.clicked_points) > 1:
            x0, y0 = self.clicked_points[-2]
            self.canvas.create_line(x0, y0, x, y, fill="green", width=2)

    def measure(self):
        if len(self.clicked_points) < 4:
            self.canvas.itemconfig(self.measurement, text="Need at least 2 suture points and 2 reference points.")
            return

        self.resolution = calculate_resolution(self.clicked_points)
        if self.resolution is None:
            self.canvas.itemconfig(self.measurement, text="Invalid reference points.")
            return

        result_lines = ["--- Measurements ---"] #[f"Resolution: {self.resolution:.4f} mm/pixel", "--- Measurements ---"]

        self.distance_measured = compute_distances(
            self.clicked_points,
            self.resolution,
            canvas=self.canvas
        )

        for i, dist in enumerate(self.distance_measured):
            pt1 = self.clicked_points[i]
            pt2 = self.clicked_points[i+1]
            dist_px = np.linalg.norm(np.array(pt1) - np.array(pt2))
            result_lines.append(f"Point {i+1} to {i+2}: {dist_px:.2f} px = {dist:.2f} mm")

        # Combine and show the result on canvas
        self.result_text = "\n".join(result_lines)
        self.canvas.itemconfig(self.measurement, text=self.result_text)
        self.controller.shared_data["measurement_photo2"] = self.result_text

    def suture_accuracy(self):
        if not self.distance_measured:
            self.canvas.itemconfig(self.measurement, text="Please measure first before checking accuracy.")
            return

        self.data = 0
        self.accurate = 0
        self.inaccurate = 0

        for dist in self.distance_measured:
            self.data += 1
            if 0.18 <= dist <= 0.22:
                self.accurate += 1
            else:
                self.inaccurate += 1

        print(f"\n\nAccuracy Summary:\n✓ Accurate: {self.accurate}/{self.data}\n✗ Inaccurate: {self.inaccurate}/{self.data}")
        
        # self.controller.shared_data["accurate_1"] = self.accurate
        # self.controller.shared_data["inaccurate_1"] = self.inaccurate
        
        self.controller.shared_data["accuracy_2"] = {
            "data": self.data,
            "accurate": self.accurate,
            "inaccurate": self.inaccurate
        }

    
    def reset(self):
        self.canvas.delete("all")
        self.clicked_points.clear()
        self.distance_measured.clear()
        self.resolution = None

        self.canvas.create_image(491.0, 276.0, image=self.image_image_1)

        self.canvas.create_image(491.0, 276.0, image=self.overlay_image)
        self.image_2 = self.canvas.create_image(400.0, 255.0, image=self.current_image)
        
        # --- Redraw overlay assets (same order as in __init__) ---
        # self.image_2 = self.canvas.create_image(400.0, 255.0, image=self.current_image)
        self.canvas.create_image(400.0, 27.0, image=self.image_image_3)
        self.canvas.create_image(400.0, 460.0, image=self.image_image_4)
        self.canvas.create_image(399.0, 27.0, image=self.image_image_5)
        self.canvas.create_image(400.0, 460.0, image=self.image_image_6)
        self.canvas.create_image(88.0, 28.0, image=self.image_image_7)
        self.canvas.create_image(764.0, 27.0, image=self.image_image_8)
        self.canvas.create_image(35.0, 27.0, image=self.image_image_9)
        self.canvas.create_image(672.0, 28.0, image=self.image_image_10)

        # --- Recreate text labels ---
        self.canvas.create_text(
            40.0,
            83.0,
            anchor="nw",
            text="Ideal Interval = 0.2 mm",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.measurement = self.canvas.create_text(
            40.0,
            116.0,
            anchor="nw",
            text=" ",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )
    
    def next_page(self):
        self.suture_accuracy()
        # Save current image and clicked points into shared_data
        self.controller.shared_data["measured_image_2"] = self.current_image
        self.controller.shared_data["clicked_points_2"] = self.clicked_points.copy()
        self.controller.shared_data["measurement_photo_2"] = self.result_text

        # Navigate to MeasurePage2
        self.controller.show_frame("RestorePage")
        
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

        self.current_flow_display = self.canvas.create_text(
            202.0,
            266.0,
            anchor="center",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 20 * -1)
        )

        self.duration_text_id = self.canvas.create_text(
            550.0,
            265.0,
            anchor="center",
            text="00:00:00",
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

        button_1.config(command=lambda: controller.show_frame("EvaluatingPage"))
        
    # def save_end_flow(self):
        # end_flow = self.canvas.itemcget(self.current_flow_display, "text")
        # print("End flow:", end_flow)
        # self.controller.shared_data["end_flow"] = end_flow
        # self.controller.show_frame("EvaluatingPage")

    def update_current_flow(self):
        current_flow = self.controller.shared_data.get("current_flow", "0")        
        self.canvas.itemconfig(self.current_flow_display, text=current_flow)
        self.controller.after(1000, self.update_current_flow)
        
    def on_show(self):
        duration = self.controller.shared_data.get("duration", "00:00:00")
        self.canvas.itemconfig(self.duration_text_id, text=duration)
        self.update_current_flow()
      
class EvaluatingPage(tk.Frame):
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
            for i in range(12, 22)
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
            end_flow = get_value("current_flow", "current_flow")
            print("End flow:", end_flow)
            self.controller.shared_data["end_flow"] = end_flow
            self.controller.show_frame("OverviewPage")

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

        self.overall = self.canvas.create_text(
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

        self.percentage_suture = self.canvas.create_text(
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

        self.percentage_flow = self.canvas.create_text(
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

        self.accurate = self.canvas.create_text(
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

        self.inaccurate = self.canvas.create_text(
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

        self.end_flow_display = self.canvas.create_text(
            598.0,
            301.0,
            anchor="nw",
            text="0",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.start_flow_display = self.canvas.create_text(
            598.0,
            276.0,
            anchor="nw",
            text="0",
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
            file=relative_to_assets_overview("button_1.png"))
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
            file=relative_to_assets_overview("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
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
    
    def terminate_flow_sensor(self):
        global sensor_process
        if sensor_process is not None:
            sensor_process.terminate()
            # try:
                # sensor_process.wait(timeout=5)
            # except subprocess.TimeoutExpired:
                # sensor_process.kill()
            sensor_process = None
        
    def on_show(self):
        self.terminate_flow_sensor()
        duration = self.controller.shared_data.get("duration", "00:00:00")
        self.canvas.itemconfig(self.duration_text_id, text=duration)
        
        start_flow = float(self.controller.shared_data.get("start_flow", "0"))
        self.canvas.itemconfig(self.start_flow_display, text=str(start_flow))

        end_flow = float(self.controller.shared_data.get("end_flow", "0"))
        self.canvas.itemconfig(self.end_flow_display, text=str(end_flow))
        
        accuracy_1 = self.controller.shared_data.get("accuracy_1",{})
        accuracy_2 = self.controller.shared_data.get("accuracy_2",{})

        data = accuracy_1.get("data", 0) + accuracy_2.get("data", 0)
        accurate = accuracy_1.get("accurate", 0) + accuracy_2.get("accurate", 0)
        inaccurate = accuracy_1.get("inaccurate", 0) + accuracy_2.get("inaccurate", 0)

        self.canvas.itemconfig(self.accurate, text=f"{accurate}/{data}")
        self.canvas.itemconfig(self.inaccurate, text=f"{inaccurate}/{data}")

        #calculation
        if end_flow != 0:
            if start_flow <= end_flow:
                flow_acc = (start_flow / end_flow) * 100
            else:
                flow_acc = (end_flow / start_flow) * 100
            print(flow_acc)
            self.canvas.itemconfig(self.percentage_flow, text=f"{int(flow_acc)}%")
        else:
            self.canvas.itemconfig(self.percentage_flow, text="0%")

        if accurate != 0:
            suture_acc = accurate/data * 100
            self.canvas.itemconfig(self.percentage_suture, text=f"{int(suture_acc)}%")
        else:
            self.canvas.itemconfig(self.percentage_suture, text="0%")

        score = int((int(flow_acc)+int(suture_acc))/2)
        self.canvas.itemconfig(self.overall, text=f"{int(score)}%")

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
        
        self.image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=None
        )

        self.measurement = self.canvas.create_text(
            40.0,
            116.0,
            anchor="nw",
            text=" ",
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
            40.0,
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

    def on_show(self):
        # photo1 = self.controller.shared_data.get("measured_image_1")
        # self.canvas.itemconfig(self.image_2, image=photo1)
        measurement = self.controller.shared_data.get("measurement_photo_1")
        self.canvas.itemconfig(self.measurement, text=measurement)

        img = self.controller.shared_data.get("measured_image_1")
        points = self.controller.shared_data.get("clicked_points_1")

        if img:
            self.canvas.itemconfig(self.image_2, image=img)
            self.image_ref = img  # prevent GC

        if points:
            r = 4
            for i, (x, y) in enumerate(points):
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="")
                if i > 0:
                    x0, y0 = points[i - 1]
                    self.canvas.create_line(x0, y0, x, y, fill="green", width=2)

        else:
            print("No points found to show.")
    
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

        self.image_2 = self.canvas.create_image(
            400.0,
            255.0,
            image=None
        )

        self.measurement = self.canvas.create_text(
            58.0,
            116.0,
            anchor="nw",
            text=" ",
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

    def on_show(self):
        measurement = self.controller.shared_data.get("measurement_photo_2")
        self.canvas.itemconfig(self.measurement, text=measurement)
        img = self.controller.shared_data.get("measured_image_2")
        points = self.controller.shared_data.get("clicked_points_2")

        if img:
            self.canvas.itemconfig(self.image_2, image=img)
            self.image_ref = img  # prevent GC

        if points:
            r = 4
            for i, (x, y) in enumerate(points):
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="")
                if i > 0:
                    x0, y0 = points[i - 1]
                    self.canvas.create_line(x0, y0, x, y, fill="green", width=2)

        else:
            print("No points found to show.")
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
