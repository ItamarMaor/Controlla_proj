import sqlite3
import tkinter as tk
from tkinter import simpledialog
from PIL import Image
import gzip
from threading import Thread
import threading
import time
import select
from cryptography.fernet import Fernet
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class Database:
    def __init__(self):
        self.database = 'Contralla_db.sqlite'

    def create_conn(self):
        '''creates connection to the database'''
        conn = sqlite3.connect(self.database)
        return (conn ,conn.cursor())
        
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
        
    def check_username_exists(self, username):
        self.create_user_table()
        conn, cursor = self.create_conn()
        # check if username exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        username_exists = cursor.fetchone() is not None
        conn.close()
        
        return username_exists
    
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

class ServerFunctions():
    def show_screenshot(self, data):
        '''this function translates the photo from byte back to png and shows it'''
        decompressed_data = gzip.decompress(data)
        image = Image.frombytes("RGB", (1920, 1080), decompressed_data)
        image.show()

    def annoucment_input(self):
        def on_click():
            global announcment_msg
            announcment_msg = announcment_entry.get()
            root.destroy()
        
        root = tk.Tk()
        root.wm_attributes("-topmost", True)
        header = tk.Label(root, text='Enter your annoucment')
        announcment_entry = tk.Entry(root)
        ok_button = tk.Button(root, text='OK', command=on_click)
        header.pack()
        announcment_entry.pack()
        ok_button.pack()
        
        root.mainloop()    
        
        return announcment_msg
    
    def recv_uname(self, conn_client_socket, public_key):
        while True:
            # Check if the client socket is ready for receiving data
            rlist, _, _ = select.select([conn_client_socket], [], [], 60)
            if conn_client_socket in rlist:
                self.encryption = HybridEncryptionServer()
                len = conn_client_socket.recv(8).decode('utf-8')
                data = conn_client_socket.recv(int(len))
                _, client_username = self.encryption.decrypt(data, public_key)
                break
        return client_username.decode('utf-8') 
    
class HybridEncryptionServer():
    def __init__(self):
        # Initialize any necessary variables or objects here
        self.key = None
        self.CHUNK_SIZE = 2**32 - 33
    
    def generate_symetric_key(self):
        # Implement code to generate encryption key
        return Fernet.generate_key()
    
    def import_public_key(self, pem_key):
        return RSA.import_key(pem_key)
    
    def encrypt(self, plaintext, symetric_key):
        cipher = Fernet(symetric_key)
        ciphertext = b""
        
        while plaintext:
            chunk = plaintext[:self.CHUNK_SIZE]
            plaintext = plaintext[self.CHUNK_SIZE:]
            encrypted_chunk = cipher.encrypt(chunk)
            ciphertext += encrypted_chunk
    
        return ciphertext
    
    def decrypt(self, ciphertext, symetric_key):
        cipher = Fernet(symetric_key)
        plaintext = b""

        while ciphertext:
            chunk = ciphertext[:self.CHUNK_SIZE]  # Use the same chunk size as encryption
            ciphertext = ciphertext[self.CHUNK_SIZE:]
            decrypted_chunk = cipher.decrypt(chunk)
            plaintext += decrypted_chunk
    
        cmmd = plaintext[:1].decode()
        data = plaintext[1:]
        
        return cmmd, data
    
    def encrypt_asymmetric(self, plaintext, public_key):
        # Implement code to encrypt plaintext using asymmetric encryption
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext
    
    # # a.insert_student('1227.0.0.1', 'bb')


    
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
