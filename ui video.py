import tkinter as tk
from PIL import Image, ImageTk
import cv2

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Simple Video Player")

        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.label = tk.Label(root)
        self.label.pack()

        self.play_video()

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            self.root.after(60, self.play_video)
        else:
            # Reset the video to the beginning and play again
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.play_video()

# ใช้งาน
if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root, "Video/test.mp4")  # เปลี่ยนเป็น path ของวิดีโอ
    root.mainloop()