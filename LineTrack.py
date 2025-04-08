import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import serial
import time
import cv2.aruco as aruco

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)

class Robot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Line Track")
        self.geometry("600x500")
        self.configure(bg="#1E90FF")
        self.vid = None
        self.room = None
        self.spincheck = 25
        self.color1 = "green"
        self.color2 = "green"
        self.color3 = "green"
        self.spindelay = 25

        # Aruco Marker Setup
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.aruco_params = aruco.DetectorParameters()
        self.aruco_detector = aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

        self.create_welcome_page()

    def move_forward_hard(self):
        ser.write("forwardHard\n".encode())

    def move_forward_mid(self):
        ser.write("forwardMid\n".encode())

    def move_forward_soft(self):
        ser.write("forwardSoft\n".encode())

    def turn_left_hard(self):
        ser.write("leftHard\n".encode())

    def turn_left_mid(self):
        ser.write("leftMid\n".encode())

    def turn_left_soft(self):
        ser.write("leftSoft\n".encode())

    def turn_right_hard(self):
        ser.write("rightHard\n".encode())

    def turn_right_mid(self):
        ser.write("rightMid\n".encode())

    def turn_right_soft(self):
        ser.write("rightSoft\n".encode())

    def stop(self):
        ser.write("stop\n".encode())

    def spin(self):
        print("spin")
        ser.write("Spin\n".encode())

    def read_from_serial(self):
        if ser.in_waiting:
            try:
                message = str(ser.readline().decode().strip())
                if message == "1off":
                    self.color1 = "red"
                    self.close_camera()
                elif message == "1on":
                    self.color1 = "green"
                    self.close_camera()
                elif message == "2off":
                    self.color2 = "red"
                    self.close_camera()
                elif message == "2on":
                    self.color2 = "green"
                    self.close_camera()
                elif message == "3off":
                    self.color3 = "red"
                    self.close_camera()
                elif message == "3on":
                    self.color3 = "green"
                    self.close_camera()
            except Exception as e:
                print(f"Error reading from serial: {e}")

        self.after(100, self.read_from_serial)

    def create_welcome_page(self):
        self.stop()
        tk.Label(self, text="Select Room", bg="#1E90FF", fg="white", font=('Helvetica', 32, "bold")).pack(pady=50)
        for i in range(3):
            row_frame = tk.Frame(self, bg="#1E90FF")
            row_frame.pack()
            for j in range(3):
                room_count = i * 3 + j + 1
                btn = tk.Button(row_frame, text=f"Room {room_count}", width=20, height=2,
                                command=lambda room=room_count: self.create_camera_page(room))
                btn.pack(side=tk.LEFT, padx=10, pady=20)

        light_frame = tk.Frame(self, bg="#1E90FF")
        light_frame.pack(pady=10)

        tk.Label(light_frame, text=f"ชั้น {1}: ", bg=self.color1, fg="white",
                 font=('Helvetica', 14), width=15, height=2).pack(side=tk.LEFT, padx=20)
        tk.Label(light_frame, text=f"ชั้น {2}: ", bg=self.color2, fg="white",
                 font=('Helvetica', 14), width=15, height=2).pack(side=tk.LEFT, padx=20)
        tk.Label(light_frame, text=f"ชั้น {3}: ", bg=self.color3, fg="white",
                 font=('Helvetica', 14), width=15, height=2).pack(side=tk.LEFT, padx=20)

        self.read_from_serial()

    def create_camera_page(self, room):
        self.room = room
        for widget in self.winfo_children():
            widget.destroy()

        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack()

        tk.Button(self, text="Back", command=self.close_camera).pack(pady=10)
        tk.Button(self, text="OK", command=self.close_camera).pack(pady=10)

        self.update_camera()

    def update_camera(self):
        ret, frame = self.vid.read()
        if not ret or frame is None:
            return

        frame = cv2.resize(frame, (600, 320))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- Aruco Marker Detection ---
        corners, ids, _ = self.aruco_detector.detectMarkers(frame)
        if ids is not None:
            for marker_id in ids.flatten():
                print(f"Aruco Marker ID: {marker_id}, Room: {self.room}")
                if str(marker_id) == str(self.room):
                    self.stop()
                    print(f"Aruco Marker matched Room {self.room}. Robot stopped.")
                    if str(self.room) == "0":
                        self.spin()
                        self.close_camera()
                    else:
                        self.spin()
                        if self.vid is not None:
                            self.vid.release()
                            self.vid = None
                        for widget in self.winfo_children():
                            widget.destroy()
                        self.confirm_close_camera()
                    return
            aruco.drawDetectedMarkers(frame, corners, ids)

        # --- Line Tracking ---
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
                    print("HardLeft")
                    self.turn_left_hard()
                elif cx < width * 0.4:
                    print("MidLeft")
                    self.turn_left_mid()
                elif cx < width * 0.5:
                    print("SoftLeft")
                    self.turn_left_soft()
                elif cx > 2 * width * 0.4:
                    print("HardRight")
                    self.turn_right_hard()
                elif cx > 2 * width * 0.35:
                    print("MidRight")
                    self.turn_right_mid()
                elif cx > 2 * width * 0.3:
                    print("SoftRight")
                    self.turn_right_soft()
                else:
                    self.move_forward_mid()
                    if self.spincheck != 0:
                        self.spincheck -= 1
            else:
                self.stop()
                print("1Spin")
        else:
            if self.spincheck == 0:
                self.spin()
                print("2Spin")
                self.spincheck = 25

        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.delete("all")
        self.canvas.create_image(300, 200, anchor=tk.CENTER, image=self.photo)
        self.after(10, self.update_camera)

    def confirm_close_camera(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Are you sure you want to close the camera?", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(self, text="Yes", command=lambda room=0: self.create_camera_page(room), width=10, bg="red", fg="white").pack(side=tk.LEFT, padx=20, pady=20)

    def close_camera(self):
        if self.vid is not None:
            self.vid.release()
            self.vid = None
        for widget in self.winfo_children():
            widget.destroy()
        self.stop()
        self.create_welcome_page()
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack()
        tk.Button(self, text="Back", command=self.close_camera).pack(pady=10)

if __name__ == '__main__':
    app = Robot()
    app.mainloop()
