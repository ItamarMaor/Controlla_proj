import socket
import cv2
import numpy as np
import zlib

# Set up socket
HOST = '127.0.0.1'  # Server's IP address
PORT = 65432        # Port to listen on
BUFFER_SIZE = 4096  # Size of the buffer for receiving data

# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    # Accept incoming connection
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        
        while True:
            # Receive size of compressed image data (4 bytes)
            size_bytes = conn.recv(4)
            if not size_bytes:
                break

            # Convert size bytes to integer
            size = int.from_bytes(size_bytes, byteorder='big')

            # Receive compressed image data
            received_data = b""
            while len(received_data) < size:
                chunk = conn.recv(min(size - len(received_data), BUFFER_SIZE))
                if not chunk:
                    break
                received_data += chunk

            # Check if all data has been received
            if len(received_data) < size:
                print("Incomplete data received")
                break

            # Debug information
            print("Received compressed image data size:", len(received_data))
            print("Expected size based on size bytes:", size)

            # Decompress the image data
            try:
                img_data = zlib.decompress(received_data)
            except zlib.error as e:
                print("Error decompressing image data:", e)
                continue

            # Convert the image data to numpy array
            img_np = np.frombuffer(img_data, dtype=np.uint8)

            # Decode the image
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            # Check if the image is valid
            if img is None:
                print("Invalid screen image")
                continue
            
            # Display received screen share
            print("Image shape:", img.shape)
            cv2.imshow('Screen Share', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
