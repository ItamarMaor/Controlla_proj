import socket
import threading
from server_utilities import Database
from server_utilities import ServerFunctions
from server_utilities import HybridEncryptionServer
from threading import Thread
from threading import Lock
import datetime
import select
import pickle
import logging

commands = {'get_client_username': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'announce': 5}
cmmd_num_to_name = {v: k for k, v in commands.items()}
        
class Server(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.database = Database()
        self.encryption = HybridEncryptionServer()
        self.messages_lock = threading.Lock()
        self.client_threads = []
        self.username = ""
        self.utils = ServerFunctions()
        self.messages = []
        self.refresh = False
        logging.basicConfig(filename='server.log', filemode='a', level=logging.INFO)
        
        print(f"Server listening on {self.host}:{self.port}")

    def run(self):
        while True:
            client_socket, (ip, port) = self.server_socket.accept()
            client_username = self.utils.recv_uname(client_socket)
            print(f"\nAccepted connection from user: {client_username} - {ip, port}")
            client_thread = ClientThread(ip, port, client_socket, client_username, self.username)
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
    
    def get_thread_by_ip_and_username(self, selection):
        for client_thread in self.client_threads:
            if [client_thread.ip, client_thread.username] == selection:
                return client_thread
            
    def get_log_for_teacher(self, teachername):
        filtered_string = ''
        with open('server.log', 'r') as f:
            logs = f.readlines()
            for line in logs:
                if teachername in line:
                    filtered_string += line
                    
            if filtered_string != '':
                return filtered_string
            return 'No logs found for this teacher'

class ClientThread(Thread): 
    def __init__(self, ip, port, client_socket, username, teacher): 
        Thread.__init__(self) 
        self.utils = ServerFunctions()
        self.ip = ip 
        self.port = port
        self.client_socket = client_socket
        self.encryption = HybridEncryptionServer()
        self.symetric_key = self.encryption.generate_symetric_key() #new
        self.username = username
        self.teacher = teacher
        self.messages = []
        self.is_blocked = False
        self.lock = Lock()  # Create a threading lock
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self): 
        self.encryption.key = self.encryption.import_public_key(self.client_socket.recv(1024))
        self.client_socket.sendall(self.encryption.encrypt_asymmetric(self.symetric_key, self.encryption.key))
        
        while True: 
            self.send_messages()
            self.recv_messages()

    def send_messages(self):
        for cmmd, data in self.messages:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if cmmd == commands['announce']:
                logging.info(f"{timestamp} - Teacher: {self.teacher} - Target: {self.username} {self.ip} - Command: {cmmd_num_to_name[cmmd]} - Data: {data}")
            else:
                logging.info(f"{timestamp} - Teacher: {self.teacher} - Target: {self.username} {self.ip} - Command: {cmmd_num_to_name[cmmd]}")
            ciphertext = self.format_message(cmmd, data)
            self.client_socket.send(str(len(ciphertext)).zfill(8).encode())
            self.client_socket.sendall(ciphertext)
            self.messages.remove((cmmd, data))
            # if cmmd == 1:
            #     self.client_threads.remove(self)
            #     break
    
    def recv_messages(self):
        # Check if the client socket is ready for receiving data
        rlist, _, _ = select.select([self.client_socket], [], [], 0)
        if self.client_socket in rlist:
            recv_len = int(self.client_socket.recv(8).decode())
            ciphertext = self.client_socket.recv(recv_len)
            
            cmmd, data = self.encryption.decrypt(ciphertext, self.symetric_key)

            self.handle_response(cmmd, data)
            
    def format_message(self, cmmd, data):
        msg = f"{cmmd}{data}".encode()
        
        return self.encryption.encrypt(msg, self.symetric_key)
            
    def handle_response(self, cmmd, data):
        cmmd = int(cmmd)
        if cmmd == 1:
            # Command: shutdown
            pass
        elif cmmd == 2:
            # Command: screenshot
            try:
                data = pickle.loads(data)
                self.utils.show_screenshot(data)
            except:
                self.append_message(2)      
        elif cmmd in (3,4):
            # Command: block/unblock
            pass
        elif cmmd == 5:
            # Command: announce
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