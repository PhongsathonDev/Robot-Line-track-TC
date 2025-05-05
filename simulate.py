import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):
    NUM_SHELVES = 3
    NUM_ROOMS = 5

    def __init__(self):
        super().__init__()
        self.title("Shelf-to-Room Simulator")
        self.geometry("400x400")

        # State variables
        # mapping as list: each element is room number for a shelf, list excludes unassigned shelves
        self.mapping = []
        self.delivered = set()
        self.selected_room = None
        self.current_page = None

        # Friendly names for pages
        self.page_names = {
            SetupPage: "หน้าตั้งค่าส่งสินค้า",
            RoomPage: "หน้าเลือกห้อง",
            ShelfPage: "หน้าเลือกชั้น"
        }

        # Debug button
        debug_btn = tk.Button(self, text="ดูตัวแปร", command=self.open_variable_viewer)
        debug_btn.pack(side="top", anchor="ne", padx=5, pady=5)

        # Container for pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Status bar
        self.status_label = tk.Label(self, text="", bd=1, relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

        # Initialize page frames
        self.frames = {}
        for F in (SetupPage, RoomPage, ShelfPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show first page
        self.show_frame(SetupPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        # Update current page state and status bar
        self.current_page = self.page_names.get(page, page.__name__)
        self.status_label.config(text=f"หน้าปัจจุบัน: {self.current_page}")
        # Refresh dynamic content
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def reset(self):
        # Reset mapping list and delivered set
        self.mapping = []
        self.delivered.clear()
        self.frames[SetupPage].reset()
        self.show_frame(SetupPage)

    def open_variable_viewer(self):
        VariableViewer(self)

class VariableViewer(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Variable Viewer")
        self.geometry("400x300")

        # Variables to display
        self.variables = {
            "Mapping": str(self.controller.mapping),
            "Delivered": str(sorted(self.controller.delivered)),
            "Selected Room": str(self.controller.selected_room),
            "Current Page": self.controller.current_page,
            "Pending": str(getattr(self.controller, 'pending', [])),  
            "Remaining": str(getattr(self.controller, 'remaining', [])),
            "Room": str(self.controller.selected_room),
        }

        self.labels = {}
        for idx, (key, value) in enumerate(self.variables.items()):
            tk.Label(self, text=f"{key}:", font=("Helvetica", 12)).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            lbl = tk.Label(self, text=value, font=("Helvetica", 12))
            lbl.grid(row=idx, column=1, sticky="w", padx=10, pady=5)
            self.labels[key] = lbl

        self.auto_refresh()

    def refresh_variables(self):
        self.variables["Mapping"] = str(self.controller.mapping)
        self.variables["Delivered"] = str(sorted(self.controller.delivered))
        self.variables["Selected Room"] = str(self.controller.selected_room)
        self.variables["Current Page"] = self.controller.current_page
        self.variables["Pending"] = str(getattr(self.controller, 'pending', []))  
        self.variables["Remaining"] = str(getattr(self.controller, 'remaining', []))  
        self.variables["Room"] = str(self.controller.selected_room)
        for key, lbl in self.labels.items():
            lbl.config(text=self.variables[key])

    def auto_refresh(self):
        self.refresh_variables()
        if self.winfo_exists():
            self.after(1000, self.auto_refresh)

class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="กำหนดชั้นที่จะส่งสินค้า (เลือกอย่างน้อย 1)").pack(pady=10)

        self.dropdown_vars = {}
        rooms = [""] + [str(r) for r in range(1, controller.NUM_ROOMS+1)]
        for i in range(1, controller.NUM_SHELVES+1):
            tk.Label(self, text=f"ชั้น {i} ไปห้อง:").pack()
            var = tk.StringVar(value="")
            opt = tk.OptionMenu(self, var, *rooms, command=lambda _: self.check_ready())
            opt.pack()
            self.dropdown_vars[i] = var

        self.next_btn = tk.Button(self, text="ถัดไป", state="disabled", command=self.next)
        self.next_btn.pack(pady=20)

    def check_ready(self):
        ready = any(v.get() for v in self.dropdown_vars.values())
        self.next_btn.config(state="normal" if ready else "disabled")

    def next(self):
        # Build mapping list without None
        mapping = []
        for i in range(1, self.controller.NUM_SHELVES+1):
            val = self.dropdown_vars[i].get()
            if val:
                mapping.append(int(val))
        if not mapping:
            messagebox.showerror("Error", "กรุณาเลือกอย่างน้อย 1 ชั้น")
            return
        self.controller.mapping = mapping
        self.controller.delivered.clear()
        self.controller.show_frame(RoomPage)

    def reset(self):
        for var in self.dropdown_vars.values():
            var.set("")
        self.check_ready()

class RoomPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = tk.Label(self, text="เลือกห้องที่จะส่งสินค้า")
        self.label.pack(pady=10)
        btn_frame = tk.Frame(self)
        btn_frame.pack()
        self.room_buttons = {}
        for r in range(1, controller.NUM_ROOMS+1):
            b = tk.Button(btn_frame, text=f"ห้อง {r}", width=10,
                          command=lambda room=r: self.select_room(room))
            b.grid(row=(r-1)//3, column=(r-1)%3, padx=5, pady=5)
            self.room_buttons[r] = b

    def on_show(self):
        mapping = self.controller.mapping
        delivered = self.controller.delivered
        # Shelves pending overall
        pending_shelves = [i for i in range(1, len(mapping)+1) if i not in delivered]
        pending_rooms = sorted({mapping[i-1] for i in pending_shelves}) if pending_shelves else []
        if not pending_rooms:
            self.label.config(text="ไม่มีสินค้าค้างส่ง")
        else:
            next_room = pending_rooms[0]
            rooms_str = ", ".join(map(str, pending_rooms))
            self.label.config(text=f"ห้องที่ยังเหลือส่ง: {rooms_str} (ควรเลือกห้อง {next_room} ก่อน)")
        # Enable all room buttons
        for btn in self.room_buttons.values():
            btn.config(state="normal")

    def select_room(self, room):
        mapping = self.controller.mapping
        delivered = self.controller.delivered
        pending_shelves = [i for i in range(1, len(mapping)+1) if i not in delivered]
        pending_rooms = sorted({mapping[i-1] for i in pending_shelves}) if pending_shelves else []
        if not pending_rooms:
            messagebox.showerror("Error", f"ไม่มีสินค้าค้างส่งสำหรับห้อง {room}")
            return
        if room not in pending_rooms:
            messagebox.showerror("Error", f"ห้อง {room} ไม่มีสินค้าสำหรับส่ง")
            return
        next_room = pending_rooms[0]
        if room != next_room:
            messagebox.showwarning("แจ้งเตือน", f"กรุณาเลือกห้อง {next_room} ก่อน")
            return
        self.controller.selected_room = room
        self.controller.show_frame(ShelfPage)

class ShelfPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = tk.Label(self, text="เลือกชั้นที่จะนำสินค้าไปวาง")
        self.label.pack(pady=10)
        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack()

    def on_show(self):
        mapping = self.controller.mapping
        room = self.controller.selected_room
        delivered = self.controller.delivered
        for widget in self.btn_frame.winfo_children():
            widget.destroy()
        # คำนวณ pending shelves
        pending = [i for i, rm in enumerate(mapping, start=1) if rm == room and i not in delivered]
        self.controller.pending = pending  # เก็บค่า pending ใน controller
        self.label.config(text=f"ห้อง {room}: ยังเหลือชั้น {', '.join(map(str, pending))} ต้องส่ง")
        for i, rm in enumerate(mapping, start=1):
            state = "disabled" if i in delivered else "normal"
            btn = tk.Button(self.btn_frame, text=f"ชั้น {i}", width=10, state=state,
                            command=lambda s=i: self.attempt_delivery(s))
            btn.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)

    def attempt_delivery(self, shelf):
        mapping = self.controller.mapping
        room = self.controller.selected_room
        if mapping[shelf-1] != room:
            messagebox.showerror("Error", f"ชั้น {shelf} ไม่ใช่สินค้าสำหรับห้อง {room}")
            return
        self.controller.delivered.add(shelf)
        messagebox.showinfo("สำเร็จ", f"ส่งสินค้า ชั้น {shelf} ไปห้อง {room} สำเร็จ")
        # คำนวณ remaining shelves
        remaining = [i for i, rm in enumerate(mapping, start=1) if rm == room and i not in self.controller.delivered]
        self.controller.remaining = remaining  # เก็บค่า remaining ใน controller
        if remaining:
            self.on_show()
        else:
            if len(self.controller.delivered) < len(mapping):
                self.controller.show_frame(RoomPage)
            else:
                messagebox.showinfo("ครบถ้วน", "ส่งสินค้าจนครบทุกชั้นแล้ว ระบบจะรีเซ็ต")
                self.controller.reset()

if __name__ == "__main__":
    app = App()
    app.mainloop()
