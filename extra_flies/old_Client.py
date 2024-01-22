import socket
import select
# import subprocess
import os
#need to download pywin32 to client computer "pip install pywin32"
import win32gui
import win32con
from Controlla_proj.project_final.protocol import *


# MY_IP = '127.0.0.1'
# Create a socket for the client and connect to the server
client_socket = socket.socket()
client_socket.connect(SERVER_ADDRESS)
print("Connected to the server.")

COMMANDS = {
    "shutdown": '1',
    "screen on/off": '2',
    "teacher shares screen": '3',
    "student shares screen": '4',
    "private message": '5'
}
screen_on = True #by default screen is on
def shutdown_computer(client_socket):
    os.system("shutdown /s /t 15")
    client_socket.close()
            

# Main client loop
while True:
    # Use select to monitor sockets for readable/writable states
    rlist, wlist, xlist = select.select([client_socket], [client_socket], [])
    for sock in rlist:
        if sock == client_socket:
            # Receive the length of the incoming message
            received_len = sock.recv(4).decode()
            # Receive the actual message content
            received_data = sock.recv(int(received_len)).decode()
            function_request = get_function(received_data)
            if function_request == COMMANDS["shutdown"]:
                # If the received message is shutdown the client does so 
                shutdown_computer(client_socket)
                break
            elif function_request == COMMANDS["screen on/off"]:
                if screen_on is True:
                    #turning off screen
                    screen_on = False
                    win32gui.SendMessage(win32con.HWND_BROADCAST, \
                        win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)
                else:
                    #turning on the screen
                    screen_on = True
                    win32gui.SendMessage(win32con.HWND_BROADCAST,\
                        win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, -1)
                
    





# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         data = conn.recv(1024)  # Receive shutdown command (optional)

#         # Initiate shutdown process here (e.g., using os.system("shutdown /s") for Windows)
#         shutdown_command = ["shutdown", "/s", "/m", f"\\\\{HOST}"]
#         subprocess.run(shutdown_command)
# conn.sendall(b'Shutdown successful')


#         # Upon successful shutdown, send confirmation message
        
