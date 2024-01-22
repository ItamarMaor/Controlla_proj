import socket
from PIL import Image

HOST = '172.20.10.4'  # The server's hostname or IP address
PORT = 5555        # The port used by the server

def show_screenshot(data):
    image = Image.frombytes("RGB", (1920, 1080), data)
    image.show()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    message = input("Enter message to send (or 'quit' to exit): ")
    if message == 'quit':
        client_socket.send(b'100000004quit')
        client_socket.close()
        break

    client_socket.send(f'{message}{str(len(message)).zfill(8)}{message}'.encode())
    length = int(client_socket.recv(8).decode())
    data = client_socket.recv(length)

    if message == '2':
        show_screenshot(data)
    else:
        print("Received from server:", data.decode())
