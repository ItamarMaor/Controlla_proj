import socket
import threading
import os
import subprocess
import platform

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connected to the server.")

        # Get and send the username to the server
        username = input("Enter your username: ")
        self.client_socket.sendall(username.encode('utf-8'))

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            print ("data" + data.decode)    
            msg = self.decoding_data_to_msg(data)
            print(f"{msg}")

            if msg == "shutdown":
                # If the received message is shutdown the client does so 
                self.shutdown_computer(self.client_socket)
                break 
            # if msg == "disable wifi":
            #     disable_internet_connection()
            # if msg == "enable wifi":
            #     enable_internet_connection()
                
                
                       
                        
    def decoding_data_to_msg(data):
            decoded_data = data.decode('utf-8')
            msg_list = decoded_data.split(":")
            msg = msg_list[1].strip()
            # print ("post_colon_msg=" + post_colon_msg)
            # final_message_list = post_colon_msg.split(" ")
            # final_message = final_message_list[1].strip()
            # print ("final_message" + final_message)
            return msg
    
    
    def shutdown_computer(self,client_socket):
        os.system("shutdown /s /t 15")
        client_socket.close()
        
    def disable_internet_connection():
        """
        Disable the internet connection for a specified network interface.
        Note: Replace "MaorMain_5" with your actual network interface name.
        """
        interface_name = "MaorMain_5"
        if platform.system().lower() == 'windows':
            subprocess.run(["netsh", "interface", "set", "interface", interface_name, "admin=disable"], check=True)
            print(f"Internet connection for {interface_name} disabled.")
        else:
            print("Unsupported operating system. This function is designed for Windows.")

    def enable_internet_connection():
        """
        Enable the internet connection for a specified network interface.
        Note: Replace "Wi-Fi" with your actual network interface name.
        """
        interface_name = "MaorMain_5"
        if platform.system().lower() == 'windows':
            subprocess.run(["netsh", "interface", "set", "interface", interface_name, "admin=enable"], check=True)
            print(f"Internet connection for {interface_name} enabled.")
        else:
            print("Unsupported operating system. This function is designed for Windows.")
            
            
    def run(self):
        try:
            self.connect()
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            receive_thread.join()

        except KeyboardInterrupt:
            print("Client shutting down.")
        finally:
            self.client_socket.close()


if __name__ == "__main__":
    server_address = "127.0.0.1"  # Change this to the server's IP address
    server_port = 5000  # Change this to the server's port

    client = Client(server_address, server_port)
    client.run()
