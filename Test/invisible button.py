import tkinter as tk

class InvisibleButtonApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Invisible Button UI")
        self.geometry("400x300")

        # Optional background label
        self.bg_label = tk.Label(self, text="Click the invisible areas!", font=("Arial", 16))
        self.bg_label.pack(pady=50)

        # Create the two invisible buttons
        self.create_invisible_buttons()

    def create_invisible_buttons(self):
        # Invisible button 1 (Go)
        invisible_btn1 = tk.Button(
            self,
            text="",
            command=self.on_go_click,
            borderwidth=1,
            highlightthickness=0,
            bg=self["bg"],
            activebackground=self["bg"]
        )
        invisible_btn1.place(x=50, y=100, width=150, height=100)

        # Invisible button 2 (Back)
        invisible_btn2 = tk.Button(
            self,
            text="",
            command=self.on_back_click,
            borderwidth=1,
            highlightthickness=0,
            bg=self["bg"],
            activebackground=self["bg"]
        )
        invisible_btn2.place(x=200, y=100, width=150, height=100)

    def on_go_click(self):
        print("Go button clicked!")

    def on_back_click(self):
        print("Back button clicked!")

if __name__ == "__main__":
    app = InvisibleButtonApp()
    app.mainloop()
