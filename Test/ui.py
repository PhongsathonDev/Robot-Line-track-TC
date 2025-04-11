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
        self.floor = None
        
        # Initialize image placeholders to avoid AttributeError
        self.image1 = None
        self.image2 = None
        self.image3 = None

        # Create the pages
        self.pages["Page 1"] = self.create_page_1()
        self.pages["Page 2"] = self.create_page_2()
        self.pages["Page 3"] = self.create_page_3()
        self.pages["Page 4"] = self.create_page_4()
        self.pages["Page 5"] = self.create_page_5()

        # Start with the first page
        self.show_page("Page 1")

    def create_page_1(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/1.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        label = tk.Label(page_frame, text="Page 1", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')

        return page_frame

    def create_page_2(self):
        print(f"Floor {self.floor} Table: {self.room}")
        
        
        
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height,)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/2.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        label = tk.Label(page_frame, text="Page 2", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # สร้างกรอบแทนปุ่ม (rectangle)
        button_frame = canvas.create_rectangle(450, 160, 820, 260, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(1, "Page 3"))
        # สร้างกรอบแทนปุ่ม (rectangle)
        
        button_frame = canvas.create_rectangle(450, 285, 820, 385, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(2, "Page 3"))
        
        button_frame = canvas.create_rectangle(450, 415, 820, 515, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_floor_and_go(3, "Page 3"))
        
                
        canvas.create_image(250, 385, anchor="center", image=self.image1)
        canvas.overlay_image1 = self.image1  # ป้องกันการถูกเก็บขยะ
        canvas.create_image(250, 298, anchor="center", image=self.image2)
        canvas.overlay_image2 = self.image2  # ป้องกันการถูกเก็บขยะ
        canvas.create_image(250, 207, anchor="center", image=self.image3)
        canvas.overlay_image3 = self.image3  # ป้องกันการถูกเก็บขยะ

        # กล่องสี่เหลี่ยมสีเขียว
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
        
        # แสดง page ที่
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
        
        label = tk.Label(page_frame, text="Page 4", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')

        return page_frame

    def create_page_5(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/5.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        label = tk.Label(page_frame, text="Page 5", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')

        return page_frame

    def show_page(self, page_name):
        if self.current_page is not None:
            self.current_page.pack_forget()
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

        overlay_image1 = PhotoImage(file="Image/R1.png")
        overlay_image2 = PhotoImage(file="Image/R2.png")
        overlay_image3 = PhotoImage(file="Image/R3.png")
        overlay_image4 = PhotoImage(file="Image/R4.png")
        overlay_image5 = PhotoImage(file="Image/R5.png")

        image_floor1 = [overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        image_floor2 = [overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]
        image_floor3 = [overlay_image1, overlay_image2, overlay_image3, overlay_image4, overlay_image5]

        if self.floor == 1 and 1 <= self.room <= 5:
            self.image1 = image_floor1[self.room - 1]
        elif self.floor == 2 and 1 <= self.room <= 5:
            self.image2 = image_floor2[self.room - 1]
        elif self.floor == 3 and 1 <= self.room <= 5:
            self.image3 = image_floor3[self.room - 1]

        # Refresh Page 2
        if page_name == "Page 2":
            self.pages["Page 2"] = self.create_page_2()
            self.show_page("Page 2")  # <-- Ensure the refreshed version is shown
        elif page_name == "Page 3":
            self.pages["Page 3"] = self.create_page_3()
            self.show_page("Page 3")

    def change_page(self, page_name):
        self.show_page(page_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiPageApp(root)
    
    # Example: Switch to Page 2 after 3 seconds
    root.after(1000, app.change_page, "Page 2")
    root.mainloop()
