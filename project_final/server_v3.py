import socket
import threading
import select

class MultiThreadedServer:
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_threads = []
        self.clients = {}
        self.client_number = 0

        print(f"Server listening on {self.host}:{self.port}")

    def start_server(self):
        try:
            input_thread = threading.Thread(target=self.read_console_input)
            input_thread.start()

            while True:
                # ready_to_read, _, _ = select.select([self.server_socket] + list(self.clients.keys()), [], [])
                ready_to_read, _, _ = select.select([self.server_socket] + self.clients, [], [])

                for sock in ready_to_read:
                    if sock == self.server_socket:
                        client_socket, client_address = self.server_socket.accept()
                        print(f"\nAccepted connection from {client_address}")
                        self.clients[(client_socket, client_address)] = f"Client{self.client_number}"
                        self.client_number += 1

                        client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                        client_handler.start()
                        self.client_threads.append(client_handler)

                    else:
                        data = sock.recv(1024)
                        if not data:
                            self.client_exit(sock)

                        else:
                            client_message = data.decode('utf-8')
                            print(f"\n{self.clients[sock]}: {client_message}")

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
                print(f"\n{self.clients[client_socket]}: {client_message}")

                # Process the message as needed

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.client_exit(client_socket)

    def client_exit(self, client_socket):
        client_address = client_socket.getpeername()
        print(f"Client {self.clients[client_socket]} at {client_address} has disconnected")
        del self.clients[client_socket]
        client_socket.close()

    def broadcast(self, message):
        for client_socket in self.clients.keys():
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")

    def read_console_input(self):
        try:
            while True:
                print("\nServer options:")
                print("1. Send to everyone")
                print("2. Send to a specific client")
                print("3. Exit")
                choice = input("Enter your choice (1/2/3): ")

                if choice == "1":
                    message = input("Enter the message to broadcast: ")
                    self.broadcast(f"Server: {message}")

                elif choice == "2":
                    print("Client list:")
                    for idx, client_address in enumerate(self.clients.values()):
                        print(f"{idx + 1}. {client_address}")

                    while True:
                        try:
                            client_number = int(input("Enter the client number to send the message to: "))
                            if 1 <= client_number <= len(self.clients):
                                target_socket = list(self.clients.keys())[client_number - 1]
                                break
                            else:
                                print("Invalid client number. Please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")

                    message = input("Enter the message to send to the client: ")
                    target_socket.sendall(f"Server: {message}".encode('utf-8'))

                elif choice == "3":
                    print("Server shutting down.")
                    break

                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")

        except Exception as e:
            print(f"Error reading console input: {e}")

if __name__ == "__main__":
    server = MultiThreadedServer(host='0.0.0.0', port=12345)
    server.start_server()
