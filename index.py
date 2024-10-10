import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('event_budget.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS event_budget_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT,
                item_name TEXT,
                unit_price REAL,
                quantity INTEGER,
                total_price REAL,
                date TEXT
            )
        ''')
        self.conn.commit()

    def add_record(self, event, item_name, unit_price, quantity, total_price, date):
        self.c.execute('INSERT INTO event_budget_records (event, item_name, unit_price, quantity, total_price, date) VALUES (?, ?, ?, ?, ?, ?)',
                       (event, item_name, unit_price, quantity, total_price, date))
        self.conn.commit()

    def fetch_all_records(self):
        self.c.execute('SELECT * FROM event_budget_records')
        return self.c.fetchall()

    def update_record(self, record_id, event, item_name, unit_price, quantity, total_price, date):
        self.c.execute('UPDATE event_budget_records SET event = ?, item_name = ?, unit_price = ?, quantity = ?, total_price = ?, date = ? WHERE id = ?',
                       (event, item_name, unit_price, quantity, total_price, date, record_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

class RecordManager:
    def __init__(self, db_manager):
        self.db = db_manager
        # Dictionary of suggested items for each event
        self.suggested_items = {
            "SIWES": ["Laptop", "Stationery", "Transport", "Meals"],
            "Orientation": ["Welcome Kits", "Stationery", "Refreshments"],
            "Seminars": ["Projector", "Refreshments", "Handouts"]
        }

    def clear_window(self, root):
        for widget in root.winfo_children():
            widget.destroy()

    def add_record(self, root, callback):
        self.clear_window(root)
        tk.Label(root, text="Add Event Budget Record", font=('Arial', 16), fg='white', bg='#4CAF50').pack(pady=10)

        event = tk.StringVar()
        item_name = tk.StringVar()
        unit_price = tk.DoubleVar()
        quantity = tk.IntVar()
        date = tk.StringVar()

        tk.Label(root, text="Select Event").pack()
        event_dropdown = ttk.Combobox(root, textvariable=event, values=list(self.suggested_items.keys()))
        event_dropdown.pack()

        tk.Label(root, text="Suggested Item").pack()
        item_dropdown = ttk.Combobox(root, textvariable=item_name)
        item_dropdown.pack()

        # Function to update item dropdown based on selected event
        def update_items(event):
            selected_event = event_dropdown.get()
            item_dropdown['values'] = self.suggested_items.get(selected_event, [])
            item_dropdown.set('')  # Clear previous selection

        event_dropdown.bind("<<ComboboxSelected>>", update_items)

        tk.Label(root, text="Unit Price").pack()
        tk.Entry(root, textvariable=unit_price).pack()

        tk.Label(root, text="Quantity").pack()
        tk.Entry(root, textvariable=quantity).pack()

        tk.Label(root, text="Date (YYYY-MM-DD)").pack()
        tk.Entry(root, textvariable=date).pack()

        def save_record():
            new_event = event.get()
            new_item_name = item_name.get()
            new_unit_price = unit_price.get()
            new_quantity = quantity.get()
            new_total_price = new_unit_price * new_quantity
            new_date = date.get()

            # Add the record to the database
            self.db.add_record(new_event, new_item_name, new_unit_price, new_quantity, new_total_price, new_date)
            messagebox.showinfo("Success", "Record added successfully!")
            callback()

        tk.Button(root, text="Add Record", bg='#4CAF50', fg='white', command=save_record).pack(pady=10)
        tk.Button(root, text="Return to Main Menu", bg='#f44336', fg='white', command=callback).pack()

    def list_records(self, root, callback):
        self.clear_window(root)
        tk.Label(root, text="Event Budgets", font=('Arial', 16), fg='white', bg='#2196F3').pack(pady=10)

        records = self.db.fetch_all_records()

        # Create a Treeview widget to display the records in a table format
        tree = ttk.Treeview(root, columns=("ID", "Event", "Item", "Unit Price", "Quantity", "Total", "Date"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Event", text="Event")
        tree.heading("Item", text="Item")
        tree.heading("Unit Price", text="Unit Price")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Total", text="Total")
        tree.heading("Date", text="Date")
        tree.column("ID", width=30, anchor=tk.CENTER)
        tree.column("Event", width=100, anchor=tk.W)
        tree.column("Item", width=150, anchor=tk.W)
        tree.column("Unit Price", width=100, anchor=tk.CENTER)
        tree.column("Quantity", width=80, anchor=tk.CENTER)
        tree.column("Total", width=100, anchor=tk.CENTER)
        tree.column("Date", width=100, anchor=tk.CENTER)

        tree.pack(pady=20)

        # Insert the records into the Treeview
        for record in records:
            tree.insert('', tk.END, values=record)

        # Button to Edit selected record
        tk.Button(root, text="Edit Selected Record", bg='#FFC107', fg='white',
                  command=lambda: self.edit_record(root, tree, callback)).pack(pady=10)
        tk.Button(root, text="Generate PDF", bg='#FFC107', fg='white', command=self.generate_pdf).pack(pady=10)
        tk.Button(root, text="Return to Main Menu", bg='#4CAF50', fg='white', command=callback).pack(pady=10)

    def edit_record(self, root, tree, callback):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a record to edit.")
            return

        record_id = tree.item(selected_item[0], 'values')[0]
        record = self.db.c.execute("SELECT * FROM event_budget_records WHERE id = ?", (record_id,)).fetchone()

        if record:
            self.clear_window(root)
            tk.Label(root, text="Edit Event Budget Record", font=('Arial', 16), fg='white', bg='#4CAF50').pack(pady=10)

            event = tk.StringVar(value=record[1])
            item_name = tk.StringVar(value=record[2])
            unit_price = tk.DoubleVar(value=record[3])
            quantity = tk.IntVar(value=record[4])
            date = tk.StringVar(value=record[6])

            tk.Label(root, text="Event").pack()
            tk.Entry(root, textvariable=event, state='readonly').pack()  # Set to readonly

            tk.Label(root, text="Item Name").pack()
            tk.Entry(root, textvariable=item_name).pack()

            tk.Label(root, text="Unit Price").pack()
            tk.Entry(root, textvariable=unit_price).pack()

            tk.Label(root, text="Quantity").pack()
            tk.Entry(root, textvariable=quantity).pack()

            tk.Label(root, text="Date (YYYY-MM-DD)").pack()
            tk.Entry(root, textvariable=date).pack()

            def save_edited_record():
                new_event = event.get()
                new_item_name = item_name.get()
                new_unit_price = unit_price.get()
                new_quantity = quantity.get()
                new_total_price = new_unit_price * new_quantity
                new_date = date.get()

                # Update the record in the database
                self.db.update_record(record_id, new_event, new_item_name, new_unit_price, new_quantity, new_total_price, new_date)
                messagebox.showinfo("Success", "Record updated successfully!")
                callback()

            tk.Button(root, text="Save Changes", bg='#4CAF50', fg='white', command=save_edited_record).pack(pady=10)
            tk.Button(root, text="Cancel", bg='#f44336', fg='white', command=callback).pack()

    def generate_pdf(self):
        records = self.db.fetch_all_records()
        if not records:
            messagebox.showwarning("No records", "There are no records to generate a PDF.")
            return

        pdf_filename = f"event_budget_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, "Event Budget Report")
        c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

        c.drawString(100, 700, "ID   Event          Item         Unit Price   Quantity   Total     Date")
        y_position = 680
        for record in records:
            c.drawString(100, y_position, f"{record[0]}   {record[1]}   {record[2]}   {record[3]:.2f}   {record[4]}   {record[5]:.2f}   {record[6]}")
            y_position -= 20

        c.save()
        messagebox.showinfo("Success", f"PDF generated: {pdf_filename}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Budget Management")
        self.root.geometry("600x600")
        self.root.configure(bg='#4CAF50')
        self.db_manager = DatabaseManager()
        self.record_manager = RecordManager(self.db_manager)
        self.show_main_menu()

    def show_main_menu(self):
        self.record_manager.clear_window(self.root)
        tk.Label(self.root, text="Event Budget Management", font=('Arial', 24), fg='white', bg='#4CAF50').pack(pady=20)
        tk.Button(self.root, text="Add Record", bg='#2196F3', fg='white', command=lambda: self.record_manager.add_record(self.root, self.show_main_menu)).pack(pady=10)
        tk.Button(self.root, text="View Records", bg='#FFC107', fg='white', command=lambda: self.record_manager.list_records(self.root, self.show_main_menu)).pack(pady=10)
        tk.Button(self.root, text="Exit", bg='#f44336', fg='white', command=self.root.quit).pack(pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()
    app.db_manager.close()
