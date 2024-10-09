import tkinter as tk
from tkinter import  ttk
from modules.database_manager import DatabaseManager
from modules.record import RecordManager
from modules.forecast import ForecastManager


# Main Application Class
class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseManager()
        self.record_manager = RecordManager(self.db)
        self.forecast_manager = ForecastManager(self.db)

        self.root.title("Budget Record Management System")
        self.root.geometry("600x600")
        self.root.configure(bg='#ECEFF1')

        self.main_menu()

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Budget Record Management System", font=('Arial', 18), fg='white', bg='#4CAF50').pack(pady=20)

        tk.Button(self.root, text="Enter Record", width=30, bg='#4CAF50', fg='white', command=self.enter_record_menu).pack(pady=5)
        tk.Button(self.root, text="View Records", width=30, bg='#2196F3', fg='white', command=lambda: self.record_manager.list_records(self.root, self.main_menu)).pack(pady=5)
        tk.Button(self.root, text="Enter Forecast", width=30, bg='#FFC107', fg='white', command=self.forecast_menu).pack(pady=5)
        tk.Button(self.root, text="Exit", width=30, bg='#f44336', fg='white', command=self.root.quit).pack(pady=5)

    def enter_record_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Enter Record Sub-Menu", font=('Arial', 16), fg='white', bg='#4CAF50').pack(pady=10)

        tk.Button(self.root, text="Create Record", width=30, bg='#4CAF50', fg='white', command=lambda: self.record_manager.create_record(self.root, self.main_menu)).pack(pady=5)
        tk.Button(self.root, text="Delete Record", width=30, bg='#f44336', fg='white', command=lambda: self.record_manager.delete_record(self.root, self.main_menu)).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", width=30, bg='#2196F3', fg='white', command=self.main_menu).pack(pady=5)

    def forecast_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Forecast Sub-Menu", font=('Arial', 16), fg='white', bg='#FFC107').pack(pady=10)

        tk.Button(self.root, text="Input Forecast Details", width=30, bg='#FFC107', fg='white', command=lambda: self.forecast_manager.input_forecast_details(self.root, self.main_menu)).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", width=30, bg='#2196F3', fg='white', command=self.main_menu).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
