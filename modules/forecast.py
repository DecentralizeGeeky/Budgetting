import tkinter as tk
from tkinter import messagebox, ttk

# Forecast Manager Class
class ForecastManager:
    def __init__(self, db):
        self.db = db

    def input_forecast_details(self, root, callback):
        self.clear_window(root)
        tk.Label(root, text="Input Forecast Details", font=('Arial', 16), fg='white', bg='#FFC107').pack(pady=10)

        item_id = tk.IntVar()
        start_month = tk.StringVar()
        end_month = tk.StringVar()
        forecast_amount = tk.DoubleVar()

        tk.Label(root, text="Item ID").pack()
        tk.Entry(root, textvariable=item_id).pack()

        tk.Label(root, text="Start Month (YYYY-MM)").pack()
        tk.Entry(root, textvariable=start_month).pack()

        tk.Label(root, text="End Month (YYYY-MM)").pack()
        tk.Entry(root, textvariable=end_month).pack()

        tk.Label(root, text="Forecast Amount").pack()
        tk.Entry(root, textvariable=forecast_amount).pack()

        def save_forecast():
            self.db.insert_forecast(item_id.get(), start_month.get(), end_month.get(), forecast_amount.get())
            messagebox.showinfo("Success", "Forecast added successfully!")
            callback()

        tk.Button(root, text="Save Forecast", bg='#FFC107', fg='white', command=save_forecast).pack(pady=10)
        tk.Button(root, text="Cancel", bg='#4CAF50', fg='white', command=callback).pack()

    def clear_window(self, root):
        for widget in root.winfo_children():
            widget.destroy()
