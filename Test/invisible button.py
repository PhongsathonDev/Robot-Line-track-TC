import tkinter as tk
from PIL import Image, ImageTk

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Canvas Resize Image Example")
root.geometry("800x600")

# สร้าง Canvas
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# โหลดและย่อภาพ
image_path = "Image/R1.png"  # เปลี่ยน path ตามของคุณ
original_image = Image.open(image_path)

# ย่อขนาดรูปเป็น 100x100 px
resized_image = original_image.resize((5, 5), Image.Resampling.LANCZOS)
tk_image = ImageTk.PhotoImage(resized_image)

# วางภาพลงบน Canvas
canvas.create_image(350, 100, anchor="center", image=tk_image)
canvas.tk_image = tk_image  # ป้องกันไม่ให้ถูก GC

# รันโปรแกรม
root.mainloop()
