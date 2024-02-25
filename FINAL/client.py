import socket
import threading
import os
from PIL import ImageGrab
import gzip
import pickle

commands = {'disconnect': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'vote': 5}


class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = []

    def connect(self):
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connected to the server.")

        # # Get and send the username to the server
        # username = self.client_username()
        # self.client_socket.sendall(username.encode('utf-8'))

    def send_recv_messages(self):
        self.receive_messages()
        
        #responsible for responses
        for cmmd, data in self.messages:
            self.client_socket.sendall(f"{cmmd}{str(len(data)).zfill(8)}{data}".encode('utf-8'))
            self.messages.remove((cmmd, data))
        
    def receive_messages(self):
        while True:
            cmmd = self.client_socket.recv(1).decode('utf-8')
            data_len = int(self.client_socket.recv(8).decode('utf-8'))
            data = self.client_socket.recv(data_len).decode('utf-8')

            self.handle_requests(cmmd, data)
    
    def handle_requests(self, cmmd, data):
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
        elif cmmd == '4':
            # Command: unblock
            self.messages.append((4, 'unblocked'))
    
    def shutdown_computer(self):
        self.client_socket.close()
        os.system("shutdown /s /t 15")
        
    # def disable_internet_connection():
    #     """
    #     Disable the internet connection for a specified network interface.
    #     Note: Replace "MaorMain_5" with your actual network interface name.
    #     """
    #     interface_name = "MaorMain_5"
    #     if platform.system().lower() == 'windows':
    #         subprocess.run(["netsh", "interface", "set", "interface", interface_name, "admin=disable"], check=True)
    #         print(f"Internet connection for {interface_name} disabled.")
    #     else:
    #         print("Unsupported operating system. This function is designed for Windows.")

    # def enable_internet_connection():
    #     """
    #     Enable the internet connection for a specified network interface.
    #     Note: Replace "Wi-Fi" with your actual network interface name.
    #     """
    #     interface_name = "MaorMain_5"
    #     if platform.system().lower() == 'windows':
    #         subprocess.run(["netsh", "interface", "set", "interface", interface_name, "admin=enable"], check=True)
    #         print(f"Internet connection for {interface_name} enabled.")
    #     else:
    #         print("Unsupported operating system. This function is designed for Windows.")
            
    def screenshot(self):
        pic = ImageGrab.grab()
        pic_bytes = pic.tobytes()
        compressed_pic = gzip.compress(pic_bytes)
        return pickle.dumps(compressed_pic)
            
    def run(self):
        try:
            self.connect()
            receive_thread = threading.Thread(target=self.receive_messages)
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
