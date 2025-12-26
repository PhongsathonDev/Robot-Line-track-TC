


# 🤖 Robot Line Track TC (Food Delivery Robot)

โปรเจกต์นี้เป็นระบบควบคุมหุ่นยนต์ส่งอาหารอัตโนมัติที่ใช้การเดินตามเส้น (Line Tracking) และระบุตำแหน่งโต๊ะด้วย ArUco Markers โดยมีหน้าจอสัมผัส (Touchscreen UI) สำหรับสั่งงาน และระบบเสียงแจ้งเตือนสถานะต่างๆ

## 📋 ภาพรวมระบบ (System Overview)

ระบบแบ่งการทำงานออกเป็น 2 ส่วนหลักที่สื่อสารกันผ่าน Serial Communication:

1. **Main Controller (Python):** รันบนคอมพิวเตอร์บอร์ดเดี่ยว (เช่น Raspberry Pi) ทำหน้าที่ประมวลผลภาพจากกล้อง (Image Processing), แสดงผล UI, จัดการคิวการส่งอาหาร และส่งคำสั่งควบคุมไปยังบอร์ดขับเคลื่อน
2. **Motor & Sensor Controller (Arduino/ESP32):** รับคำสั่งเพื่อขับมอเตอร์ ควบคุมการเคลื่อนที่ และอ่านค่าจากเซนเซอร์อัลตราโซนิกเพื่อเช็คสิ่งกีดขวางและสถานะถาดวางอาหาร

## ✨ ฟีเจอร์หลัก (Features)

* **Line Tracking Navigation:** ใช้กล้องประมวลผลภาพ (OpenCV) เพื่อหาเส้นทางและส่งคำสั่งเลี้ยวซ้าย/ขวา/ตรงไป
* **ArUco Marker Positioning:** ใช้ ArUco Markers (DICT_4X4_50) ในการระบุตำแหน่งโต๊ะหรือจุดจอด
* **Touchscreen UI:** อินเทอร์เฟซใช้งานง่ายด้วย Tkinter สำหรับเลือกชั้นและห้องที่จะไปส่งอาหาร
* **Voice Interaction:** มีเสียงแจ้งเตือนเมื่ออาหารมาถึง ("Food Arrived"), ให้หลีกทาง ("Make Way"), และขอบคุณเมื่อหยิบอาหารออก ("Enjoy Food")
* **Obstacle Avoidance:** มีเซนเซอร์ด้านหน้าสำหรับหยุดเมื่อเจอสิ่งกีดขวาง
* **Tray Detection:** เซนเซอร์ตรวจจับว่ามีอาหารวางอยู่บนชั้นวางหรือไม่

## 🛠️ โครงสร้างฮาร์ดแวร์ (Hardware Setup)

### การต่อสาย (Pinout Configuration)

*อ้างอิงจากไฟล์ `Motor.ino` (บอร์ด ESP32)*

**Motor Connections:**

* **Left Front:** IN1 (25), IN2 (26)
* **Left Rear:** IN1 (23), IN2 (22)
* **Right Front:** IN1 (27), IN2 (14)
* **Right Rear:** IN1 (19), IN2 (18)

**Ultrasonic Sensors:**

* **Front (กันชนหน้า):** Trig (2), Echo (4)
* **Shelf 1 (ชั้น 1):** Trig (32), Echo (33)
* **Shelf 2 (ชั้น 2):** Trig (12), Echo (13)
* **Shelf 3 (ชั้น 3):** Trig (21), Echo (5)

## 💻 การติดตั้งซอฟต์แวร์ (Software Installation)

### 1. Python Environment (Main Controller)

ตรวจสอบให้แน่ใจว่าติดตั้ง Python 3.x และไลบรารีที่จำเป็นแล้ว:

```bash
pip install opencv-python opencv-contrib-python pyserial pygame pillow

```

*หมายเหตุ: บน Linux/Raspberry Pi อาจต้องติดตั้ง `python3-tk` เพิ่มเติม*

### 2. Arduino Firmware

อัปโหลดไฟล์ `Motor.ino` ลงในบอร์ด Microcontroller โดยตั้งค่า Baudrate เป็น `115200`

## 🚀 วิธีการใช้งาน (Usage)

1. เชื่อมต่อกล้องและบอร์ด Microcontroller เข้ากับคอมพิวเตอร์หลัก
2. รันโปรแกรม Python:
```bash
python Main-V2.py

```


3. **หน้าจอ UI:**
* เลือกชั้น (Floor) และห้อง (Room) ที่ต้องการไปส่ง
* กด "OK" เพื่อเริ่มภารกิจ


4. **การทำงาน:**
* หุ่นยนต์จะเดินตามเส้นและสแกน ArUco Code
* เมื่อถึงโต๊ะที่กำหนด (ID ตรงกัน) หุ่นยนต์จะหมุนตัวและแจ้งเตือน
* เมื่อลูกค้าหยิบอาหารออก (เซนเซอร์ที่ชั้นวางตรวจจับได้) หุ่นยนต์จะกล่าวขอบคุณและกลับฐาน



## 📂 โครงสร้างไฟล์ (File Structure)

* `Main-V2.py`: โค้ดหลัก Python ควบคุม UI, กล้อง, และ Logic ทั้งหมด
* `Motor.ino`: โค้ด Arduino สำหรับควบคุมมอเตอร์และอ่านค่าเซนเซอร์
* `Image/`: โฟลเดอร์เก็บรูปภาพ UI และไฟล์ Animation (.gif)
* `Voice/`: โฟลเดอร์เก็บไฟล์เสียง (.wav, .mp3)
* `Sub/`: โฟลเดอร์สำหรับโมดูลย่อย (เช่น Debugger)
