import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from server_utilities import Database
from server_utilities import ServerFunctions
from threading import Thread
from threading import Lock
import select

class Server(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.database = Database()
        self.messages_lock = threading.Lock()
        self.client_threads = []
        self.username = ""
        self.utills = ServerFunctions()
        self.messages = []
        
        print(f"Server listening on {self.host}:{self.port}")


    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_username = self.utills.ask_for_username()
            print(f"\nAccepted connection from user: {client_username} - {client_address}")
            client_thread = ClientThread(client_address[0], client_address[1], client_socket, client_username)
            client_thread.start()
            self.client_threads.append(client_thread)
            
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
            
    def get_connected_clients(self):
        connected_list = []
        
        for client_thread in self.client_threads:
            connected_list.append((client_thread.ip, client_thread.username))
            
        return self.database.format_to_tktable(connected_list)
    
    def get_client_thread_by_ip(self, ip):
        for client_thread in self.client_threads:
            if client_thread.ip == ip:
                return client_thread
        return None

class ClientThread(Thread): 
    def __init__(self, ip, port, client_socket, username): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port
        self.client_socket = client_socket
        self.username = username
        self.messages = []
        self.lock = Lock()  # Create a threading lock
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self): 
        while True: 
            for cmmd, data in self.messages:
                self.client_socket.send(f"{cmmd}{str(len(data)).zfill(8)}{data}".encode('utf-8'))
                self.messages.remove(cmmd, data)
                
            # Check if the client socket is ready for receiving data
            rlist, _, _ = select.select([self.client_socket], [], [], 0)
            if self.client_socket in rlist:
                cmmd = self.client_socket.recv(1).decode('utf-8')
                data_len = int(self.client_socket.recv(8).decode('utf-8'))
                data = self.client_socket.recv(data_len).decode('utf-8')
                
                #TODO: Process the received data here
                print(f"Command: {cmmd}, Data: {data}")

    def append_message(self, cmmd, data=''):
        with self.lock:  # Acquire the lock before modifying the messages list
            self.messages.append((cmmd, data))

if __name__ == "__main__":
    server = Server(host='0.0.0.0', port=5000)
    server.start()