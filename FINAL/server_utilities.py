import sqlite3
import tkinter as tk
from tkinter import simpledialog


class Database:
    def __init__(self):
        self.database = 'Contralla_db.sqlite'

    def create_conn(self):
        '''creates connection to the database'''
        conn = sqlite3.connect(self.database)
        return (conn ,conn.cursor())
    
    # def generic_func_temp(self):
    #     conn, cursor = self.create_conn()
        
    #     code here
        
    #     conn.commit()
    #     conn.close()
        
    def create_user_table(self):
        conn, cursor = self.create_conn()
        # Create a table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def insert_user(self, username, password):
        self.create_user_table()
        conn, cursor = self.create_conn()
        # Insert data
        cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, password),)
        conn.commit()
        conn.close()
        
    def remove_user(self, username):
        self.create_user_table()
        conn, cursor = self.create_conn()
        # delete data
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.close()
    
    def check_user(self, username, password):
        self.create_user_table()
        conn, cursor = self.create_conn()
        # check if user exists
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user_exists = cursor.fetchone() is not None
        conn.close()
        
        return user_exists
    
    def create_student_table(self):
        conn, cursor = self.create_conn()
        # Create a table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                ip TEXT PRIMARY KEY,
                name TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def insert_student(self, ip, name):
        self.create_student_table()
        conn, cursor = self.create_conn()
        # Insert data
        cursor.execute('''
            INSERT INTO students (ip, name) VALUES (?, ?)
        ''', (ip, name),)
        conn.commit()
        conn.close()
        
    def remove_student(self, name):
        self.create_student_table()
        conn, cursor = self.create_conn()
        # delete data
        cursor.execute('DELETE FROM students WHERE name = ?', (name,))
        conn.close()
        
    def format_to_tktable(self, data):
        conn, cursor = self.create_conn()
        
        data_dict = {}
        
        # cursor.execute("SELECT ip, name FROM students")
        # rows = cursor.fetchall()
        # print(rows)
        
        # Populate the dictionary
        for idx, row in enumerate(data):
            rec_key = f'rec{idx+1}'
            data_dict[rec_key] = {'IP': row[0], 'Name': row[1], 'Shutdown': None, 'Screenshare': None, 'Block': None}
        
        # Close the connection
        conn.close()
        
        print(data_dict)
        return data_dict

class ServerFunctions():   
    def ask_for_username(self):
        def on_click():
            global uname
            uname = name_entry.get()
            root.destroy()
        
        root = tk.Tk()
        header = tk.Label(root, text='Enter client username')
        name_entry = tk.Entry(root)
        ok_button = tk.Button(root, text='OK', command=on_click)
        header.pack()
        name_entry.pack()
        ok_button.pack()
        
        root.mainloop()    
        
        return uname


        
if __name__ == '__main__':  
    a = Database()
    # # a.insert_student('1227.0.0.1', 'bb')
    print(a.format_to_tktable())

    
    # # Create a cursor
    # cursor = conn.cursor()

    # # Create a table
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS students (
    #         id INTEGER PRIMARY KEY,
    #         name TEXT,
    #         age INTEGER
    #     )
    # ''')

    # # Insert data
    # cursor.execute('''
    #     INSERT INTO students (name, age) VALUES (?, ?)
    # ''', ('Alice', 22),)
    # conn.commit()

    # # Query data
    # cursor.execute('SELECT * FROM students')
    # rows = cursor.fetchall()

    # for row in rows:
    #     print(row)

    # # Update and delete data
    # cursor.execute('UPDATE students SET age = ? WHERE name = ?', (23, 'Alice'))
    # cursor.execute('DELETE FROM students WHERE name = ?', ('Alice',))
    # conn.commit()

    # # Close the connection
    # conn.close()
