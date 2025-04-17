import tkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage

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
        self.room1 = None
        self.room2 = None
        self.room3 = None
        self.sortroom = [0, 0, 0]
        self.floor = None
        
        # Initialize image placeholders to avoid AttributeError
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.gif1 = Image.open("Image/animation.gif")
        self.gif2 = Image.open("Image/animation.gif")
        self.gif3 = Image.open("Image/animation.gif")
        

        # Create the pages
        self.pages["Page 1"] = self.create_page_1()
        self.pages["Page 2"] = self.create_page_2()
        self.pages["Page 3"] = self.create_page_3()
        self.pages["Page 4"] = self.create_page_4()
        self.pages["Page 5"] = self.create_page_5()
        self.pages["Page 6"] = self.create_page_6()
        self.pages["Page 7"] = self.create_page_7()
        self.pages["Page 8"] = self.create_page_8()
        self.pages["Page 9"] = self.create_page_9()
        self.pages["Page 10"] = self.create_page_10()

        # Start with the first page
        self.show_page("Page 1")
        
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
        print(f"Rooms: {self.sortroom}")
        
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
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(1, "Page 3"))
        # Button Floor 2
        button_frame = canvas.create_rectangle(450, 285, 820, 385, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(2, "Page 3"))
        # Button Floor 3
        button_frame = canvas.create_rectangle(450, 415, 820, 515, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(3, "Page 3"))
        
        # Button Floor OK
        button_frame = canvas.create_rectangle(830, 450, 1000, 600, outline="black", width=self.Outline)  
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.show_page("Page 4"))
        
        # Floor 1, 2, 3 images
        canvas.create_image(250, 385, anchor="center", image=self.image1)
        canvas.overlay_image1 = self.image1  
        canvas.create_image(250, 298, anchor="center", image=self.image2)
        canvas.overlay_image2 = self.image2  
        canvas.create_image(250, 207, anchor="center", image=self.image3)
        canvas.overlay_image3 = self.image3
        
        # Floor Stats Green Box 
        stata_box1 = canvas.create_oval(180, 375, 200, 395, fill="green", outline="black", width=0)
        stata_box2 = canvas.create_oval(180, 290, 200, 310, fill="green", outline="black", width=0)
        stata_box3 = canvas.create_oval(180, 200, 200, 220, fill="green", outline="black", width=0)

        
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

        self.gif_frames = []
        try:
            gif = self.gif1  # <-- Your GIF path
            while True:
                frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
                self.gif_frames.append(frame)
                gif.seek(len(self.gif_frames))  # Move to next frame
        except EOFError:
            pass  # End of GIF
        
        self.gif_frame_index = 0
        self.animate_gif()
        
        
        # ปุ่มวางทับ GIF
        overlay_button = tk.Button(
            page_frame,
            text="กดที่นี่",
            font=("Helvetica", 16),
            bg="lightblue",
            command=lambda: self.show_page("Page 6")
        )
        # ใช้พิกัดเดียวกันกับ gif_label (หรือปรับตำแหน่งตามที่ต้องการ)
        overlay_button.place(relx=0.95, rely=0.95, anchor='se')  # ขวาล่าง
        return page_frame
    
    def create_page_6(self):
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
            gif = Image.open("Image/end.gif")  # <-- Your GIF path
            while True:
                frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
                self.gif_frames.append(frame)
                gif.seek(len(self.gif_frames))  # Move to next frame
        except EOFError:
            pass  # End of GIF
        
        self.gif_frame_index = 0
        self.animate_gif()
        
        
        # ปุ่มวางทับ GIF
        overlay_button = tk.Button(
            page_frame,
            text="กดที่นี่",
            font=("Helvetica", 16),
            bg="lightblue",
            command=lambda: self.show_page("Page 2")
        )
        # ใช้พิกัดเดียวกันกับ gif_label (หรือปรับตำแหน่งตามที่ต้องการ)
        overlay_button.place(relx=0.95, rely=0.95, anchor='se')  # ขวาล่าง
           
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
        if self.current_page is not None:
            self.current_page.pack_forget()
    
        # Reload Page 5 dynamically to always get latest GIF
        if page_name == "Page 5":
            self.pages["Page 5"] = self.create_page_5()

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
            self.room1 = room_value
        elif self.floor == 2:
            self.room2 = room_value
        elif self.floor == 3:
            self.room3 = room_value

        # Ensure room1, room2, and room3 are not None before sorting
        room_values = [
        self.room1 if self.room1 is not None else 0,
        self.room2 if self.room2 is not None else 0,
        self.room3 if self.room3 is not None else 0,
    ]
        self.sortroom = [value for value in sorted(set(room_values)) if value != 0]

        
        overlay_image1 = PhotoImage(file="Image/R1.png")
        overlay_image2 = PhotoImage(file="Image/R2.png")
        overlay_image3 = PhotoImage(file="Image/R3.png")
        overlay_image4 = PhotoImage(file="Image/R4.png")
        overlay_image5 = PhotoImage(file="Image/R5.png")
        
        gif_image1 = Image.open("Image/animation1.gif")
        gif_image2 = Image.open("Image/animation2.gif")
        gif_image3 = Image.open("Image/animation3.gif")
        gif_image4 = Image.open("Image/animation4.gif")
        gif_image5 = Image.open("Image/animation5.gif")

        image_floor1 = [overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        image_floor2 = [overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        image_floor3 = [overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        
        gif_floor1 = [gif_image1, gif_image2, gif_image3, gif_image4, gif_image5]
        gif_floor2 = [gif_image1, gif_image2, gif_image3, gif_image4, gif_image5]
        gif_floor3 = [gif_image1, gif_image2, gif_image3, gif_image4, gif_image5]
        

        if self.floor == 1 and 1 <= self.room <= 5:
            self.image1 = image_floor1[self.room - 1]
            self.gif1 = gif_floor1[self.room - 1]
        elif self.floor == 2 and 1 <= self.room <= 5:
            self.image2 = image_floor2[self.room - 1]
            self.gif2 = gif_floor2[self.room - 1]
        elif self.floor == 3 and 1 <= self.room <= 5:
            self.image3 = image_floor3[self.room - 1]
            self.gif3 = gif_floor3[self.room - 1]

        # Refresh Page
        page_creators = {
            "Page 2": self.create_page_2,
            "Page 3": self.create_page_3,
            "Page 5": self.create_page_5,
            "Page 6": self.create_page_6,
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
            self.root.after(1000, self.animate_gif)  # Adjust timing (ms) for frame delay


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiPageApp(root)
    
    # Example: Switch to Page 2 after 3 seconds
    root.after(1000, app.change_page, "Page 2")
    root.mainloop()
