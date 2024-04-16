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
        """
        Runs the method and displays a blocking window.

        This method sets the `block_key` attribute to True and then displays a blocking window.

        Parameters:
        None

        Returns:
        None
        """
        self.block_key = True
        self._display_blocking_window()

    def unblock(self):
            """
            Unblocks the client.

            This method sets the `block_key` attribute of the client to False,
            allowing the client to continue processing.

            Parameters:
                None

            Returns:
                None
            """
            with threading.Lock():
                self.block_key = False

    def _display_blocking_window(self):
        """
        Displays a blocking window that covers the entire screen and prevents keyboard input.
        This method creates a Tkinter window with a black background and displays a message to listen to the teacher.
        The window remains on top of other windows and cannot be closed until the `block_key` flag is set to False.

        Args:
            None

        Returns:
            None
        """
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
            """
            Export the public key.

            Returns:
                bytes: The exported public key.
            """
            return self.public_key.export_key()
    
    def encrypt(self, plaintext):
        """
        Encrypts the given plaintext using symmetric encryption.

        Args:
            plaintext (bytes): The plaintext to be encrypted.

        Returns:
            bytes: The encrypted ciphertext.
        """
        cipher = Fernet(self.symetric_key)
        ciphertext = b""
        
        while plaintext:
            chunk = plaintext[:self.CHUNK_SIZE]
            plaintext = plaintext[self.CHUNK_SIZE:]
            encrypted_chunk = cipher.encrypt(chunk)
            ciphertext += encrypted_chunk

        return ciphertext
    
    def decrypt(self, ciphertext):
        """
        Decrypts the given ciphertext using symmetric encryption.

        Args:
            ciphertext (bytes): The ciphertext to be decrypted.

        Returns:
            tuple: A tuple containing the command (cmmd) and the decrypted data (data).
        """
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
        """
        Decrypts the given ciphertext using asymmetric encryption.

        Args:
            ciphertext (bytes): The encrypted ciphertext to be decrypted.
            private_key (RSA._RSAobj): The private key used for decryption.

        Returns:
            str: The decrypted plaintext.

        Raises:
            None

        """
        cipher = PKCS1_OAEP.new(private_key)
        plaintext = cipher.decrypt(ciphertext)

        return plaintext.decode()
