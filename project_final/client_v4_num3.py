import socket
import threading

class ChatClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connected to the server.")

        # Get and send the username to the server
        username = input("Enter your username: ")
        self.client_socket.sendall(username.encode('utf-8'))

    def receive_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"{data.decode('utf-8')}")
        except Exception as e:
            print(f"Error receiving message: {e}")

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
    server_port = 12345  # Change this to the server's port

    client = ChatClient(server_address, server_port)
    client.run()
