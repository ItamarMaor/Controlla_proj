import socket
import threading
import os
from PIL import ImageGrab
import gzip
import pickle
from client_utils import WindowBlocker 
import tkinter as tk
from tkinter import messagebox

commands = {'get_client_username': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'announce': 5}

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = []
        self.blocker = WindowBlocker()
        # self.utills = ClientFunctions()

    def connect(self):
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connected to the server.")
        client_username = self.ask_for_username()
        self.client_socket.sendall(f"{commands['get_client_username']}{str(len(client_username)).zfill(8)}".encode('utf-8'))
        self.client_socket.sendall(client_username.encode('utf-8'))

    def receive_messages(self):
        cmmd = self.client_socket.recv(1).decode('utf-8')
        data_len = int(self.client_socket.recv(8).decode('utf-8'))
        data = self.client_socket.recv(data_len).decode('utf-8')
        self.handle_requests(cmmd, data)
    
    def handle_requests(self, cmmd, data):
        with threading.Lock():
            if cmmd == '0':
                # Command: get_client_username
                pass
            elif cmmd == '1':
                # Command: shutdown
                # self.client_socket.close()
                self.shutdown_computer()
            elif cmmd == '2':
                # Command: screenshot
                self.messages.append((2, self.screenshot()))
            elif cmmd == '3':
                # Command: block
                self.messages.append((3, 'blocked'))
                if not self.blocker.is_alive():
                    self.blocker.start()
            elif cmmd == '4':
                # Command: unblock
                self.blocker.unblock()
                self.messages.append((4, 'unblocked'))
                self.blocker = WindowBlocker()
            elif cmmd == '5':
                # Command: announce
                messagebox.showinfo("Announcement", data) 
    
    def shutdown_computer(self):
        self.client_socket.close()
        os.system("shutdown /s /t 15")
              
    def screenshot(self):
        pic = ImageGrab.grab()
        pic_bytes = pic.tobytes()
        compressed_pic = gzip.compress(pic_bytes)
        
        return pickle.dumps(compressed_pic)
            
    def run(self):
        try:
            self.connect()
            receive_thread = threading.Thread(target=self.send_recv_messages, daemon=True)
            receive_thread.start()
            receive_thread.join()

        except KeyboardInterrupt:
            print("Client shutting down.")
        finally:
            self.client_socket.close()

    def send_recv_messages(self):
        while True:
            self.receive_messages()
            
            #responsible for responses
            for cmmd, data in self.messages:
                print(type(cmmd))
                if cmmd == 2:
                    self.client_socket.sendall(f"{cmmd}{str(len(data)).zfill(8)}".encode('utf-8'))
                    self.client_socket.sendall(data)
                else:
                    self.client_socket.sendall(f"{cmmd}{str(len(data)).zfill(8)}".encode('utf-8'))
                    self.client_socket.sendall(data.encode('utf-8'))
                
                self.messages.remove((cmmd, data))
    
    def ask_for_username(self):
        def on_click():
            global uname
            uname = name_entry.get()
            root.destroy()
        
        root = tk.Tk()
        root.wm_attributes("-topmost", True)
        header = tk.Label(root, text='Enter client username')
        name_entry = tk.Entry(root)
        ok_button = tk.Button(root, text='OK', command=on_click)
        header.pack()
        name_entry.pack()
        ok_button.pack()
        
        root.mainloop()    
        
        return uname


if __name__ == "__main__":
    server_address = "127.0.0.1"  # Change this to the server's IP address
    server_port = 5000  # Change this to the server's port

    client = Client(server_address, server_port)
    client.run()