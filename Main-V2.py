import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
from tkinter import PhotoImage
import pygame  # ใช้ pygame สำหรับเสียง
import cv2.aruco as aruco
import cv2
import serial
import time
import tkinter as tk
from tkinter import ttk


from Sub.Debug import VariableViewer 


class PageReset(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        # แสดงข้อความระหว่างรีเซ็ต
        label = tk.Label(self, text="กำลังรีเซ็ตระบบ กรุณารอสักครู่...", font=("Helvetica", 18), bg="white")
        label.pack(fill="both", expand=True, pady=200)
        # สั่ง restart หลังพัก 0.5 วินาที


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
        if getattr(self, 'gif_animation_id', None):
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
            if not gif_label.winfo_exists():
                return
            gif_label.configure(image=self.gif_frames[frame_index])
            gif_label.image = self.gif_frames[frame_index]
            self.gif_animation_id = self.root.after(300, animate,(frame_index + 1) % len(self.gif_frames))

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
        

        
class SerialManager:
    def __init__(self,controller , port, baudrate):
        self.controller = controller
        self.delivered = set()
        self.spincheck = 25
        
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None
        time.sleep(2)

    def send_command(self, command):
        self.ser.write(f"{command}\n".encode())
        if command == "HSpinL" or command == "HSpinR":
            self.spincheck = 25

    def read_message(self):
        if self.ser.in_waiting:
            return str(self.ser.readline().decode().strip())
        return None
    
    def track_scan(self):
        frame = self.controller.camera_manager.get_frame()
        if frame is None:
            print("Error: Unable to capture frame.")
            return None
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #--------Aruco--------
        
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
        
        #--------Line Track--------
        _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
        height, width = thresh.shape
        roi = thresh[int(height / 2):, :]
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy + int(height / 2)), 5, (0, 255, 0), -1)
                if cx < width * 0.3:
                    # print("HardLeft")
                    self.ser.write("leftHard\n".encode())
                elif cx < width * 0.4:
                    # print("MidLeft")
                    self.ser.write("leftMid\n".encode())
                elif cx < width * 0.5:
                    # print("SoftLeft")
                    self.ser.write("leftSoft\n".encode())
                elif cx > 2 * width * 0.4:
                    # print("HardRight")
                    self.ser.write("rightHard\n".encode())  
                elif cx > 2 * width * 0.35:
                    # print("MidRight")
                    self.ser.write("rightMid\n".encode()) 
                elif cx > 2 * width * 0.3:
                    # print("SoftRight")
                    self.ser.write("rightSoft\n".encode())
                else:
                    self.ser.write("forwardMid\n".encode())
                    if self.spincheck != 0:
                        self.spincheck -= 1
            else:
                self.ser.write("stop\n".encode())  
                # print("1Spin")
        else:
            if self.spincheck == 0:
                self.ser.write("Spin\n".encode())
                # print("2Spin")
                self.spincheck = 25
                
                
        
        
        
    
    
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
        
    def reset(self):
        # แสดงหน้า ResetPage
        self.controller.ui_manager.show_page("ResetPage")
        # สั่ง restart อีกทีผ่าน root.after
        self.controller.root.after(500, self.controller.restart)
        
        
        
