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
        
        overlay_image1 = PhotoImage(file="Image/R1.png")
        overlay_image2 = PhotoImage(file="Image/R2.png")
        overlay_image3 = PhotoImage(file="Image/R3.png")
        overlay_image4 = PhotoImage(file="Image/R4.png")
        overlay_image5 = PhotoImage(file="Image/R5.png")
        
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
        
       
          # <- Use your own image file
        canvas.create_image(350, 100, anchor="center", image=overlay_image1)
        canvas.overlay_image = overlay_image1  # Prevent garbage collection


        return page_frame

    def create_page_3(self):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.Width, height=self.Height)
        canvas.pack(fill="both", expand=True)
        
        # Set background image
        bg_image = PhotoImage(file="Image/3.png")  # Update with your image file
        canvas.create_image(0, 0, anchor="nw", image=bg_image)
        canvas.image = bg_image
        
        label = tk.Label(page_frame, text="Page 3", font=("Helvetica", 24))
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        
        # สร้างกรอบแทนปุ่ม (rectangle)
        button_frame = canvas.create_rectangle(250, 220, 390, 360, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(1, "Page 2"))
        # สร้างกรอบแทนปุ่ม (rectangle)
        # สร้างกรอบแทนปุ่ม (rectangle)
        button_frame = canvas.create_rectangle(480, 220, 620, 360, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(2, "Page 2"))
        # สร้างกรอบแทนปุ่ม (rectangle)
        
        # สร้างกรอบแทนปุ่ม (rectangle)
        button_frame = canvas.create_rectangle(710, 220, 860, 360, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(2, "Page 2"))
        # สร้างกรอบแทนปุ่ม (rectangle)
        
        button_frame = canvas.create_rectangle(370, 380, 510, 520, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(3, "Page 2"))
        # สร้างกรอบแทนปุ่ม (rectangle)
        
        button_frame = canvas.create_rectangle(600, 380, 740, 520, outline="black", width=self.Outline)  # กำหนดตำแหน่งของกรอบ
        # ผูกการคลิกกรอบให้ไปหน้า 2
        canvas.tag_bind(button_frame, "<Button-1>", lambda event: self.set_room_and_go(3, "Page 2"))
        # สร้างกรอบแทนปุ่ม (rectangle)
        
    

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
        self.change_page(page_name)
        if page_name == "Page 2":
            self.pages["Page 2"] = self.create_page_2()  # Recreate with updated room
        if page_name == "Page 3":
            self.pages["Page 3"] = self.create_page_3()  # Recreate with updated room


    def change_page(self, page_name):
        self.show_page(page_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiPageApp(root)
    
    # Example: Switch to Page 2 after 3 seconds
    root.after(1000, app.change_page, "Page 2")
    root.mainloop()
