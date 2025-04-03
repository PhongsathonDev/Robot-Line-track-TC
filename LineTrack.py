import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode

import numpy as np

class Robot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Line Track")
        self.geometry("600x500")
        self.configure(bg="#1E90FF")
        self.vid = None  # Initialize video capture variable
        self.room = None  # Initialize room variable
        self.create_welcome_page()
        self.spindelay = 25

    def create_welcome_page(self):
        tk.Label(self, text="Select Room",
                 bg="#1E90FF",  
                 fg="white",  
                 font=('Helvetica', 32, "bold")).pack(pady=50)
        
        for i in range(3):
            row_frame = tk.Frame(self, bg="#1E90FF")
            row_frame.pack()
            for j in range(3):
                room_count = i * 3 + j + 1
                btn = tk.Button(row_frame, text=f"Room {room_count}", width=20, height=2, 
                                command=lambda room=room_count: self.create_camera_page(room))
                btn.pack(side=tk.LEFT, padx=10, pady=20)

    def create_camera_page(self, room):
        # Switch to the Camera Page
        self.room = room
        for widget in self.winfo_children():  # Clear previous widgets
            widget.destroy()

        self.vid = cv2.VideoCapture("test.mp4")  # Open camera
        self.width, self.height = 600, 320
        
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack()
        
        self.btn_quit = tk.Button(self, text="Back", command=self.close_camera)
        self.btn_quit.pack(pady=10)
        
        self.btn_quit = tk.Button(self, text="OK", command=self.close_cameraa)
        self.btn_quit.pack(pady=10)

        self.update_camera()

    def update_camera(self):
        ret, frame = self.vid.read()
        if ret:
        # QR code Scan----------------------------------------
            frame = cv2.resize(frame, (600, 320))
            for qr in decode(frame):
                qr_data = qr.data.decode('utf-8')
                print(f"QR Code: {qr_data}, Room: {self.room}")
                
                # Draw a rectangle around the QR code
                points = qr.polygon
                if len(points) == 4:
                    pts = [(point.x, point.y) for point in points]
                    cv2.polylines(frame, [np.array(pts, np.int32)], True, (0, 255, 0), 2)
                if str(qr_data) == str("30"):
                    self.close_camera()
                elif str(qr_data) == str(self.room):
                    print(f"Room {self.room} stop")
                    self.confirm_close_camera()

        # Line Track-----------------------------------------
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
                    
                    # Logic for movement based on center position-------------------
                    if cx < width * 0.3:
                        print("HardLeft")
                        # turn_left_mid()
                    elif cx < width * 0.4:
                        print("MidLeft")
                        # turn_left_mid()
                    elif cx < width * 0.5:
                        print("SoftLeft")
                        # turn_left_mid()
                    elif cx > 2 * width * 0.4:
                        print("HardRight")
                        # turn_right_mid()
                    elif cx > 2 * width * 0.35:
                        print("MidRight")
                        # turn_right_mid()
                    elif cx > 2 * width * 0.3:
                        print("SoftRight")
                        # turn_right_mid()
                    else:
                        #move_forward_mid()
                        if self.spindelay != 0:
                            self.spindelay = self.spindelay-1
                else:
                    #stop()
                    print("1Spin")
            else:
                if self.spindelay == 0:
                    #spin()
                    print("2Spin")
                    self.spindelay = 25
        
        # Display video in Tkinter-------------------------------
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.delete("all")
        self.canvas.create_image(self.width // 2, self.height // 2, anchor=tk.CENTER, image=self.photo)
        self.after(10, self.update_camera)

    def confirm_close_camera(self):
        """Show confirmation button to close the camera"""
        for widget in self.winfo_children():
            widget.destroy()  # Clear previous UI
        
        tk.Label(self, text="Are you sure you want to close the camera?", font=("Helvetica", 16)).pack(pady=20)
        
        btn_yes = tk.Button(self, text="Yes", command=lambda room=30: self.create_camera_page(room), width=10, bg="red", fg="white")
        btn_yes.pack(side=tk.LEFT, padx=20, pady=20)

    def close_camera(self):
        """Close camera and return to main page"""
        if self.vid is not None:
            self.vid.release()
            self.vid = None

        # Clear UI and go back to welcome page
        for widget in self.winfo_children():
            widget.destroy()

        self.create_welcome_page()
        
    def close_cameraa(self):
        """Close camera and return to main page"""
        if self.vid is not None:
            self.vid.release()
            self.vid = None

        # Clear UI and go back to welcome page
        for widget in self.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack()
        self.btn_quit = tk.Button(self, text="Back", command=self.close_camera)
        self.btn_quit.pack(pady=10)

if __name__ == '__main__':
    app = Robot()
    app.mainloop()
    app = Robot()
    app.mainloop()