class AppController:
    def __init__(self, root):
        
        self.root = root
        self.ui_manager = UIManager(root)
        self.camera_manager = CameraManager()
        self.serial_manager = SerialManager(self,'/dev/ttyUSB0', 115200)
        self.sound_manager = SoundManager()
        self.food_setup = food_setup(self)
        
        self.current_page = None  # Variable to track the current page
        self.start = False

        if not getattr(self.root, 'variable_viewer_shown', False):
            VariableViewer(self)
            self.root.variable_viewer_shown = True
        # Link the root to this controller
        
        root.app_controller = self

        # Create pages
        self.ui_manager.create_page("Page1", Page1, self)
        self.ui_manager.create_page("Page2", Page2, self)
        self.ui_manager.create_page("Page3", Page3, self)
        self.ui_manager.create_page("Page4", Page4, self)
        self.ui_manager.create_page("Page5", Page5, self)
        self.ui_manager.create_page("Page6", Page6, self)
        self.ui_manager.create_page("ResetPage", PageReset, self)

        # Show initial page
        self.ui_manager.show_page("Page1")

        
        
        # Schedule to switch to Page 2 after 1.5 seconds
        root.after(1500, lambda: self.ui_manager.show_page("Page2"))
            
            
    def restart(self):
        # ปล่อยกล้องก่อน
        try:
            self.camera_manager.release()
        except:
            pass
        
        # ทำลายทุกหน้าเดิม
        for page in self.ui_manager.pages.values():
            page.destroy()
        self.ui_manager.pages.clear()

        # เรียก init ใหม่ทั้งหมด
        self.__init__(self.root)
        

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
        self.color1 = "black"
        self.color2 = "black"
        self.color3 = "black"
        

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
        
        # # Button Floor 1
        # button_floor_1 = self.canvas.create_rectangle(0, 0, 0, 0, outline="black", width=outline)  
        # self.canvas.tag_bind(button_floor_1, "<Button-1>", lambda event: self.controller.food_setup.set_floor(3, "Page3"))
        # # Button Floor 2
        # button_floor_2 = self.canvas.create_rectangle(0, 0, 0, 0, outline="black", width=outline)  
        # self.canvas.tag_bind(button_floor_2, "<Button-1>", lambda event: self.controller.food_setup.set_floor(2, "Page3"))
        # # Button Floor 3
        # button_floor_3 = self.canvas.create_rectangle(0, 0, 0, 0, outline="black", width=outline)  
        # self.canvas.tag_bind(button_floor_3, "<Button-1>", lambda event: self.controller.food_setup.set_floor(1, "Page3"))
        
        # Button Clear
        button_clear = self.canvas.create_rectangle(200, 430, 300, 510, outline="black", width=outline)  
        self.canvas.tag_bind(button_clear, "<Button-1>", lambda event: self.clear_item())
        
        
        # Add "Close" button with a beautiful style
        style = ttk.Style()
        style.configure(
            "TButton",
            font=("Helvetica", 14),
            foreground="white",
            background="#ff4d4d",  # Red color
            borderwidth=0,
            relief="flat",
        )
        style.map(
            "TButton",
            background=[("active", "#ff6666")],  # Lighter red on hover
            relief=[("pressed", "sunken")],
        )
        
        
        # Add "Close" button
        self.close_button = ttk.Button(self, text="Close", style="TButton", command=root.destroy)
        self.close_button.place(relx=0.05, rely=0.1, anchor="center")

        
        # Floor 1, 2, 3 images
        self.image_id1 = self.canvas.create_image(250, 385, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room1))
        self.image_id2 = self.canvas.create_image(250, 298, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room2))
        self.image_id3 = self.canvas.create_image(250, 207, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room3))
        
        
        
        def refresh():
            if not self.winfo_exists():
                return
            
            
            self.canvas.delete(self.image_id1)
            self.canvas.delete(self.image_id2)
            self.canvas.delete(self.image_id3)
            self.image_id1 = self.canvas.create_image(250, 385, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room1))
            self.image_id2 = self.canvas.create_image(250, 298, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room2))
            self.image_id3 = self.canvas.create_image(250, 207, anchor="center", image=self.controller.ui_manager.floor_image(self.controller.food_setup.room3))
            
            #Shelf Stats
            shelf_stats_3 = self.canvas.create_rectangle(142, 162, 358, 252, outline=self.color1, width=6)  
            shelf_stats_2 = self.canvas.create_rectangle(142, 257, 358, 342, outline=self.color2, width=6)  
            shelf_stats_1 = self.canvas.create_rectangle(142, 347, 358, 428, outline=self.color3, width=6) 
            
            if self.color1 == "green":
            # Button Floor 1
                button_floor_1 = self.canvas.create_rectangle(450, 160, 820, 260, outline="black", width=outline) 
                self.canvas.tag_bind(button_floor_1, "<Button-1>", lambda event: self.controller.food_setup.set_floor(3, "Page3"))
            else:
                button_floor_1 = self.canvas.create_rectangle(450, 160, 820, 260, outline="black", width=outline) 
                self.canvas.tag_bind(button_floor_1, "<Button-1>")
            if self.color2 == "green":
            # Button Floor 2
                button_floor_2 = self.canvas.create_rectangle(450, 285, 820, 385, outline="black", width=outline)  
                self.canvas.tag_bind(button_floor_2, "<Button-1>", lambda event: self.controller.food_setup.set_floor(2, "Page3"))
            else:
                button_floor_2 = self.canvas.create_rectangle(450, 285, 820, 385, outline="black", width=outline) 
                self.canvas.tag_bind(button_floor_2, "<Button-1>")
            # Button Floor 3
            if self.color3 == "green":
                button_floor_3 = self.canvas.create_rectangle(450, 415, 820, 515, outline="black", width=outline) 
                self.canvas.tag_bind(button_floor_3, "<Button-1>", lambda event: self.controller.food_setup.set_floor(1, "Page3"))
            else:
                button_floor_3 = self.canvas.create_rectangle(450, 415, 820, 515, outline="black", width=outline) 
                self.canvas.tag_bind(button_floor_3, "<Button-1>")
            
            
            
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
        self._scan_id = None
        
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
            if not self.winfo_exists(): return
            if self.controller.current_page == "Page4" or self.controller.current_page == "Page5":
                if len(self.controller.food_setup.sortroom) != 0:
                    self.controller.ui_manager.start_gif_animation(gif_label, self.controller.food_setup.sortroom[0])
                else:
                    self.controller.ui_manager.start_gif_animation(gif_label, 0)
            root.after(1000, refresh)
                
            
        def scan_camera():
            if not self.winfo_exists(): return
            if self.controller.current_page == "Page5":
                self.controller.serial_manager.track_scan()
                if len(self.controller.food_setup.sortroom) != 0:
                    if self.controller.serial_manager.aruco_id == self.controller.food_setup.sortroom[0]:
                        self.controller.food_setup.nowtable = self.controller.food_setup.nowtable +1
                        self.controller.ui_manager.start_gif_animation(gif_label, 0)
                        self.controller.serial_manager.send_command("HSpinL")
                        time.sleep(2)
                        self.controller.sound_manager.play_sound("food_arrived")
                        self.controller.ui_manager.show_page("Page6")
                        
                else:
                    if self.controller.serial_manager.aruco_id == 6:
                        self.controller.serial_manager.send_command("Spin")
                        self.controller.food_setup.reset()
            self._scan_id = self.after(20, scan_camera)
            
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
            if not self.winfo_exists(): return
            if self.controller.current_page == "Page6":
                self.controller.ui_manager.start_gif_animation(gif_label, 6)
                
                # check_shelf()
                if self.controller.current_page == "Page6":
                    if min(self.controller.food_setup.sortroom) not in  self.controller.food_setup.room:
                        del self.controller.food_setup.sortroom[0]
                        self.controller.sound_manager.play_sound("enjoy_food")
                        self.controller.ui_manager.show_page("Page5")
                        if len(self.controller.food_setup.sortroom) != 0:
                            self.controller.serial_manager.send_command("HSpinR")
                        else:
                            self.controller.serial_manager.send_command("HSpinL")
            root.after(1000, refresh)
            
        refresh()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Set the window size to the screen size
    root.attributes("-fullscreen", True)  # Enable fullscreen mode
    root.overrideredirect(True)  # Remove window decorations (title bar, etc.)
    root.bind("<Escape>", lambda event: (root.overrideredirect(False), root.attributes("-fullscreen", False)))  # Exit fullscreen with Escape key
    app = AppController(root)
    root.mainloop()
