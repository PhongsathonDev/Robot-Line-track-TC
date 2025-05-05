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
        self.gif_animation_id = None
        
        #Icon image
        self.icon_image0 = PhotoImage(file="Image/R0.png")
        self.icon_image1 = PhotoImage(file="Image/R1.png")
        self.icon_image2 = PhotoImage(file="Image/R2.png")
        self.icon_image3 = PhotoImage(file="Image/R3.png")
        self.icon_image4 = PhotoImage(file="Image/R4.png")
        self.icon_image5 = PhotoImage(file="Image/R5.png")
        
        #Gif Image
        self.gif_image0 = Image.open("Image/animation.gif")
        self.gif_image1 = Image.open("Image/animation1.gif")
        self.gif_image2 = Image.open("Image/animation2.gif")
        self.gif_image3 = Image.open("Image/animation3.gif")
        self.gif_image4 = Image.open("Image/animation4.gif")
        self.gif_image5 = Image.open("Image/animation5.gif") 
        self.gif_image6 = Image.open("Image/End.gif") 

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
            
            
    def start_gif_animation(self, gif_label, gif_image_index):
        # Cancel any previous animation
        if self.gif_animation_id:
            self.root.after_cancel(self.gif_animation_id)
            self.gif_animation_id = None

        # Clear previous GIF frames
        self.gif_frames = []

        # Load the GIF frames
        try:
            gif = getattr(self, f"gif_image{gif_image_index}")
            while True:
                frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
                self.gif_frames.append(frame)
                gif.seek(len(self.gif_frames))  # Move to the next frame
        except EOFError:
            pass  # End of GIF

        # Animate the GIF
        def animate(frame_index=0):
            if self.gif_frames:
                gif_label.configure(image=self.gif_frames[frame_index])
                gif_label.image = self.gif_frames[frame_index]
                self.gif_animation_id = self.root.after(300, animate, (frame_index + 1) % len(self.gif_frames))  # Adjust timing (ms)

        animate()
            
    
    
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
        
        self.aruco_id = None
        
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

    def aruco_scan(self):
        frame = self.get_frame()
        if frame is None:
            print("Error: Unable to capture frame.")
            return None

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Load the predefined dictionary for ArUco markers
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        parameters = aruco.DetectorParameters()

        # Detect the markers in the image
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            self.aruco_id = ids.flatten()
            return ids.flatten(), corners
        
        else:
            self.aruco_id = "None"
            return None
        
        
        


class SerialManager:
    def __init__(self, port, baudrate):
        self.delivered = set()
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
            return str(self.ser.readline().decode().strip())
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

        
class food_setup:
    def __init__(self, controller):
        self.controller = controller
        self.floor = 0
        self.room1 = 0
        self.room2 = 0
        self.room3 = 0
        self.sortroom = []
        self.room = [self.room1, self.room2, self.room3]
        self.nowtable = 1
        
        self.delivered = self.controller.serial_manager.delivered
            
    def set_floor(self, floor, page):
        self.floor = floor
        self.controller.ui_manager.show_page(page)
        
        
    def set_room(self,room ,page):
        if self.floor == 1:
            self.room1 = room
        elif self.floor == 2:
            self.room2 = room
        elif self.floor == 3:
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
        

        
        
        
class AppController:
    def __init__(self, root):
        self.ui_manager = UIManager(root)
        self.camera_manager = CameraManager()
        self.serial_manager = SerialManager('/dev/ttyUSB0', 115200)
        self.sound_manager = SoundManager()
        self.food_setup = food_setup(self)
        
        self.current_page = None  # Variable to track the current page
        self.start = False

        # Link the root to this controller
        root.app_controller = self

        # Create pages
        self.ui_manager.create_page("Page1", Page1, self)
        self.ui_manager.create_page("Page2", Page2, self)
        self.ui_manager.create_page("Page3", Page3, self)
        self.ui_manager.create_page("Page4", Page4, self)
        self.ui_manager.create_page("Page5", Page5, self)
        self.ui_manager.create_page("Page6", Page6, self)

        # Show initial page
        self.ui_manager.show_page("Page1")

        # Schedule to switch to Page 2 after 1.5 seconds
        root.after(1500, lambda: self.ui_manager.show_page("Page2"))
        
        # def reset():
            
        

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
            
            button_ok = None
            
            if len(self.controller.food_setup.sortroom) != 0 :
                # Button Floor OK
                button_ok = self.canvas.create_rectangle(830, 450, 1050, 600, outline="black", width=outline)  
                self.canvas.tag_bind(button_ok, "<Button-1>", lambda event: self.controller.ui_manager.show_page("Page4"))
            else :
                button_ok = self.canvas.create_rectangle(0, 0, 0, 0, outline="black", width=outline)  
                
            
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
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.ui_manager.show_page("Page2"))


