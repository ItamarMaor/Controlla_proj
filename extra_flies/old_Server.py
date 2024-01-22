import socket
import threading
import select
from datetime import datetime
from Controlla_proj.project_final.protocol import *



print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen()
print("Listening for clients...")

client_sockets = []  # List to store connected client sockets
uname_to_socket_dict = {} #dictionary to translate ip to its client name
clients = {}

while True:
    currentTime = datetime.now().strftime("%H:%M")
    # Use select to monitor sockets for readable/writable states
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            # New client connection request
            connection, client_address = current_socket.accept()
            # Add client socket to the list of all clients
            client_sockets.append(connection)
            client_uname = f"computer{len(client_sockets)}"
            # Map username to the socket
            uname_to_socket_dict[client_uname] = connection
            print("New client joined!", client_uname)

            # Add client socket to the list of current sockets being dealt with
            # curr_sock_list.append(connection)


            # Inform all clients about the new user joining
            messages_to_send.append((f'{currentTime} {client_uname} has joined the chat!', client_sockets.copy()))

# לכתוב פעולה שהיא ת'רד הנדל קליינט 
#מזמן את הפעולה כת'רד
#שייר סקרין בתור ת'רד