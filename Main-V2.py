import tkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage
import pygame  # ใช้ pygame สำหรับเสียง
import cv2.aruco as aruco
import cv2
import serial
import time
import tkinter as tk



class UIManager:
    def __init__(self, root):
        self.root = root
        self.pages = {}
        self.current_page = None

    def create_page(self, page_name, page_class, *args, **kwargs):
        self.pages[page_name] = page_class(self.root, *args, **kwargs)

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = self.pages[page_name]
        self.current_page.pack(fill="both", expand=True)
        # Notify AppController about the current page
        if hasattr(self.root, 'app_controller'):
            self.root.app_controller.current_page = page_name  # Update current_page here


class CameraManager:
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_frame(self):
        ret, frame = self.vid.read()
        if ret:
            return frame
        return None

    def release(self):
        if self.vid.isOpened():
            self.vid.release()


class SerialManager:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)

    def send_command(self, command):
        self.ser.write(f"{command}\n".encode())

    def read_message(self):
        if self.ser.in_waiting:
            return self.ser.readline().decode().strip()
        return None


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "click": pygame.mixer.Sound("Image/click.wav"),
            "make_way": pygame.mixer.Sound("Voice/make_way.mp3"),
            "food_arrived": pygame.mixer.Sound("Voice/food_arrived.wav"),
            "enjoy_food": pygame.mixer.Sound("Voice/enjoy_food.wav"),
            "wrong_food": pygame.mixer.Sound("Voice/wrong_food.wav"),
        }

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()


class AppController:
    def __init__(self, root):
        self.ui_manager = UIManager(root)
        self.camera_manager = CameraManager()
        self.serial_manager = SerialManager('/dev/ttyUSB0', 115200)
        self.sound_manager = SoundManager()
        self.current_page = None  # Variable to track the current page

        # Link the root to this controller
        root.app_controller = self

        # Create pages
        self.ui_manager.create_page("Page1", Page1, self)
        self.ui_manager.create_page("Page2", Page2, self)

        # Show initial page
        self.ui_manager.show_page("Page1")

        # Schedule to switch to Page 2 after 1.5 seconds
        root.after(1500, lambda: self.ui_manager.show_page("Page2"))


class VariableViewer(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Variable Viewer")
        self.geometry("400x300")

        # Example variables to display
        self.variables = {
            "Camera Status": "Active" if self.controller.camera_manager.vid.isOpened() else "Inactive",
            "Serial Port": self.controller.serial_manager.ser.port,
            "Baudrate": self.controller.serial_manager.ser.baudrate,
            "Now Page": self.controller.current_page,
        }

        # Create labels to display variables
        self.labels = {}
        for idx, (key, value) in enumerate(self.variables.items()):
            tk.Label(self, text=f"{key}:", font=("Helvetica", 12)).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            self.labels[key] = tk.Label(self, text=value, font=("Helvetica", 12))
            self.labels[key].grid(row=idx, column=1, sticky="w", padx=10, pady=5)

        # Add a refresh button
        refresh_button = tk.Button(self, text="Refresh", command=self.refresh_variables)
        refresh_button.grid(row=len(self.variables), column=0, columnspan=2, pady=10)
        
        # Start auto-refresh
        self.auto_refresh()

    def refresh_variables(self):
        # Update variable values
        self.variables["Camera Status"] = "Active" if self.controller.camera_manager.vid.isOpened() else "Inactive"
        self.variables["Serial Port"] = self.controller.serial_manager.ser.port
        self.variables["Baudrate"] = self.controller.serial_manager.ser.baudrate
        self.variables["Now Page"] = self.controller.current_page  # Fetch updated current_page

        # Update labels
        for key, label in self.labels.items():
            label.config(text=self.variables[key])
    
    def auto_refresh(self):
        self.refresh_variables()
        self.after(1000, self.auto_refresh)  # Refresh every 1000 milliseconds (1 second)


class Page1(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller

        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("Image/1.png"))

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Add label and button on top of the canvas
        label = tk.Label(self, text="Page 1", font=("Helvetica", 16), bg="white")
        label.place(relx=0.5, rely=0.05, anchor='center')

        switch_button = tk.Button(self, text="Go to Page 2", command=lambda: self.controller.ui_manager.show_page("Page2"))
        switch_button.place(relx=0.5, rely=0.9, anchor='center')


class Page2(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller

        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("Image/2.png"))

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Add label and button on top of the canvas
        label = tk.Label(self, text="Page 2", font=("Helvetica", 16), bg="white")
        label.place(relx=0.5, rely=0.05, anchor='center')

        switch_button = tk.Button(self, text="Go to Page 1", command=lambda: self.controller.ui_manager.show_page("Page1"))
        switch_button.place(relx=0.5, rely=0.95, anchor='center')
        
        # Add button to open Variable Viewer
        variable_viewer_button = tk.Button(self, text="Debug", command=self.open_variable_viewer)
        variable_viewer_button.place(relx=0.04, rely=0.03, anchor='center')

    def open_variable_viewer(self):
        VariableViewer(self.controller)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()