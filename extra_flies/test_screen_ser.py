import socket
import os

# local ip depends on computer ip
LOCAL_IP = socket.gethostname()
PORT = 5457  # initiate port no above 1024
# Server address and length field size constants
SERVER_ADDRESS = (LOCAL_IP, PORT)


def turn_off_screen():
    if os.name == 'nt':
        os.system(
            'powershell (Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::AllScreens | ForEach-Object {$_.Brightness = 0})')
    else:
        os.system('xset dpms force off')


def main():
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind(SERVER_ADDRESS)  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    usernames = {}
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        if data == "username":
            username = conn.recv(1024).decode()
            client_ip_address = conn.recv(1024).decode()
            usernames[username] = client_ip_address
            print(f"{username} connected with IP address {client_ip_address}")
        elif data == "username list":
            conn.send(str(usernames).encode())
        elif data == "turn-off":
            conn.send("who to turn off?".encode())
            username = conn.recv(1024).decode()
            if username in usernames:
                client_ip_address = usernames[username]
                client_socket = socket.socket()
                client_socket.connect((client_ip_address, PORT))
                client_socket.send("turn off screen".encode())
                data = client_socket.recv(1024).decode()
                if data == "Screen turned off":
                    conn.send("Screen turned off successfully".encode())
                client_socket.close()
            else:
                conn.send("Username not found".encode())

    conn.close()  # close the connection
    server_socket.close()


if __name__ == '__main__':
    main()
