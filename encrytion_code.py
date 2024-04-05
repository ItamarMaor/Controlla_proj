from cryptography.fernet import Fernet
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class HybridEncryptionServer:
    def __init__(self):
        # Initialize any necessary variables or objects here
        self.key = None
        self.public_key = None
        self.private_key = None
    
    def generate_symetric_key(self):
        # Implement code to generate encryption key
        return Fernet.generate_key()
    
    def recv_public_key(self, pem_key):
        return RSA.import_key(pem_key)
    
    def encrypt(self, plaintext, symetric_key):
        # Implement code to encrypt ciphertext using symmetric encryption
        cipher = Fernet(symetric_key)
        ciphertext = cipher.encrypt(plaintext.encode())
        return ciphertext
    
    def decrypt(self, ciphertext, symetric_key):
        # Implement code to decrypt ciphertext using symmetric encryption
        cipher = Fernet(symetric_key)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()
    
    def encrypt_asymmetric(self, plaintext, public_key):
        # Implement code to encrypt plaintext using asymmetric encryption
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(plaintext.encode())
        return ciphertext

class HybridEncryptionClient:
    def __init__(self):
        # Initialize any necessary variables or objects here
        self.key = RSA.generate(1024)
        self.public_key = self.key.publickey()
        self.private_key = self.key
        self.symetric_key = None
        
    def export_public_key(self):
        return self.public_key.export_key()
    
    # TODO: Depends on the max len of the encryption, split to chunks might be needed
    def encrypt(self, plaintext, symetric_key):
        # Implement code to encrypt ciphertext using symmetric encryption
        cipher = Fernet(symetric_key)
        ciphertext = cipher.encrypt(plaintext.encode())
        return ciphertext
    
    def decrypt(self, ciphertext, symetric_key):
        # Implement code to decrypt ciphertext using symmetric encryption
        cipher = Fernet(symetric_key)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()
    
    def decrypt_asymmetric(self, ciphertext, private_key):
        # Implement code to encrypt plaintext using asymmetric encryption
        cipher = PKCS1_OAEP.new(private_key)
        plaintext = cipher.decrypt(ciphertext)

        return plaintext.decode()
