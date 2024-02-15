import sqlite3
import tkinter as tk
from tkinter import N, S, E, W, TOP, BOTTOM, LEFT, RIGHT, END
from tksheet import Sheet

class ComputerTableApp:
    def __init__(self, root, db_name, table_name):
        self.root = root
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create a sample table for demo purposes only.
        # In a full app, the database schema would be created elsewhere.
        self.create_table()

        # Create the sheet to display data
        self.sheet = Sheet(self.root, page_up_down_select_row=True)
        self.sheet.grid(row=0, column=0, sticky=N + S + E + W)

        # Add column headers
        self.sheet.headers(["Computer Name", "Button 1", "Button 2", "Button 3"])

        # Fetch data from the table and populate the sheet
        self.populate_sheet()

        # Add two buttons below the table
        self.add_buttons()

    def create_table(self):
        col_defs = ("ID INTEGER PRIMARY KEY", "computer_name TEXT", "button1 TEXT", "button2 TEXT", "button3 TEXT")
        stmnt = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({', '.join(col_defs)})"
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.cursor.execute(stmnt)
        self.conn.commit()

    def populate_sheet(self):
        # Sample data (replace with your own)
        data = [
            ("Computer A", "", "", ""),
            ("Computer B", "", "", ""),
            ("Computer C", "", "", ""),
        ]
        self.sheet.set_sheet_data(data)

    def add_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, sticky=E)

        button1 = tk.Button(button_frame, text="Action 1", command=self.button1_action)
        button1.pack(side=LEFT)

        button2 = tk.Button(button_frame, text="Action 2", command=self.button2_action)
        button2.pack(side=LEFT)

        button3 = tk.Button(button_frame, text="Action 3", command=self.button3_action)
        button3.pack(side=LEFT)

    def button1_action(self):
        print("Button 1 clicked")

    def button2_action(self):
        print("Button 2 clicked")

    def button3_action(self):
        print("Button 3 clicked")

if __name__ == "__main__":
    db_name = "my_database.db"  # Replace with your database name
    table_name = "computers"  # Replace with your table name

    root = tk.Tk()
    app = ComputerTableApp(root, db_name, table_name)
    root.mainloop()
