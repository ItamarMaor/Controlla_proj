import socket
import threading


def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            client_message = data.decode('utf-8')
            if not data or client_message == "exit":
                break
            print(f"Received data: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_exit(client_socket)


def client_exit(client_socket):
    client_socket.close()
    print("Client has disconnected")


class MultiThreadedServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_threads = []
        print(f"Server listening on {self.host}:{self.port}")

    def start_server(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_handler = threading.Thread(target=handle_client, args=(client_socket,))
                self.client_threads.append(client_handler)
                client_handler.start()
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = MultiThreadedServer(host='0.0.0.0', port=12345)
    server.start_server()
