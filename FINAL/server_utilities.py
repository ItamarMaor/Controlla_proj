import sqlite3

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
    
    def check_user(self, username):
        self.create_user_table()
        conn, cursor = self.create_conn()
        # check if user exists
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.close()
        
        
a = Database()
# # a.insert_user('aa', 'hhh')
# a.remove_user('aa')

    
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
