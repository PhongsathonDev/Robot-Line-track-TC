import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class AnimatedGIFApp:
    def __init__(self, root, gif_path, update_interval=100):
        self.root = root
        self.update_interval = update_interval

        self.lbl = tk.Label(root)
        self.lbl.pack()

        self.gif = Image.open("Image/animation1.gif")
        self.frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(self.gif)]
        self.current_frame = 0

        self.update()

    def update(self):
        frame = self.frames[self.current_frame % len(self.frames)]
        self.lbl.config(image=frame)
        self.current_frame += 1
        self.root.after(self.update_interval, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedGIFApp(root, "Image/animation1.gif")
    root.mainloop()