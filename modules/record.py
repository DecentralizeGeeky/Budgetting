import tkinter as tk
from tkinter import messagebox, ttk

# Record Manager Class
class RecordManager:
    def __init__(self, db):
        self.db = db

    def create_record(self, root, callback):
        self.clear_window(root)
        tk.Label(root, text="Create New Record", font=('Arial', 16), fg='white', bg='#4CAF50').pack(pady=10)

        item_name = tk.StringVar()
        amount = tk.DoubleVar()
        quantity = tk.IntVar()
        date = tk.StringVar()
        department = tk.StringVar()

        tk.Label(root, text="Item Name").pack()
        tk.Entry(root, textvariable=item_name).pack()

        tk.Label(root, text="Amount").pack()
        tk.Entry(root, textvariable=amount).pack()

        tk.Label(root, text="Quantity").pack()
        tk.Entry(root, textvariable=quantity).pack()

        tk.Label(root, text="Date (YYYY-MM-DD)").pack()
        tk.Entry(root, textvariable=date).pack()

        tk.Label(root, text="Department").pack()
        department_menu = ttk.Combobox(root, textvariable=department, values=["HR", "Finance", "IT", "Sales", "Admin"])
        department_menu.pack()

        def save_record():
            self.db.insert_record(item_name.get(), amount.get(), quantity.get(), date.get(), department.get())
            messagebox.showinfo("Success", "Record added successfully!")
            callback()

        tk.Button(root, text="Save Record", bg='#4CAF50', fg='white', command=save_record).pack(pady=10)
        tk.Button(root, text="Cancel", bg='#f44336', fg='white', command=callback).pack()

    def delete_record(self, root, callback):
        self.clear_window(root)
        tk.Label(root, text="Delete Record", font=('Arial', 16), fg='white', bg='#f44336').pack(pady=10)

        record_id = tk.IntVar()

        tk.Label(root, text="Enter Record ID to Delete").pack()
        tk.Entry(root, textvariable=record_id).pack()

        def remove_record():
            self.db.delete_record(record_id.get())
            messagebox.showinfo("Success", "Record deleted successfully!")
            callback()

        tk.Button(root, text="Delete Record", bg='#f44336', fg='white', command=remove_record).pack(pady=10)
        tk.Button(root, text="Cancel", bg='#4CAF50', fg='white', command=callback).pack()

    def list_records(self, root, callback):
        self.clear_window(root)
        tk.Label(root, text="Budget Records", font=('Arial', 16), fg='white', bg='#2196F3').pack(pady=10)

        records = self.db.fetch_all_records()

        # Create a Treeview widget to display the records in a table format
        tree = ttk.Treeview(root, columns=("ID", "Item", "Amount", "Quantity", "Date", "Department"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Item", text="Item")
        tree.heading("Amount", text="Amount")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Date", text="Date")
        tree.heading("Department", text="Department")
        tree.column("ID", width=30, anchor=tk.CENTER)
        tree.column("Item", width=150, anchor=tk.W)
        tree.column("Amount", width=100, anchor=tk.CENTER)
        tree.column("Quantity", width=80, anchor=tk.CENTER)
        tree.column("Date", width=100, anchor=tk.CENTER)
        tree.column("Department", width=100, anchor=tk.CENTER)

        tree.pack(pady=20)

        # Insert the records into the Treeview
        for record in records:
            tree.insert('', tk.END, values=record)

        tk.Button(root, text="Return to Main Menu", bg='#4CAF50', fg='white', command=callback).pack(pady=10)

    def clear_window(self, root):
        for widget in root.winfo_children():
            widget.destroy()