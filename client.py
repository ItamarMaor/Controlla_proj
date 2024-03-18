import socket
import threading
import os
from PIL import ImageGrab
import gzip
import pickle
from client_utils import *

commands = {'disconnect': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'vote': 5}

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = []
        self.blocker = WindowBlocker()

    def connect(self):
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connected to the server.")

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
        
    def receive_messages(self):
        cmmd = self.client_socket.recv(1).decode('utf-8')
        data_len = int(self.client_socket.recv(8).decode('utf-8'))
        data = self.client_socket.recv(data_len).decode('utf-8')
        self.handle_requests(cmmd, data)
    
    def handle_requests(self, cmmd, data):
        with threading.Lock():
            if cmmd == '0':
                # Command: disconnect
                pass
            elif cmmd == '1':
                # Command: shutdown
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



if __name__ == "__main__":
    server_address = "127.0.0.1"  # Change this to the server's IP address
    server_port = 5000  # Change this to the server's port

    client = Client(server_address, server_port)
    client.run()