import socket
import threading
from server_utilities import Database
from server_utilities import ServerFunctions
from threading import Thread
from threading import Lock
import select
import pickle

commands = {'disconnect': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'vote': 5}

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
        self.refresh = False
        
        print(f"Server listening on {self.host}:{self.port}")


    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_username = self.utills.ask_for_username()
            print(f"\nAccepted connection from user: {client_username} - {client_address}")
            client_thread = ClientThread(client_address[0], client_address[1], client_socket, client_username)
            client_thread.start()
            self.client_threads.append(client_thread)
            self.refresh = True
            
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
            
        return connected_list
    
    def get_client_thread_by_listbox_selection(self, selection):
        for client_thread in self.client_threads:
            if [client_thread.ip, client_thread.username] == selection:
                return client_thread

class ClientThread(Thread): 
    def __init__(self, ip, port, client_socket, username): 
        Thread.__init__(self) 
        self.utills = ServerFunctions()
        self.ip = ip 
        self.port = port
        self.client_socket = client_socket
        self.username = username
        self.messages = []
        self.is_blocked = False
        self.lock = Lock()  # Create a threading lock
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self): 
        while True: 
            self.send_messages()
            self.recv_messages()

    def send_messages(self):
        for cmmd, data in self.messages:
            self.client_socket.send(f"{cmmd}{str(len(data)).zfill(8)}{data}".encode('utf-8'))
            self.messages.remove((cmmd, data))
    
    def recv_messages(self):
        # Check if the client socket is ready for receiving data
        rlist, _, _ = select.select([self.client_socket], [], [], 0)
        if self.client_socket in rlist:
            cmmd = self.client_socket.recv(1).decode('utf-8')
            data_len = int(self.client_socket.recv(8).decode('utf-8'))
            data = self.client_socket.recv(data_len)

            self.handle_response(cmmd, data)
            
    def handle_response(self, cmmd, data):
        cmmd = int(cmmd)
        if cmmd == 1:
            # Command: shutdown
            pass
        elif cmmd == 2:
            # Command: screenshot
            data = pickle.loads(data)
            self.utills.show_screenshot(data)
        elif cmmd in (3,4):
            # Command: block/unblock
            pass
        elif cmmd == 5:
            # Command: vote
            pass
        else:
            data = data.decode('utf-8')
            print(f"Received command: {cmmd} with data: {data}")
            
    def toggle_block_state(self):  
        with self.lock:
            self.is_blocked = not self.is_blocked
    
    def get_block_state(self):
        with self.lock:
            return self.is_blocked
           
    def append_message(self, cmmd, data=''):
        with self.lock:  # Acquire the lock before modifying the messages list
            self.messages.append((cmmd, data))
            print(f"Appended message: {cmmd} with data: {data}")

if __name__ == "__main__":
    server = Server(host='0.0.0.0', port=5000)
    server.start()