import threading
import tkinter as tk
from cryptography.fernet import Fernet
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class WindowBlocker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.block_key = False

    def run(self):
        self.block_key = True
        self._display_blocking_window()

    def unblock(self):
        with threading.Lock():
            self.block_key = False

    def _display_blocking_window(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("Keyboard Blocker")
        self.root['background'] = 'black'
        self.root.wm_attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        label = tk.Label(self.root, text="Computer blocked.\nListen to your teacher now!",
                         font=("Garamond", 25), fg='white', bg='black')
        logo = tk.Label(self.root, text="Controlla",
                    font=("Garamond", 20), fg='white', bg='black')
        label.pack(side="top", fill="both", expand=True)
        logo.pack(side="bottom", fill="both", expand=True)
        # tk.Button(self.root, text="Unblock", command=self.unblock).pack(side="bottom")

        while self.block_key:
            self.root.update()
            self.root.update_idletasks()

        self.root.destroy()

class HybridEncryptionClient():
    def __init__(self):
        # Initialize any necessary variables or objects here
        self.key = RSA.generate(1024)
        self.public_key = self.key.publickey()
        self.private_key = self.key
        self.symetric_key = None
        self.CHUNK_SIZE = 2**32 - 33
        
    def export_public_key(self):
        return self.public_key.export_key()
    
    def encrypt(self, plaintext):
        # Implement code to encrypt ciphertext using symmetric encryption
        cipher = Fernet(self.symetric_key)
        ciphertext = b""
        
        while plaintext:
            chunk = plaintext[:self.CHUNK_SIZE]
            plaintext = plaintext[self.CHUNK_SIZE:]
            encrypted_chunk = cipher.encrypt(chunk)
            ciphertext += encrypted_chunk
    
        return ciphertext
    
    def decrypt(self, ciphertext):
        # Implement code to decrypt ciphertext using symmetric encryption
        cipher = Fernet(self.symetric_key)
        plaintext = b""
        
        while ciphertext:
            chunk = ciphertext[:self.CHUNK_SIZE]
            ciphertext = ciphertext[self.CHUNK_SIZE:]
            decrypted_chunk = cipher.decrypt(chunk)
            plaintext += decrypted_chunk
        
        plaintext = plaintext.decode()
        cmmd = plaintext[:1]
        data = plaintext[1:]
        
        return cmmd, data
    
    def decrypt_asymmetric(self, ciphertext, private_key):
        # Implement code to encrypt plaintext using asymmetric encryption
        cipher = PKCS1_OAEP.new(private_key)
        plaintext = cipher.decrypt(ciphertext)

        return plaintext.decode()

# class Encryption():
#     def __init__(self):
#         pass

# class ClientFunctions():   
#     def ask_for_username(self):
#         def on_click():
#             global uname
#             uname = name_entry.get()
#             root.destroy()
        
#         root = tk.Tk()
#         root.wm_attributes("-topmost", True)
#         header = tk.Label(root, text='Enter client username')
#         name_entry = tk.Entry(root)
#         ok_button = tk.Button(root, text='OK', command=on_click)
#         header.pack()
#         name_entry.pack()
#         ok_button.pack()
        
#         root.mainloop()    
        
#         return uname    pass
