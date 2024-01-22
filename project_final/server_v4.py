import socket
import threading

class MultiThreadedServer():
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = {}  # Dictionary to store connected clients
        self.client_threads = []
        
        print(f"Server listening on {self.host}:{self.port}")

    def start_server(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                
                # Store client socket in the dictionary
                self.clients[client_address] = client_socket
                
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_handler.start()
                self.client_threads.append(client_handler)
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()
            
    def handle_client(self, client_socket, client_address):
        try:
            
            while True:
                # Choose who to send the message
                target_address = eval(input("Choose target client (Type 'all' for all clients): "))
                
                # Input the message
                message = input("Enter a message (Type 'exit' to disconnect client): ")

                # Check if the message is a command to exit
                if message.lower() == "exit":
                    break

                # Check if the message is a command to send to a specific client or all clients
                else:
                    self.send_to_client(target_address, message)

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            self.client_exit(client_socket, client_address)

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
            if target_address == 'all':
                self.broadcast(message)
            else:
                target_socket = self.clients.get(target_address)
                if target_socket:
                    target_socket.sendall(f"Private Message: {message}".encode('utf-8'))
                else:
                    print(f"Target client {target_address} not found.")
        except Exception as e:
            print(f"Error sending message to client: {e}")

if __name__ == "__main__":
    server = MultiThreadedServer(host='0.0.0.0', port=12345)
    server.start_server()
