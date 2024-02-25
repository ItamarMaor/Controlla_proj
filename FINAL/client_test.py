import socket
import pyautogui
import zlib

# Set up socket
HOST = '127.0.0.1'  # Server's IP address
PORT = 65432        # Port to connect to

# Connect to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        # Capture screen
        screenshot = pyautogui.screenshot()

        # Convert screenshot to bytes
        img_bytes = screenshot.tobytes()

        # Compress the image data
        compressed_img_bytes = zlib.compress(img_bytes)

        # Send the size of compressed image data
        try:
            s.sendall(len(compressed_img_bytes).to_bytes(4, byteorder='big'))
        except Exception as e:
            print("Error sending size of compressed image data:", e)
            break

        # Send the compressed image data
        try:
            s.sendall(compressed_img_bytes)
        except Exception as e:
            print("Error sending compressed image data:", e)
            break
