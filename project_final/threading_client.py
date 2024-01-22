import socket
import threading
from clientUtills import *



class MultiThreadedClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.COMMANDS = {
        "shutdown": '1',
        "screen on/off": '2',
        "student shares screen": '3',
        "teacher shares screen": '4',
        "private message": '5'
        }

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def send_data(self, data):
        self.client_socket.send(data.encode('utf-8'))

    def receive_data(self):
        while True:
            data = self.client_socket.recv(1024)
            server_message = data.decode('utf-8')
            if server_message == "shutdown":
                computer_shutdown(self)
            if not data:
                    break
            # if server_message == self.COMMANDS[1]:
            #     #add a new function to shutdown client's computer. 
            
            print(f"Received data: {server_message}")

    def start_client(self):
        # Connect to the server
        self.connect()

        # Start a thread for receiving data from the server
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

        try:
            # Send data to the server (replace this with your logic)
            while True:
                message = input("Enter a message (type 'exit' to quit): ")
                self.send_data(message)
                if message.lower() == 'exit':
                    receive_thread.join()
                    break

        except KeyboardInterrupt:
            print("Client shutting down.")
        finally:
            self.client_socket.close()


if __name__ == "__main__":
    client = MultiThreadedClient(host='127.0.0.1', port=12345)
    client.start_client()