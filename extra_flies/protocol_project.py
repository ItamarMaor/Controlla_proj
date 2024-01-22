import socket

# local ip depends on computer ip
LOCAL_IP = socket.gethostname()
PORT = 5457  # initiate port no above 1024
# Server address and length field size constants
CLIENT_ADDRESS = (LOCAL_IP, PORT)


def main():
    client_socket = socket.socket()  # instantiate
    client_socket.connect(CLIENT_ADDRESS)  # connect to the server

    username = input("Enter username: ")
    client_socket.send("username".encode())
    client_socket.send(username.encode())
    client_socket.send(socket.gethostbyname(socket.gethostname()).encode())

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal
        if data == "Screen turned off successfully":
            print("Screen turned off successfully")

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    main()
