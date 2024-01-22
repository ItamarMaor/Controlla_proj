import socket
import threading
import select
import sys

class MultiThreadedServer:
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_threads = []
        self.clients = []
        self.should_send = True

        print(f"Server listening on {self.host}:{self.port}")

    def start_server(self):
        try:
            input_thread = threading.Thread(target=self.read_console_input)
            input_thread.start()

            while True:
                ready_to_read, _, _ = select.select([self.server_socket] + self.clients, [], [])

                for sock in ready_to_read:
                    if sock == self.server_socket:
                        client_socket, client_address = self.server_socket.accept()
                        print(f"\nAccepted connection from {client_address}")
                        self.clients.append(client_socket)
                        client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                        client_handler.start()
                        self.client_threads.append(client_handler)

        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_message = data.decode('utf-8')
                print(f"\nReceived data from {client_socket.getpeername()}: {client_message}")

                # Process the message as needed

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.client_exit(client_socket)

    def client_exit(self, client_socket):
        self.clients.remove(client_socket)
        client_socket.close()
        print("Client has disconnected")

    def broadcast(self, message):
        for client_socket in self.clients:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")

    def read_console_input(self):
        try:
            while True:
                message = input("Server (Type 'exit' to close the server): ")
                if message.lower() == "exit":
                    print("Server shutting down.")
                    break
                else:
                    self.broadcast(f"Server: {message}")

        except Exception as e:
            print(f"Error reading console input: {e}")

if __name__ == "__main__":
    server = MultiThreadedServer(host='0.0.0.0', port=12345)
    server.start_server()
