import sqlite3

# Database Manager Class
class DatabaseManager:
    def __init__(self, db_name="budget_records.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_tables()
        self.insert_sample_data()  # Insert sample data if necessary

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS budget_records (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            item_name TEXT NOT NULL,
                            amount REAL NOT NULL,
                            quantity INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            department TEXT NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS forecast_records (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            item_id INTEGER NOT NULL,
                            start_month TEXT NOT NULL,
                            end_month TEXT NOT NULL,
                            forecast_amount REAL NOT NULL,
                            FOREIGN KEY(item_id) REFERENCES budget_records(id))''')
        self.conn.commit()

    def insert_sample_data(self):
        # Check if there are records in the table
        self.c.execute("SELECT COUNT(*) FROM budget_records")
        count = self.c.fetchone()[0]
        
        if count == 0:
            # Insert 5 sample records
            sample_data = [
                ('Office Supplies', 150.00, 20, '2024-10-01', 'Finance'),
                ('Laptops', 1200.00, 5, '2024-09-20', 'IT'),
                ('Paper Reams', 300.00, 50, '2024-10-10', 'HR'),
                ('Projector', 450.00, 2, '2024-08-15', 'Sales'),
                ('Desks', 800.00, 10, '2024-07-30', 'Admin')
            ]
            self.c.executemany("INSERT INTO budget_records (item_name, amount, quantity, date, department) VALUES (?, ?, ?, ?, ?)", sample_data)
            self.conn.commit()

    def insert_record(self, item_name, amount, quantity, date, department):
        self.c.execute("INSERT INTO budget_records (item_name, amount, quantity, date, department) VALUES (?, ?, ?, ?, ?)",
                       (item_name, amount, quantity, date, department))
        self.conn.commit()

    def delete_record(self, record_id):
        self.c.execute("DELETE FROM budget_records WHERE id = ?", (record_id,))
        self.conn.commit()

    def fetch_all_records(self):
        return self.c.execute("SELECT * FROM budget_records").fetchall()

    def insert_forecast(self, item_id, start_month, end_month, forecast_amount):
        self.c.execute("INSERT INTO forecast_records (item_id, start_month, end_month, forecast_amount) VALUES (?, ?, ?, ?)",
                       (item_id, start_month, end_month, forecast_amount))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

