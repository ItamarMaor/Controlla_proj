import socket
import threading
from server_utilities import Database

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
        self.usernames = {} #Dictionary to store usernames to client address and socket
        self.client_threads = []
        self.username = ""
        
        print(f"Server listening on {self.host}:{self.port}")

    def start_server(self):
            while True:
                client_socket, client_address = self.server_socket.accept()
                data = client_socket.recv(1024)
                if data:
                    self.username = data.decode('utf-8')
                print(f"\nAccepted connection from user: {self.username} - {client_address}")
                # Store client socket in the dictionary
                self.clients[client_address] = client_socket
                self.usernames[self.username] = (client_socket)
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_handler.start()
                self.client_threads.append(client_handler)

            self.server_socket.close()
            
    def handle_client(self, client_socket, client_address):
            while True:
                self.timeout_between_threads
                with threading.Lock():
                    # Choose who to send the message
                    target_address = input("""Choose target client"
                                           Type 'all' for all clients
                                           type the client's name for a specific client
                                           type 'exit' to end """)
                    # target_address = "all"
                    
                    # Check if the message is a command to exit
                    if target_address.lower() == "exit":
                        break
                    if target_address == 'all':
                        message = input("""Enter a message to send to all: 
                                        Type 'shutdown' to shutdown a client
                                        Type 'disable wifi' to shutdown a client
                                        Type 'enable wifi' to shutdown a client""")
                        self.broadcast(message)
                    # Input the message
                    else:
                        message = input("""Enter a message:
                                        Type 'shutdown' to shutdown a client
                                        Type 'disable wifi' to shutdown a client
                                        Type 'enable wifi' to shutdown a client""")

                        # send the messages for the specific client
                        self.send_to_client(target_address, message)
                
            self.client_exit(client_socket, client_address)

    def timeout_between_threads(self):
        event = threading.Event()
        i_time_value = 2  # Set the timeout value in seconds
        t = threading.Timer(i_time_value, event.set(), [event])
        t.start()
        
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
                target_socket.sendall(f"Private Message: {message}".encode('utf-8'))
            else:
                print(f"Target client {target_address} not found.")
        except Exception as e:
            print(f"Error sending message to client: {e}")
            
    def request_data(self, cmmd, data=''):
        '''allows to gui to add messages to be sent, uses the threading lock in order to stop the thread to be able to insert to the messages list'''
        with self.messages_lock:
            self.messages.append((cmmd, data))


if __name__ == "__main__":
    server = MultiThreadedServer(host='0.0.0.0', port=5000)
    server.start_server()
