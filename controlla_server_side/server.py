import socket
import threading
import datetime
import select
import pickle
import logging
from controlla_server_side.server_utilities import Database
from controlla_server_side.server_utilities import ServerFunctions
from controlla_server_side.server_utilities import HybridEncryptionServer
from threading import Thread
from threading import Lock


commands = {'get_client_username': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'announce': 5}
cmmd_num_to_name = {v: k for k, v in commands.items()}
        
class Server(Thread):
    """
    Represents a server that listens for client connections and handles client threads.

    Attributes:
        host (str): The host address to bind the server socket to.
        port (int): The port number to bind the server socket to.
        server_socket (socket.socket): The server socket object.
        database (Database): The database object for storing client information.
        encryption (HybridEncryptionServer): The encryption object for secure communication.
        messages_lock (threading.Lock): The lock object for synchronizing access to the messages list.
        client_threads (list): The list of active client threads.
        username (str): The username of the server.
        utils (ServerFunctions): The utility functions for server operations.
        messages (list): The list of messages received from clients.
        refresh (bool): Flag indicating whether the server needs to refresh the client list.
        lesson_start_time (str): The start time of the lesson.
    """

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
        self.lesson_start_time = ""
        logging.basicConfig(filename='server.log', filemode='a', level=logging.INFO)
        
        print(f"Server listening on {self.host}:{self.port}")

    def run(self):
        """
        Starts the server and listens for client connections.
        Creates a new client thread for each connected client.
        """
        while True:
            client_socket, (ip, port) = self.server_socket.accept()
            client_thread = ClientThread(ip, port, client_socket, self.username)
            client_thread.start()
            self.client_threads.append(client_thread)
            self.refresh = True
            
    def close(self):
        """
        Closes all client sockets and the server socket.
        """
        for client_thread in self.client_threads:
            client_thread.client_socket.close()
        self.server_socket.close()
            
    def client_exit(self, client_socket, client_address):
        """
        Handles the disconnection of a client.

        Args:
            client_socket (socket.socket): The client socket object.
            client_address (tuple): The client address (IP, port).
        """
        del self.clients[client_address]
        client_socket.close()
        print(f"Client at {client_address} has disconnected")
        
    def broadcast(self, message):
        """
        Sends a message to all connected clients.

        Args:
            message (str): The message to broadcast.
        """
        for client_socket in self.clients.values():
            try:
                client_socket.sendall(f"Broadcast: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")

    def send_to_client(self, target_address, message):
        """
        Sends a message to a specific client.

        Args:
            target_address (tuple): The target client address (IP, port).
            message (str): The message to send.
        """
        try:
            target_socket = self.usernames.get(target_address)
            if target_socket:
                target_socket.sendall(message.encode('utf-8'))
            else:
                print(f"Target client {target_address} not found.")
        except Exception as e:
            print(f"Error sending message to client: {e}")
            
    def get_connected_clients(self):
        """
        Retrieves a list of connected clients.

        Returns:
            list: A list of tuples containing the client IP and username.
        """
        connected_list = []
        
        for client_thread in self.client_threads:
            while client_thread.username == None:
                pass
            connected_list.append((client_thread.ip, client_thread.username))
            
        return connected_list
    
    def get_clients_attendance(self):
        """
        Retrieves the attendance information of connected clients.

        Returns:
            list: A list of tuples containing the date, lesson start time, client counter,
                  client username, arrival time, and time late.
        """
        clients_attendance = []
        counter = 0
        for client_thread in self.client_threads:
            while client_thread.username == None:
                pass
            
            counter += 1
            date = datetime.datetime.strptime(self.lesson_start_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            lesson_start_time = datetime.datetime.strptime(self.lesson_start_time, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
            arrival_time = datetime.datetime.strptime(client_thread.arrival_time, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
            time_late = datetime.datetime.strptime(client_thread.arrival_time, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(self.lesson_start_time, "%Y-%m-%d %H:%M:%S")
            time_late = str(time_late)  # Convert timedelta object to string
            time_late = datetime.datetime.strptime(time_late, "%H:%M:%S").strftime("%H:%M:%S")
            
            clients_attendance.append((date, lesson_start_time, counter, client_thread.username, arrival_time, time_late))
            
        return clients_attendance
    
    def get_thread_by_ip_and_username(self, selection):
        """
        Retrieves the client thread object based on the IP and username selection.

        Args:
            selection (list): The IP and username selection.

        Returns:
            ClientThread: The client thread object.
        """
        for client_thread in self.client_threads:
            if [client_thread.ip, client_thread.username] == selection:
                return client_thread
            
    def get_log_for_teacher(self, teachername):
        """
        Retrieves the log entries for a specific teacher.

        Args:
            teachername (str): The name of the teacher.

        Returns:
            str: The filtered log entries for the teacher.
        """
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
    def __init__(self, ip, port, client_socket, teacher): 
        """
        Initializes a new instance of the Server class.

        Parameters:
        - ip (str): The IP address of the client.
        - port (int): The port number of the clirnt.
        - client_socket (socket): The client socket object.
        - teacher (str): The name of the teacher.

        Attributes:
        - utils (ServerFunctions): An instance of the ServerFunctions class.
        - ip (str): The IP address of the client.
        - port (int): The port number of the client.
        - client_socket (socket): The client socket object.
        - encryption (HybridEncryptionServer): An instance of the HybridEncryptionServer class.
        - symetric_key (str): The generated symmetric key.
        - arrival_time (str): The arrival time of the client connection.
        - username (str): The username of the client.
        - teacher (str): The name of the teacher.
        - messages (list): A list to store messages that will be sent to the client.
        - is_blocked (bool): A flag indicating if the client is blocked.
        - lock (Lock): A threading lock object.

        Returns:
        None
        """
        Thread.__init__(self) 
        self.utils = ServerFunctions()
        self.ip = ip 
        self.port = port
        self.client_socket = client_socket
        self.encryption = HybridEncryptionServer()
        self.symetric_key = self.encryption.generate_symetric_key()
        self.arrival_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.username = None
        self.teacher = teacher
        self.messages = []
        self.is_blocked = False
        self.lock = Lock()  
        
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self): 
        """
        Runs the class and handles the communication with the client.

        This method performs the following steps:
        1. Imports the public key from the client.
        2. Sends the symmetric key encrypted with the client's public key.
        3. Receives the username from the client.
        4. Prints the accepted connection information.
        5. Continuously sends and receives messages with the client.

        """
        self.encryption.key = self.encryption.import_public_key(self.client_socket.recv(1024))
        self.client_socket.sendall(self.encryption.encrypt_asymmetric(self.symetric_key, self.encryption.key))
        
        self.username = self.utils.recv_uname(self.client_socket, self.symetric_key)
        print(f"\nAccepted connection from user: {self.username} - {self.ip, self.port}")
        
        while True: 
            self.send_messages()
            self.recv_messages()

    def send_messages(self):
        """
        Sends messages to the client.

        This method iterates through the messages stored in the `self.messages` list and sends them to the client.
        Each message consists of a command (`cmmd`) and data associated with the command.
        The method logs the details of each message before sending it.

        Returns:
            None
        """
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
   
    def recv_messages(self):
        """
        Receive messages from the client socket.

        This method checks if the client socket is ready for receiving data. If data is available,
        it receives the encrypted message from the client socket, decrypts it using the symmetric key,
        and then handles the response.

        Note: This method assumes that the `encryption` and `symetric_key` attributes have been properly set.

        Returns:
            None
        """
        # Check if the client socket is ready for receiving data
        rlist, _, _ = select.select([self.client_socket], [], [], 0)
        if self.client_socket in rlist:
            recv_len = int(self.client_socket.recv(8).decode())
            ciphertext = self.client_socket.recv(recv_len)
            
            cmmd, data = self.encryption.decrypt(ciphertext, self.symetric_key)

            self.handle_response(cmmd, data)
            
    def format_message(self, cmmd, data):
        """
        Formats the message by encoding the command and data, and encrypts it using the symmetric key.

        Args:
            cmmd (str): The command to be included in the message.
            data (str): The data to be included in the message.

        Returns:
            bytes: The encrypted message.

        """
        msg = f"{cmmd}{data}".encode()
        return self.encryption.encrypt(msg, self.symetric_key)
            
    def handle_response(self, cmmd, data):
        """
        Handles the response received from the client.

        Parameters:
        - cmmd (int): The command code received from the client.
        - data (bytes): The data received from the client.

        Returns:
        None
        """
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
        """
        Toggles the block state of the client on the server side.

        This method is used to toggle the block state of the server. If the server is currently blocked,
        it will be unblocked, and vice versa.
        """
        with self.lock:
            self.is_blocked = not self.is_blocked
    
    def get_block_state(self):
            """
            Returns the current state of the block.

            Returns:
                bool: True if the block is currently active, False otherwise.
            """
            with self.lock:
                return self.is_blocked
           
    def append_message(self, cmmd, data=''):
        """
        Appends a message to the messages list.

        Parameters:
        - cmmd (str): The command to be appended.
        - data (str): The data associated with the command (default: '').

        """
        with self.lock:  # Acquire the lock before modifying the messages list
            self.messages.append((cmmd, data))

if __name__ == "__main__":
    server = Server(host='0.0.0.0', port=5000)
    server.start()