class Page4(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        outline = self.controller.ui_manager.Button_Hitbox_outline

        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("Image/4.png"))

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Add label and button on top of the canvas
        label = tk.Label(self, text="Page 4", font=("Helvetica", 16), bg="white")
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # Ok button
        button_frame = self.canvas.create_rectangle(550, 380, 780, 570, outline="black", width=outline)  
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.ui_manager.show_page("Page5"))
        
        # Cancel button
        button_frame = self.canvas.create_rectangle(270, 380, 500, 570, outline="black", width=outline)  
        self.canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.controller.ui_manager.show_page("Page2"))
        
            
        
class Page5(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        outline = self.controller.ui_manager.Button_Hitbox_outline

        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("Image/animation.gif"))

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        # Add label and button on top of the canvas
        label = tk.Label(self, text="Page 5", font=("Helvetica", 16), bg="white")
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # Create a label for the GIF animation
        gif_label = tk.Label(self)
        gif_label.place(relx=0.5, rely=0.5, anchor="center")
        
        def refresh():
            if self.controller.current_page == "Page4" or self.controller.current_page == "Page5":
                if len(self.controller.food_setup.sortroom) != 0:
                    self.controller.ui_manager.start_gif_animation(gif_label, self.controller.food_setup.sortroom[0])
                else:
                    self.controller.ui_manager.start_gif_animation(gif_label, 0)
                # Start the refresh thread
            root.after(1000, refresh)
                
            
        def scan_camera():
            if self.controller.current_page == "Page5":
                self.controller.camera_manager.aruco_scan()
                if len(self.controller.food_setup.sortroom) != 0:
                    if self.controller.camera_manager.aruco_id == self.controller.food_setup.sortroom[0]:
                        self.controller.food_setup.nowtable = self.controller.food_setup.nowtable +1
                        self.controller.ui_manager.start_gif_animation(gif_label, 0)
                        self.controller.ui_manager.show_page("Page6")
                else:
                    if self.controller.camera_manager.aruco_id == 6:
                        self.controller.ui_manager.show_page("Page2")
            root.after(100, scan_camera)
            
        scan_camera()
        refresh()
        
        
class Page6(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        outline = self.controller.ui_manager.Button_Hitbox_outline

        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("Image/End.gif"))

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        # Add label and button on top of the canvas
        label = tk.Label(self, text="Page 6", font=("Helvetica", 16), bg="white")
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # Create a label for the GIF animation
        gif_label = tk.Label(self)
        gif_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.controller.ui_manager.start_gif_animation(gif_label, 6)
        def refresh():
            if self.controller.current_page == "Page6":
                self.controller.ui_manager.start_gif_animation(gif_label, 6)
                check_shelf()
            root.after(1000, refresh)
            
        def check_shelf():
            if self.controller.current_page == "Page6":
                if min(self.controller.food_setup.sortroom) not in  self.controller.food_setup.room:
                    del self.controller.food_setup.sortroom[0]
                    self.controller.ui_manager.show_page("Page5")
            root.after(1000, check_shelf)
            
        check_shelf()
        refresh()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()