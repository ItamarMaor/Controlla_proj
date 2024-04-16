import sqlite3
import tkinter as tk
from PIL import Image
import gzip
import select
from cryptography.fernet import Fernet
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
import pandas as pd

import sqlite3

class Database:
    def __init__(self):
        self.database = 'Contralla_db.sqlite'

    def create_conn(self):
        '''Creates a connection to the database.

        Returns:
            tuple: A tuple containing the connection and cursor objects.
        '''
        conn = sqlite3.connect(self.database)
        return (conn, conn.cursor())
        
    def create_user_table(self):
        '''Creates the users table if it doesn't exist.'''
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
        '''Inserts a new user into the users table.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        '''
        self.create_user_table()
        conn, cursor = self.create_conn()
        # Insert data
        cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, password),)
        conn.commit()
        conn.close()
        
    def remove_user(self, username):
        '''Removes a user from the users table.

        Args:
            username (str): The username of the user to be removed.
        '''
        self.create_user_table()
        conn, cursor = self.create_conn()
        # delete data
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.close()
        
    def check_username_exists(self, username):
        '''Checks if a username exists in the users table.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        '''
        self.create_user_table()
        conn, cursor = self.create_conn()
        # check if username exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        username_exists = cursor.fetchone() is not None
        conn.close()
        
        return username_exists
    
    def check_user(self, username, password):
        '''Checks if a user exists in the users table.

        Args:
            username (str): The username to check.
            password (str): The password to check.

        Returns:
            bool: True if the user exists, False otherwise.
        '''
        self.create_user_table()
        conn, cursor = self.create_conn()
        # check if user exists
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user_exists = cursor.fetchone() is not None
        conn.close()
        
        return user_exists
    
    def create_student_table(self):
        '''Creates the students table if it doesn't exist.'''
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
        '''Inserts a new student into the students table.

        Args:
            ip (str): The IP address of the student.
            name (str): The name of the student.
        '''
        self.create_student_table()
        conn, cursor = self.create_conn()
        # Insert data
        cursor.execute('''
            INSERT INTO students (ip, name) VALUES (?, ?)
        ''', (ip, name),)
        conn.commit()
        conn.close()
        
    def remove_student(self, name):
        '''Removes a student from the students table.

        Args:
            name (str): The name of the student to be removed.
        '''
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
    
    def attendance_report(self, students):
        df = pd.DataFrame(students, columns=["Name", "Arrival Time"])
        filename = 'students_attendance.xlsx'
        df.to_excel(filename, index=False)
        os.startfile(filename)
    
class HybridEncryptionServer():
    """
    A class that provides hybrid encryption functionality for a server.

    Attributes:
        key: The encryption key used for symmetric encryption.
        CHUNK_SIZE: The size of each chunk used for encryption and decryption.
    """

    def __init__(self):
        self.key = None
        self.CHUNK_SIZE = 2**32 - 33
    
    def generate_symetric_key(self):
        """
        Generates a symmetric encryption key.

        Returns:
            The generated symmetric encryption key.
        """
        return Fernet.generate_key()
    
    def import_public_key(self, pem_key):
        """
        Imports a public key for asymmetric encryption.

        Args:
            pem_key: The PEM-encoded public key.

        Returns:
            The imported public key.
        """
        return RSA.import_key(pem_key)
    
    def encrypt(self, plaintext, symetric_key):
        """
        Encrypts plaintext using symmetric encryption.

        Args:
            plaintext: The plaintext to be encrypted.
            symetric_key: The symmetric encryption key.

        Returns:
            The encrypted ciphertext.
        """
        cipher = Fernet(symetric_key)
        ciphertext = b""
        
        while plaintext:
            chunk = plaintext[:self.CHUNK_SIZE]
            plaintext = plaintext[self.CHUNK_SIZE:]
            encrypted_chunk = cipher.encrypt(chunk)
            ciphertext += encrypted_chunk
    
        return ciphertext
    
    def decrypt(self, ciphertext, symetric_key):
        """
        Decrypts ciphertext using symmetric encryption.

        Args:
            ciphertext: The ciphertext to be decrypted.
            symetric_key: The symmetric encryption key.

        Returns:
            The decrypted plaintext.
        """
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
        """
        Encrypts plaintext using asymmetric encryption.

        Args:
            plaintext: The plaintext to be encrypted.
            public_key: The public key for asymmetric encryption.

        Returns:
            The encrypted ciphertext.
        """
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext
    