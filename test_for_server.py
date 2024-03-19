import threading
import queue
import select

# Create a Queue object
global q 
q = queue.Queue()

def get_username_input():
    while True:
        # Check if the client socket is ready for receiving data
        rlist, _, _ = select.select([self.client_socket], [], [], 60)
        if self.client_socket in rlist:
            cmmd = self.client_socket.recv(1).decode('utf-8')
            client_username_len = int(self.client_socket.recv(8).decode('utf-8'))
            client_username = self.client_socket.recv(client_username_len)
            break
    return client_username    

# Create a new thread for the input function
input_thread = threading.Thread(target=get_input,args=(client_socket, client_address ))

# Start the new thread
input_thread.start()

# The while loop will continue running in the main thread
while True:
    # Check if there is something in the queue
    if not q.empty():
        # Get the input from the queue
        user_input = q.get()
        print(f"You entered: {user_input}")