import tkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage
import pygame  # ใช้ pygame สำหรับเสียง
import cv2.aruco as aruco
import cv2
import serial
import time
import tkinter as tk

from Sub.Debug import VariableViewer 



class UIManager:
    def __init__(self, root):
        self.root = root
        self.pages = {}
        self.current_page = None
        self.Button_Hitbox_outline = 0
        
        #Icon image
        self.icon_image0 = PhotoImage(file="Image/R0.png")
        self.icon_image1 = PhotoImage(file="Image/R1.png")
        self.icon_image2 = PhotoImage(file="Image/R2.png")
        self.icon_image3 = PhotoImage(file="Image/R3.png")
        self.icon_image4 = PhotoImage(file="Image/R4.png")
        self.icon_image5 = PhotoImage(file="Image/R5.png")

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
    
    def floor_image(self,image):
            if image == 0:
                return self.icon_image0
            if image == 1:
                return self.icon_image1
            if image == 2:
                return self.icon_image2
            if image == 3:
                return self.icon_image3
            if image == 4:
                return self.icon_image4
            if image == 5:
                return self.icon_image5

class CameraManager:
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not self.vid.isOpened():
            print("Error: Unable to access the camera.")

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
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None
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
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(self.sounds[sound_name])


class AppController:
    def __init__(self, root):
        self.ui_manager = UIManager(root)
        self.camera_manager = CameraManager()
        self.serial_manager = SerialManager('/dev/ttyUSB0', 115200)
        self.sound_manager = SoundManager()
        self.food_setup = food_setup(self)
        
        self.current_page = None  # Variable to track the current page

        # Link the root to this controller
        root.app_controller = self

        # Create pages
        self.ui_manager.create_page("Page1", Page1, self)
        self.ui_manager.create_page("Page2", Page2, self)
        self.ui_manager.create_page("Page3", Page3, self)

        # Show initial page
        self.ui_manager.show_page("Page1")

        # Schedule to switch to Page 2 after 1.5 seconds
        root.after(1500, lambda: self.ui_manager.show_page("Page2"))



        
class food_setup:
    def __init__(self, controller):
        self.controller = controller
        self.floor = 0
        self.room1 = 0
        self.room2 = 0
        self.room3 = 0
        self.sortroom = []
        self.room = [self.room1, self.room2, self.room3]
    
    def set_floor(self, floor, page):
        self.floor = floor
        self.controller.ui_manager.show_page(page)
        
    def set_room(self,room ,page):
        if self.floor == 1:
            if room == self.room2:
                self.room2 = 0
            if room == self.room3:
                self.room3 = 0
            self.room1 = room
        elif self.floor == 2:
            if room == self.room1:
                self.room1 = 0
            if room == self.room3:
                self.room3 = 0
            self.room2 = room
        elif self.floor == 3:
            if room == self.room1:
                self.room1 = 0
            if room == self.room2:
                self.room2 = 0
            self.room3 = room
            
        #Sort room
        room = [
        self.room1 if self.room1 is not None else 0,
        self.room2 if self.room2 is not None else 0,
        self.room3 if self.room3 is not None else 0,
        ]
            
        self.sortroom = [value for value in sorted(set(room)) if value != 0]    
        
        self.room = [self.room1, self.room2, self.room3]
        self.controller.ui_manager.show_page(page)
        

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
        
        # button for swithching to Page 2
        switch_button = tk.Button(self, text="Go to Page 2", command=lambda: self.controller.ui_manager.show_page("Page2"))
        switch_button.place(relx=0.5, rely=0.9, anchor='center')


class Page2(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        outline = self.controller.ui_manager.Button_Hitbox_outline

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
        
        # Button Floor 1
        button_floor_1 = self.canvas.create_rectangle(450, 160, 820, 260, outline="black", width=outline)  
        self.canvas.tag_bind(button_floor_1, "<Button-1>", lambda event: self.controller.food_setup.set_floor(3, "Page3"))
        # Button Floor 2
        button_floor_2 = self.canvas.create_rectangle(450, 285, 820, 385, outline="black", width=outline)  
        self.canvas.tag_bind(button_floor_2, "<Button-1>", lambda event: self.controller.food_setup.set_floor(2, "Page3"))
        # Button Floor 3
        button_floor_3 = self.canvas.create_rectangle(450, 415, 820, 515, outline="black", width=outline)  
        self.canvas.tag_bind(button_floor_3, "<Button-1>", lambda event: self.controller.food_setup.set_floor(1, "Page3"))
        
        # Button Floor OK
        button_ok = self.canvas.create_rectangle(830, 450, 1050, 600, outline="black", width=outline)  
        self.canvas.tag_bind(button_ok, "<Button-1>")
        
        # Button Clear
        button_clear = self.canvas.create_rectangle(200, 430, 300, 510, outline="black", width=outline)  
        self.canvas.tag_bind(button_clear, "<Button-1>", lambda event: self.clear_item())
        
        # Floor 1, 2, 3 images
        self.image_id1 = self.canvas.create_image(250, 385, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room1))
        self.image_id2 = self.canvas.create_image(250, 298, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room2))
        self.image_id3 = self.canvas.create_image(250, 207, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room3))
        
        
        
        def refresh():
            self.canvas.delete(self.image_id1)
            self.canvas.delete(self.image_id2)
            self.canvas.delete(self.image_id3)
            self.image_id1 = self.canvas.create_image(250, 385, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room1))
            self.image_id2 = self.canvas.create_image(250, 298, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room2))
            self.image_id3 = self.canvas.create_image(250, 207, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room3))
            root.after(500, refresh)  # Refresh every 1000 milliseconds (1 second)
        refresh()

    def open_variable_viewer(self):
        VariableViewer(self.controller)
    
    
class Page3(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        outline = self.controller.ui_manager.Button_Hitbox_outline

        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("Image/3.png"))

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Add label and button on top of the canvas
        label = tk.Label(self, text="Page 3", font=("Helvetica", 16), bg="white")
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # button for swithching to Page 2
        switch_button = tk.Button(self, text="Go to Page 2", command=lambda: self.controller.ui_manager.show_page("Page2"))
        switch_button.place(relx=0.5, rely=0.9, anchor='center')

        
        # ---- ปุ่มเลือกห้อง 1 ----
        button_frame = self.canvas.create_rectangle(250, 220, 390, 360, outline="black", width=outline) 
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.food_setup.set_room(1, "Page2"))
        
        # ---- ปุ่มเลือกห้อง 2 ----
        button_frame = self.canvas.create_rectangle(480, 220, 620, 360, outline="black", width=outline) 
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.food_setup.set_room(2, "Page2"))        
        
        # ---- ปุ่มเลือกห้อง 3 ----
        button_frame = self.canvas.create_rectangle(710, 220, 860, 360, outline="black", width=outline)  
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.food_setup.set_room(3, "Page2"))
        
        # ---- ปุ่มเลือกห้อง 4 ----      
        button_frame = self.canvas.create_rectangle(370, 380, 510, 520, outline="black", width=outline)
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.food_setup.set_room(4, "Page2"))
        
        # ---- ปุ่มเลือกห้อง 5 ----
        button_frame = self.canvas.create_rectangle(600, 380, 740, 520, outline="black", width=outline)
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.food_setup.set_room(5, "Page2"))
        
        # ---- ปุ่มย้อนกลับ ----
        button_frame = self.canvas.create_rectangle(10, 450, 160, 600, outline="black", width=outline)
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.food_setup.change_page("Page2"))


if __name__ == "__main__":
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()