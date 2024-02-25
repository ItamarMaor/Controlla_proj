import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from server_utilities import Database
from server_utilities import ServerFunctions

class MultiThreadedServer():
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.database = Database()
        self.messages_lock = threading.Lock()
        self.clients = {}  # Dictionary to store connected clients
        self.usernames = {} # Dictionary to store usernames to client address and socket
        self.client_threads = []
        self.username = ""
        self.utills = ServerFunctions
        self.messages = []
        
        print(f"Server listening on {self.host}:{self.port}")


    def start_server(self):
        # Start the handle_client method in a separate thread
        message_handler_thread = threading.Thread(target=self.handle_client)
        message_handler_thread.daemon = True  # Daemonize the thread to allow program exit
        message_handler_thread.start()

        while True:
            client_socket, client_address = self.server_socket.accept()
            self.username = self.utills.client_username(self)
            print(f"\nAccepted connection from user: {self.username} - {client_address}")
            self.clients[client_address] = client_socket
            self.usernames[self.username] = client_socket


    def handle_client(self):
        while True:
            # print("Checking messages...")
            # with self.messages_lock:
                if self.messages:
                    print("Messages found, processing...")
                    for message in self.messages[:]:
                        cmmd, dst_addr, data = message
                        print(f"Command: {cmmd}, Destination Address: {dst_addr}, Data: {data}")

                        # Remove the tuple from the original list
                        self.messages.remove(message)
                # else:
                    # print("No messages to process.")


    def client_exit(self, client_socket, client_address):
        del self.clients[client_address]
        client_socket.close()
        print(f"Client at {client_address} has disconnected")

    def broadcast(self, message):
        for client_socket in self.clients.values():
            try:
                client_socket.sendall(f"Broadcast: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")

    def send_to_client(self, target_address, message):
        try:
            target_socket = self.usernames.get(target_address)
            if target_socket:
                target_socket.sendall(message.encode('utf-8'))
            else:
                print(f"Target client {target_address} not found.")
        except Exception as e:
            print(f"Error sending message to client: {e}")
            
    def request_data(self, cmmd, dst_addr, data=''):
        '''Allows GUI to add messages to be sent. Uses threading lock to safely insert into the messages list.'''
        with self.messages_lock:
            message = (cmmd, dst_addr, data)  # Keep the tuple
            self.messages.append(message)
            text = ' '.join(map(str, message))  # Convert the tuple to string for printing
            print("what up my man", text)



if __name__ == "__main__":
    server = MultiThreadedServer(host='0.0.0.0', port=5000)
    server.start_server()