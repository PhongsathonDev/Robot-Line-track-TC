import tkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage
import pygame  # ใช้ pygame สำหรับเสียง
import cv2.aruco as aruco
import cv2
import serial
import time
import tkinter as tk

# เชื่อมต่อกับ esp32
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)


class MultiPageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MultiPage App with Backgrounds")
        self.Width = 1024
        self.Height = 600
        self.Outline = 0
        self.pages = {}
        self.current_page = None
        self.room = None
        self.room1 = 0
        self.room2 = 0
        self.room3 = 0
        self.table = 1
        self.sortroom = []
        self.room_values_dict = {}
        self.floor = None
        self.marker_id = 0
        self.ids = 0
        

        # Initialize pygame สำหรับเสียง
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("Image/click.wav")  # ใส่ path ของไฟล์เสียงคลิก

        # ผูก event คลิกกับ root widget
        self.root.bind("<Button-1>", self.play_click_sound)

        # Initialize image placeholders to avoid AttributeError
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.gif1 = Image.open("Image/animation.gif")
        self.gif2 = Image.open("Image/animation.gif")
        self.gif3 = Image.open("Image/animation.gif")
        self.giftable = [self.gif1, self.gif2, self.gif3]
        
        # ----------------------- Line tracking and camera setup ------------------------
        
        # self.vid = None #ใว้เก็บภาพจากกล้อง
        self.is_camera_active = False  # ตัวแปรสถานะสำหรับกล้อง
        self.room = None 
        self.spincheck = 25
        
        # ไฟสถานะชั้นวาง
        self.color1 = "green"
        self.color2 = "green"
        self.color3 = "green"
        
        
        self.makeway = pygame.mixer.Sound("Voice/make_way.mp3")
        self.food_arrived = pygame.mixer.Sound("Voice/food_arrived.wav")
        self.enjoy_food = pygame.mixer.Sound("Voice/enjoy_food.wav")
        self.wrong_food = pygame.mixer.Sound("Voice/wrong_food.wav")

        # Aruco Marker Setup
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.aruco_params = aruco.DetectorParameters()
        self.aruco_detector = aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        
        
        
        # Create the pages
        self.pages["Page 1"] = self.create_page_1()
        self.pages["Page 2"] = self.create_page_2()
        self.pages["Page 3"] = self.create_page_3()
        self.pages["Page 4"] = self.create_page_4()
        self.pages["Page 5"] = self.create_page_5()
        self.pages["Page 6"] = self.create_page_6()
        self.pages["Page 7"] = self.create_page_7()
        # self.pages["Page 8"] = self.create_page_8()
        # self.pages["Page 9"] = self.create_page_9()
        # self.pages["Page 10"] = self.create_page_10()
        # self.pages["Page Debug"] = self.create_page_debug()

        

        
        
        
        # Start with the first page
        self.show_page("Page 1")

    def play_click_sound(self, event=None):
        """เล่นเสียงคลิก"""
        self.click_sound.play()

    # ----- title page -----
    def create_page_1(self): 
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/1.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 1", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')

        return page_frame

    def create_page_2(self):
        self.stats = 0
        print("----------------")
        print(f"Rooms: {self.sortroom}")
        print(f"table: [{self.room1}, {self.room2}, {self.room3}]") 
        
        
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height,)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/2.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 2", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # Button Floor 1
        button_frame = canvas.create_rectangle(450, 160, 820, 260, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(3, "Page 3"))
        # Button Floor 2
        button_frame = canvas.create_rectangle(450, 285, 820, 385, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(2, "Page 3"))
        # Button Floor 3
        button_frame = canvas.create_rectangle(450, 415, 820, 515, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(1, "Page 3"))
        
        # Button Floor OK
        button_frame = canvas.create_rectangle(830, 450, 1050, 600, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>")
        
        # Button Clear
        button_frame = canvas.create_rectangle(200, 430, 300, 510, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.clear_item())
        
        
        # Floor 1, 2, 3 images
        canvas.create_image(250, 385, anchor="center", image=self.image1)
        canvas.overlay_image1 = self.image1  
        canvas.create_image(250, 298, anchor="center", image=self.image2)
        canvas.overlay_image2 = self.image2  
        canvas.create_image(250, 207, anchor="center", image=self.image3)
        canvas.overlay_image3 = self.image3
        
        # Floor Stats Green Box 
        stata_box1 = canvas.create_oval(180, 375, 200, 395, fill=self.color1, outline=self.color1, width=5)
        stata_box2 = canvas.create_oval(180, 290, 200, 310, fill=self.color2, outline=self.color2, width=5)
        stata_box3 = canvas.create_oval(180, 200, 200, 220, fill=self.color3, outline=self.color3, width=5)

        def refresh():
            
            # self.root.attributes("-fullscreen", True)
            canvas.itemconfig(stata_box1, fill=self.color1, outline=self.color1)
            canvas.itemconfig(stata_box2, fill=self.color2, outline=self.color2)
            canvas.itemconfig(stata_box3, fill=self.color3, outline=self.color3)
            
            # Floor 1, 2, 3 images
            canvas.create_image(250, 385, anchor="center", image=self.image1)
            canvas.overlay_image1 = self.image1  
            canvas.create_image(250, 298, anchor="center", image=self.image2)
            canvas.overlay_image2 = self.image2  
            canvas.create_image(250, 207, anchor="center", image=self.image3)
            canvas.overlay_image3 = self.image3
            
            # Button Floor 1
            if self.color1 == "red":
                button_frame = canvas.create_rectangle(450, 415, 820, 515, outline="black", width=self.Outline)
                canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(1, "Page 3"))
            elif self.color1 == "green":
                button_frame = canvas.create_rectangle(450, 415, 820, 515, outline="black", width=self.Outline)
                canvas.tag_bind(button_frame, "<Button-1>")
            # Button Floor 2
            if self.color2 == "red":
                button_frame = canvas.create_rectangle(450, 285, 820, 385, outline="black", width=self.Outline)
                canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(2, "Page 3"))
            elif self.color2 == "green":
                button_frame = canvas.create_rectangle(450, 285, 820, 385, outline="black", width=self.Outline)
                canvas.tag_bind(button_frame, "<Button-1>")
            # Button Floor 3
            if self.color3 == "red":
                button_frame = canvas.create_rectangle(450, 160, 820, 260, outline="black", width=self.Outline)  
                canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(3, "Page 3"))
            elif self.color3 == "green":
                button_frame = canvas.create_rectangle(450, 160, 820, 260, outline="black", width=self.Outline)  
                canvas.tag_bind(button_frame, "<Button-1>")
            
            if len(self.sortroom) > 0:
                button_frame = canvas.create_rectangle(830, 450, 1050, 600, outline="black", width=self.Outline)  
                canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.show_page("Page 4"))
            else:
                button_frame = canvas.create_rectangle(830, 450, 1050, 600, outline="black", width=self.Outline)  
                canvas.tag_bind(button_frame, "<Button-1>")
                
            if self.stats == 0:
                if self.color1 == "green" and self.room1 != 0:
                    self.clear_item()
                    # self.room1 = 0
                    # self.image1 = None
                    # self.floor = 1
                    # self.set_room_and_go(0, "Page 2")
                elif self.color2 == "green" and self.room2 != 0:
                    self.clear_item()
                    # self.room2 = 0
                    # self.image2 = None
                    # self.floor = 2
                    # self.set_room_and_go(0, "Page 2")
                elif self.color3 == "green" and self.room3 != 0:
                    self.clear_item()
                    # self.room3 = 0
                    # self.image3 = None
                    # self.floor = 3
                    # self.set_room_and_go(0, "Page 2")
            self.root.after(100, refresh)  # Adjust the interval as needed

        refresh()
        

        
        self.read_from_serial()
        return page_frame

    def create_page_3(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/3.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 3", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        
        # ---- ปุ่มเลือกห้อง 1 ----
        button_frame = canvas.create_rectangle(250, 220, 390, 360, outline="black", width=self.Outline) 
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(1, "Page 2"))
        
        # ---- ปุ่มเลือกห้อง 2 ----
        button_frame = canvas.create_rectangle(480, 220, 620, 360, outline="black", width=self.Outline) 
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(2, "Page 2"))        
        
        # ---- ปุ่มเลือกห้อง 3 ----
        button_frame = canvas.create_rectangle(710, 220, 860, 360, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(3, "Page 2"))
        
        # ---- ปุ่มเลือกห้อง 4 ----      
        button_frame = canvas.create_rectangle(370, 380, 510, 520, outline="black", width=self.Outline)
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(4, "Page 2"))
        
        # ---- ปุ่มเลือกห้อง 5 ----
        button_frame = canvas.create_rectangle(600, 380, 740, 520, outline="black", width=self.Outline)
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(5, "Page 2"))
        
        # ---- ปุ่มย้อนกลับ ----
        button_frame = canvas.create_rectangle(10, 450, 160, 600, outline="black", width=self.Outline)
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.change_page("Page 2"))
        
        return page_frame

    
    
    def create_page_4(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/4.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 4", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # Ok button
        button_frame = canvas.create_rectangle(550, 380, 780, 570, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.show_page("Page 5"))
        
        # Cancel button
        button_frame = canvas.create_rectangle(270, 380, 500, 570, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.show_page("Page 2"))
        

        return page_frame

    def create_page_5(self):
        self.stats = 1
        ser.write("stop\n".encode())  
        print(f"sortroom: {len(self.sortroom)+1}")
        print(f"table: {self.table}")
        
        
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/5.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 5", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # ----- GIF Animation -----
        self.gif_label = tk.Label(page_frame, bd=0, bg='white')
        self.gif_label.place(relx=0.5, rely=0.5, anchor='center')
        if len(self.sortroom)+1 > self.table:
            self.gif_frames = []
            try:
                gif = self.giftable[self.table - 1]  # <-- Your GIF path
                self.table += 1
                while True:
                    frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
                    self.gif_frames.append(frame)
                    gif.seek(len(self.gif_frames))  # Move to next frame
            except EOFError:
                pass  # End of GIF
            
            self.gif_frame_index = 0
            self.animate_gif()
        
        overlay_button = tk.Button(
            page_frame,
            text="กดที่นี่",
            font=("Helvetica", 16),
            bg="lightblue",
            command=lambda: self.show_page("Page 6")
            )
            # ใช้พิกัดเดียวกันกับ gif_label (หรือปรับตำแหน่งตามที่ต้องการ)
        overlay_button.place(relx=0.95, rely=0.95, anchor='se')  # ขวาล่าง

        # Start updating the camera feed
        if len(self.sortroom) > 0:
            self.is_camera_active = True  # เปิดสถานะกล้อง
        self.update_camera()  # เรียกใช้ update_camera
        
        
        return page_frame
    
    def create_page_6(self):
        ser.write("stop\n".encode())  
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/5.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 6", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        
        # ----- GIF Animation -----
        self.gif_label = tk.Label(page_frame, bd=0, bg='white')
        self.gif_label.place(relx=0.5, rely=0.5, anchor='center')

        self.gif_frames = []
        try:
            gif = Image.open("Image/End.gif")  # <-- Your GIF path
            while True:
                frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
                self.gif_frames.append(frame)
                gif.seek(len(self.gif_frames))  # Move to next frame
        except EOFError:
            pass  # End of GIF
        
        self.gif_frame_index = 0
        self.animate_gif()
        print(f"table:  {self.table-1} [ {self.room1} {self.room2} {self.room3} ]") 
        self.checkfood()

        return page_frame
    
    def create_page_7(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/5.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 7", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # Camera setup
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Create a canvas for displaying the video feed
        self.canvas = tk.Canvas(page_frame, width=300, height=200)
        self.canvas.pack()

        # Start updating the camera feed
        if len(self.sortroom) > 0:
            self.is_camera_active = True  # เปิดสถานะกล้อง
        self.update_camera()  # เรียกใช้ update_camera
        
        return page_frame

    def create_page_8(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/5.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 8", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
           
        return page_frame
    
    def create_page_9(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/5.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 9", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
           
        return page_frame
    
    def create_page_10(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/5.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        # Show page No.
        label = tk.Label(page_frame, text="Page 10", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
           
        return page_frame

    def show_page(self, page_name):
        if page_name == "Page 5":
            self.pages["Page 5"] = self.create_page_5()
        if page_name == "Page 6":
            self.pages["Page 6"] = self.create_page_6()
        if page_name == "Page 7":
            self.pages["Page 7"] = self.create_page_7()
        
        
        if self.current_page is not None:
            self.current_page.pack_forget()
            # if self.current_page == self.pages.get("Page 7"):
            #     self.is_camera_active = False
            #     if self.vid is not None:
            #         self.vid.release()
            #         self.vid = None
    
        # Reload Page 5 dynamically to always get latest GIF
        
            

        self.current_page = self.pages[page_name]
        self.current_page.pack(fill="both", expand=True)

        
    def set_floor_and_go(self,floor, page_name):
        self.floor = floor
        self.change_page(page_name)
        if page_name == "Page 2":
            self.pages["Page 2"] = self.create_page_2()  # Recreate with updated room
        if page_name == "Page 3":
            self.pages["Page 3"] = self.create_page_3()  # Recreate with updated room
        
    def set_room_and_go(self, room_value, page_name):
        self.room = room_value
        
        if self.floor == 1:
            if room_value == self.room2:
                self.room2 = 0
            if room_value == self.room3:
                self.room3 = 0
            self.room1 = room_value
        elif self.floor == 2:
            if room_value == self.room1:
                self.room1 = 0
            if room_value == self.room3:
                self.room3 = 0
            self.room2 = room_value
        elif self.floor == 3:
            if room_value == self.room1:
                self.room1 = 0
            if room_value == self.room2:
                self.room2 = 0
            self.room3 = room_value
        self.room4 = 6

        # Ensure room1, room2, and room3 are not None before sorting
        room_values = [
        self.room1 if self.room1 is not None else 0,
        self.room2 if self.room2 is not None else 0,
        self.room3 if self.room3 is not None else 0,
        self.room4 if self.room4 is not None else 0,
        ]
        

            
        
        
        self.sortroom = [value for value in sorted(set(room_values)) if value != 0]
        
        self.overlay_image0 = PhotoImage(file="Image/R0.png")
        overlay_image1 = PhotoImage(file="Image/R1.png")
        overlay_image2 = PhotoImage(file="Image/R2.png")
        overlay_image3 = PhotoImage(file="Image/R3.png")
        overlay_image4 = PhotoImage(file="Image/R4.png")
        overlay_image5 = PhotoImage(file="Image/R5.png")
        
        self.gif_image0 = Image.open("Image/animation.gif")
        gif_image0 = Image.open("Image/animation.gif")
        gif_image1 = Image.open("Image/animation1.gif")
        gif_image2 = Image.open("Image/animation2.gif")
        gif_image3 = Image.open("Image/animation3.gif")
        gif_image4 = Image.open("Image/animation4.gif")
        gif_image5 = Image.open("Image/animation5.gif")

        image_floor1 = [self.overlay_image0,overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        image_floor2 = [self.overlay_image0,overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        image_floor3 = [self.overlay_image0,overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        
        gif_floor1 = [gif_image1, gif_image2, gif_image3, gif_image4, gif_image5, gif_image0]
        gif_floor2 = [gif_image1, gif_image2, gif_image3, gif_image4, gif_image5, gif_image0]
        gif_floor3 = [gif_image1, gif_image2, gif_image3, gif_image4, gif_image5, gif_image0]
        gif_floor4 = [gif_image1, gif_image2, gif_image3, gif_image4, gif_image5, gif_image0]

        if self.floor == 1 and 1 <= self.room <= 5:
            self.image1 = image_floor1[self.room1]
            self.image2 = image_floor2[self.room2]
            self.image3 = image_floor3[self.room3]
            self.gif1 = gif_floor1[self.sortroom[0] - 1] if len(self.sortroom) > 0 else None
            self.gif2 = gif_floor2[self.sortroom[1] - 1] if len(self.sortroom) > 1 else None
            self.gif3 = gif_floor3[self.sortroom[2] - 1] if len(self.sortroom) > 2 else None
            self.gif4 = gif_floor4[5]

        elif self.floor == 2 and 1 <= self.room <= 5:
            self.image1 = image_floor1[self.room1]
            self.image2 = image_floor2[self.room2]
            self.image3 = image_floor3[self.room3]
            self.gif1 = gif_floor1[self.sortroom[0] - 1] if len(self.sortroom) > 0 else None
            self.gif2 = gif_floor2[self.sortroom[1] - 1] if len(self.sortroom) > 1 else None
            self.gif3 = gif_floor3[self.sortroom[2] - 1] if len(self.sortroom) > 2 else None
            self.gif4 = gif_floor4[5]

        elif self.floor == 3 and 1 <= self.room <= 5:
            self.image1 = image_floor1[self.room1]
            self.image2 = image_floor2[self.room2]
            self.image3 = image_floor3[self.room3]
            self.gif1 = gif_floor1[self.sortroom[0] - 1] if len(self.sortroom) > 0 else None
            self.gif2 = gif_floor2[self.sortroom[1] - 1] if len(self.sortroom) > 1 else None
            self.gif3 = gif_floor3[self.sortroom[2] - 1] if len(self.sortroom) > 2 else None
            self.gif4 = gif_floor4[5]

        self.giftable = [self.gif1, self.gif2, self.gif3,self.gif4]
        
        # Refresh Page
        page_creators = {
            "Page 2": self.create_page_2,
            "Page 3": self.create_page_3,
            "Page 5": self.create_page_5,
            "Page 6": self.create_page_6,
            "Page 7": self.create_page_7,
        }

        if page_name in page_creators:
            self.pages[page_name] = page_creators[page_name]()
            self.show_page(page_name)
            
    def change_page(self, page_name):
        self.show_page(page_name)
        
    def animate_gif(self):
        if self.gif_frames:
            frame = self.gif_frames[self.gif_frame_index]
            self.gif_label.configure(image=frame)
            self.gif_label.image = frame
            self.gif_frame_index = (self.gif_frame_index + 1) % len(self.gif_frames)
            
            # Cancel any previous scheduled calls
            if hasattr(self, 'gif_animation_id') and self.gif_animation_id:
                self.root.after_cancel(self.gif_animation_id)
            
            # Schedule the next frame
            self.gif_animation_id = self.root.after(300, self.animate_gif)  # Adjust timing (ms) for frame delay
            #print(self.gif_frame_index)

    def reset_app(self):
        # Reset all attributes to their initial state
        ser.write("stop\n".encode())
        self.room = None
        self.room1 = 0
        self.room2 = 0
        self.room3 = 0
        self.table = 1
        self.sortroom = []
        self.floor = None
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.room_values_dict = {}
        self.marker_id = None
        
        
        
        
        self.change_page("Page 2")
        self.gif1 = Image.open("Image/animation.gif")
        self.gif2 = Image.open("Image/animation.gif")
        self.gif3 = Image.open("Image/animation.gif")
        self.giftable = [self.gif1, self.gif2, self.gif3,self.gif4]
        
        # self.vid = None #ใว้เก็บภาพจากกล้อง
        self.room = None 
        self.spincheck = 25
        
        # ไฟสถานะชั้นวาง
        self.color1 = "green"
        self.color2 = "green"
        self.color3 = "green"
    
    def update_camera(self):
        if not self.is_camera_active:  # เช็คสถานะกล้อง
            print("Camera is not active.")
            return

        if self.vid is None or not self.vid.isOpened():
            print("vid")
            return

        ret, frame = self.vid.read()
        if not ret or frame is None:
            print("ret frame")
            return

        frame = cv2.resize(frame, (600, 320))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.marker_id = None
        # ------ Aruco Marker Detection ------
        corners, self.ids, _ = self.aruco_detector.detectMarkers(frame)
        if self.ids is not None:
            for self.marker_id in self.ids.flatten():
                print(f"Aruco Marker ID: {self.marker_id}, Room: {self.sortroom[self.table - 2]}")
                print(f"room : {len(self.sortroom)+1} table : {self.table}")
                if str(self.marker_id) == "6":
                    print(f"1 {self.marker_id}")
                    # print(f"Aruco Marker matched Room {self.room}. Robot stopped.")
                    self.spincheck = 25
                    ser.write("Spin\n".encode())
                    for i in range (20):
                        ret, frame = self.vid.read()
                        frame = cv2.resize(frame, (600, 320))
                        corners, ids, _ = self.aruco_detector.detectMarkers(frame)
                        time.sleep(0.1)
                    self.reset_app()
                    return

                elif str(self.marker_id) == str(self.sortroom[self.table - 2]):
                    print(f"2 {self.marker_id}. {self.sortroom[self.table - 2]}")
                    # print(f"Aruco Marker matched Room {self.room}. Robot stopped.")
                    ser.write("HSpinL\n".encode())  
                    time.sleep(1)
                    self.food_arrived.play()
                    self.show_page("Page 6")
                    return
                
                
            aruco.drawDetectedMarkers(frame, corners, self.ids)

        # ------ Line Tracking ------
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
                    ser.write("leftHard\n".encode())
                elif cx < width * 0.4:
                    # print("MidLeft")
                    ser.write("leftMid\n".encode())
                elif cx < width * 0.5:
                    # print("SoftLeft")
                    ser.write("leftSoft\n".encode())
                elif cx > 2 * width * 0.4:
                    # print("HardRight")
                    ser.write("rightHard\n".encode())  
                elif cx > 2 * width * 0.35:
                    # print("MidRight")
                    ser.write("rightMid\n".encode()) 
                elif cx > 2 * width * 0.3:
                    # print("SoftRight")
                    ser.write("rightSoft\n".encode())
                else:
                    ser.write("forwardMid\n".encode())
                    if self.spincheck != 0:
                        self.spincheck -= 1
            else:
                ser.write("stop\n".encode())  
                # print("1Spin")
        else:
            if self.spincheck == 0:
                ser.write("Spin\n".encode())
                # print("2Spin")
                self.spincheck = 25

        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.delete("all")
        self.canvas.create_image(0, 105, anchor=tk.CENTER, image=self.photo)
        self.root.after(100, self.update_camera)
        
    def read_from_serial(self):
        if ser.in_waiting:
            try:
                message = str(ser.readline().decode().strip())
                # print(message)
                # -------เปลี่ยนสถานะชั้นวางของ-------
                if message == "1off":
                    self.color1 = "red"
                elif message == "1on":
                    self.color1 = "green"
                elif message == "2off":
                    self.color2 = "red"
                elif message == "2on":
                    self.color2 = "green"
                elif message == "3off":
                    self.color3 = "red"
                elif message == "3on":
                    self.color3 = "green"
                
            except Exception as e:
                print(f"Error reading from serial: {e}")
                
        # Delay การอ่าน
        self.root.after(5, self.read_from_serial)
    
    def clear_item(self):
        self.sortroom = []
        self.room = None
        self.room1 = 0
        self.room2 = 0
        self.room3 = 0
        self.table = 1
        self.floor = None
        print("----------------")
        print(f"Rooms: {self.sortroom}")
        self.image1 = None
        self.image2 = None
        self.image3 = None
                
        
    def checkfood(self):
        # ทำงานเฉพาะเมื่ออยู่ใน Page 6

        # Initialize last stats if not already set
        if not hasattr(self, 'last_color_stats'):
            self.last_color_stats = {
                "color1": self.color1,
                "color2": self.color2,
                "color3": self.color3
            }

        # Initialize warned colors if not already set
        if not hasattr(self, 'warned_colors'):
            self.warned_colors = set()

        # Update last stats when table changes
        if not hasattr(self, 'last_table') or self.last_table != self.table:
            self.last_table = self.table
            self.last_color_stats = {
                "color1": self.color1,
                "color2": self.color2,
                "color3": self.color3
            }
            self.warned_colors.clear()  # Reset warnings when table changes

        def check_and_warn(target_color, related_colors):
            for color_name in related_colors:
                if getattr(self, color_name) != self.last_color_stats[color_name]:
                    if color_name not in self.warned_colors:
                        # print(f"Warning: อาหารของคุณไม่ได้อยู่ที่ชั้น {color_name} แต่อาหารของคุณอยู่ที่ชั้น {target_color} กรุณาวางคืนแล้วหยิบอาหารของคุณ")
                        self.wrong_food.play()
                        print(f"Warning: อาหารของคุณอยู่ที่ชั้น {target_color} กรุณาวางคืนแล้วหยิบอาหารของคุณ")
                        self.warned_colors.add(color_name)  # Mark as warned
                    return False
            return True

        # Logic for checking food
        if self.table - 1 == 1:
            if self.sortroom[0] == self.room1:
                if check_and_warn("ชั้น 1", ["color2", "color3"]) and self.color1 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode())  
                    self.show_page("Page 5")
            if self.sortroom[0] == self.room2:
                if check_and_warn("ชั้น 2", ["color1", "color3"]) and self.color2 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")
            if self.sortroom[0] == self.room3:
                if check_and_warn("ชั้น 3", ["color1", "color2"]) and self.color3 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")
        if self.table - 1 == 2:
            if self.sortroom[1] == self.room1:
                if check_and_warn("ชั้น 1", ["color2", "color3"]) and self.color1 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")
            if self.sortroom[1] == self.room2:
                if check_and_warn("ชั้น 2", ["color1", "color3"]) and self.color2 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")
            if self.sortroom[1] == self.room3:
                if check_and_warn("ชั้น 3", ["color1", "color2"]) and self.color3 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")
        if self.table - 1 == 3:
            if self.sortroom[2] == self.room1:
                if check_and_warn("ชั้น 1", ["color2", "color3"]) and self.color1 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")
            if self.sortroom[2] == self.room2:
                if check_and_warn("ชั้น 2", ["color1", "color3"]) and self.color2 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")
            if self.sortroom[2] == self.room3:
                if check_and_warn("ชั้น 3", ["color1", "color2"]) and self.color3 == "green":
                    self.spincheck = 25
                    self.enjoy_food.play()
                    time.sleep(1)
                    ser.write("HSpinR\n".encode()) 
                    self.show_page("Page 5")

        # Schedule the next check
        self.root.after(10, self.checkfood)
        
        
    def exit_fullscreen(event):
        root.attributes("-fullscreen", False)
        
    def create_page_debug(self):
        """Create a debug page to display variable values in a new window."""
        debug_window = tk.Toplevel(self.root)
        debug_window.title("Debug Page")
        debug_window.geometry(f"{300}x{1000}")
        debug_window.configure(bg="white")

        # Show page title
        label = tk.Label(debug_window, text="Debug Page", font=("Helvetica", 24), bg="white")
        label.place(relx=0.5, rely=0.05, anchor='center')
        def re():
            variables = [
                f"Room: {self.room}",
                f"Room1: {self.room1}",
                f"Room2: {self.room2}",
                f"Room3: {self.room3}",
                f"Table: {self.table}",
                f"Sortroom: {self.sortroom}",
                f"Floor: {self.floor}",
                f"Color1: {self.color1}",
                f"Color2: {self.color2}",
                f"Color3: {self.color3}",
                f"current_page: {self.current_page}",
                f"room_values_dict: {self.room_values_dict}",
                f"spincheck: {self.spincheck}",
                f"self.image1: {self.image1}",
                f"self.image2: {self.image2}",
                f"self.image3: {self.image3}",
                # f"self.gif1: {self.gif1}",
                # f"self.gif2: {self.gif2}",
                # f"self.gif3: {self.gif3}",
                # f"self.giftable: {self.giftable}",
                f"self.is_camera_active: {self.is_camera_active}",
                f"len(self.sortroom): {len(self.sortroom)}",


                
                
        

            ]

            for i, var in enumerate(variables):
                var_label = tk.Label(debug_window, text=var+"           ", font=("Helvetica", 10), bg="white", anchor="w")
                var_label.place(relx=0.1, rely=0.10 + i * 0.03, anchor='w')
            root.after(500, re)

        # Close button to close the debug window
        close_button = tk.Button(
            debug_window,
            text="Close",
            font=("Helvetica", 16),
            bg="lightblue",
            command=debug_window.destroy
        )
        close_button.place(relx=0.9, rely=0.9, anchor='center')
        re()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiPageApp(root)
    # Example: Switch to Page 2 after 3 seconds
    root.after(1000, app.change_page, "Page 2")
    root.mainloop()