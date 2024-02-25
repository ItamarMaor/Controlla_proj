import socket
from threading import Thread
from threading import Lock
import select

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
    def __init__(self, ip, port, client_socket): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port
        self.client_socket = client_socket
        self.messages = []
        self.lock = Lock()  # Create a threading lock
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self): 
        while True: 
            for cmmd, data in self.messages:
                self.client_socket.send(f"{cmmd}{str(len(data)).zfill(8)}{data}".encode('utf-8'))
                self.messages.remove(cmmd, data)
                
                # Check if the client socket is ready for receiving data
                rlist, _, _ = select.select([self.client_socket], [], [], 0)
                if self.client_socket in rlist:
                    cmmd = self.client_socket.recv(1).decode('utf-8')
                    data_len = int(self.client_socket.recv(8).decode('utf-8'))
                    data = self.client_socket.recv(data_len).decode('utf-8')
                    
                    #TODO: Process the received data here
                    print(f"Command: {cmmd}, Data: {data}")

    def append_message(self, cmmd, data=''):
        with self.lock:  # Acquire the lock before modifying the messages list
            self.messages.append((cmmd, data))
