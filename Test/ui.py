import tkinter as tk
from PIL import Image, ImageTk

class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi Page App with Background Image")
        self.geometry("1024x600")
        self.current_page = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # โหลดภาพพื้นหลัง (ใส่ path รูปของคุณ)
        self.bg_images = {
            "Page1": ImageTk.PhotoImage(Image.open("Image/1.png").resize((1024, 600))),
            "Page2": ImageTk.PhotoImage(Image.open("Image/2.png").resize((1024, 600))),
            "Page3": ImageTk.PhotoImage(Image.open("Image/3.png").resize((1024, 600))),
            "Page4": ImageTk.PhotoImage(Image.open("Image/1.png").resize((1024, 600))),
            "Page5": ImageTk.PhotoImage(Image.open("Image/1.png").resize((1024, 600))),
        }

        self.page_order = ["Page1", "Page2", "Page3", "Page4", "Page5"]

        self.pages = {
            "Page1": self.create_page1(),
            "Page2": self.create_page2(),
            "Page3": self.create_page3(),
            "Page4": self.create_page4(),
            "Page5": self.create_page5(),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("Page1")

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.lower()
        self.current_page = self.pages[page_name]
        self.current_page.lift()

    def create_nav_bar(self, frame, current_index, page_key):
        nav = tk.Frame(frame, bg="black")
        nav.pack(side="bottom", fill="x", pady=10)

        btn_style = {
            "bg": "black",
            "fg": "white",
            "activebackground": "white",
            "activeforeground": "white",
            "relief": "flat",
            "borderwidth": 0,
            "highlightthickness": 0
        }

        if current_index > -1:
            tk.Button(nav, text="⬅ Back", command=lambda: self.show_page(self.page_order[current_index - 1]),
                    width=10, height=2, **btn_style).pack(side="left", padx=10)

        if current_index < len(self.page_order) - 0:
            tk.Button(nav, text="Next ➡", command=lambda: self.show_page(self.page_order[current_index + 1]),
                    width=10, height=2, **btn_style).pack(side="right", padx=10)

        jump_nav = tk.Frame(nav, bg="black")
        jump_nav.pack(expand=True)
        for i, name in enumerate(self.page_order):
            tk.Button(jump_nav, text=f"Page {i+1}", command=lambda name=name: self.show_page(name),
                    width=10, height=2, **btn_style).pack(side="left", padx=5)

    def create_page1(self):
        frame = tk.Frame(self.container)
        bg_label = tk.Label(frame, image=self.bg_images["Page1"])
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Label(frame, text="Page 1", font=("Helvetica", 28), bg="black", fg="white").pack(pady=40)
        self.create_nav_bar(frame, 0, "Page1")
        return frame

    def create_page2(self):
        frame = tk.Frame(self.container)
        bg_label = tk.Label(frame, image=self.bg_images["Page2"])
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Label(frame, text="Page 2", font=("Helvetica", 28), fg="white").pack(pady=40)
        self.create_nav_bar(frame, 1, "Page2")
        return frame

    def create_page3(self):
        frame = tk.Frame(self.container)
        bg_label = tk.Label(frame, image=self.bg_images["Page3"])
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Label(frame, text="Page 3", font=("Helvetica", 28), bg="black", fg="white").pack(pady=40)
        self.create_nav_bar(frame, 2, "Page3")
        return frame

    def create_page4(self):
        frame = tk.Frame(self.container)
        bg_label = tk.Label(frame, image=self.bg_images["Page4"])
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Label(frame, text="Page 4", font=("Helvetica", 28), bg="black", fg="white").pack(pady=40)
        self.create_nav_bar(frame, 3, "Page4")
        return frame

    def create_page5(self):
        frame = tk.Frame(self.container)
        bg_label = tk.Label(frame, image=self.bg_images["Page5"])
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Label(frame, text="Page 5", font=("Helvetica", 28), bg="black", fg="white").pack(pady=40)
        self.create_nav_bar(frame, 4, "Page5")
        return frame


if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()
