import tkinter as tk

class VariableViewer(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Variable Viewer")
        self.geometry("400x300")

        # Example variables to display
        self.variables = {
            "Camera Status": "Active" if self.controller.camera_manager.vid.isOpened() else "Inactive",
            "Serial Port": self.controller.serial_manager.ser.port,
            "Baudrate": self.controller.serial_manager.ser.baudrate,
            "Now Page": self.controller.current_page,
            "Floor": self.controller.food_setup.floor,
            "Room": self.controller.food_setup.room,
            "Room (sort)" : self.controller.food_setup.sortroom,
        }

        # Create labels to display variables
        self.labels = {}
        for idx, (key, value) in enumerate(self.variables.items()):
            tk.Label(self, text=f"{key}:", font=("Helvetica", 12)).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            self.labels[key] = tk.Label(self, text=value, font=("Helvetica", 12))
            self.labels[key].grid(row=idx, column=1, sticky="w", padx=10, pady=5)

        # Add a refresh button
        refresh_button = tk.Button(self, text="On/Off Outline", command=self.refresh_variables)
        refresh_button.grid(row=len(self.variables), column=0, columnspan=2, pady=10)
        
        # Start auto-refresh
        self.auto_refresh()

    def refresh_variables(self):
        # Update variable values
        self.variables["Camera Status"] = "Active" if self.controller.camera_manager.vid.isOpened() else "Inactive"
        self.variables["Serial Port"] = self.controller.serial_manager.ser.port
        self.variables["Baudrate"] = self.controller.serial_manager.ser.baudrate
        self.variables["Now Page"] = self.controller.current_page  
        self.variables["Floor"] = self.controller.food_setup.floor  
        self.variables["Room"] = self.controller.food_setup.room 
        self.variables["Room (sort)"] = self.controller.food_setup.sortroom

        # Update labels
        for key, label in self.labels.items():
            label.config(text=self.variables[key])
    
    def auto_refresh(self):
        self.refresh_variables()
        if self.winfo_exists():
            self.after(1000, self.auto_refresh)  # Refresh every 1000 milliseconds (1 second)