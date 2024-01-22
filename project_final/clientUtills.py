import threading
import os


def computer_shutdown(client_socket):
    # If the received message is shutdown the client does so 
    os.system("shutdown /s /t 15")
    client_socket.close()