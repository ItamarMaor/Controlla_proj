
import rsa
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

# Generate public + private keypair
publicKey, privateKey = rsa.newkeys(2048)

# Generate a symmetric key
symmetricKey = Fernet.generate_key()
f = Fernet(symmetricKey)

# Sample data to encrypt
data_dict = {'user_id':1, 'name':'John', 'age':30}
data = str(data_dict)

print("\nOriginal data: ", data)

# Encrypt data with symmetric key
enc_data = f.encrypt(data.encode('utf-8'))

# Convert to base64 for sending over the network
b64_enc_data = b64encode(enc_data).decode('utf-8')

# publicKey = rsa.PublicKey.load_pkcs1(publicKey)
enc_symmetricKey = rsa.encrypt(symmetricKey, publicKey)

# Convert the symmetric key to base64 for sending
# over the network
b64_enc_symmetricKey = b64encode(enc_symmetricKey).decode('utf-8')

# Create payload
payload = { 'key':b64_enc_symmetricKey, 'data': b64_enc_data }

print("\nPayload: ", payload)

# Here we send payload over the network
# And receive it somewhere at the client side

# Decode the symmetric key from base64
enc_symmetricKey = b64decode(payload['key'])

# Decode the data from base64
enc_data = b64decode(payload['data'])

# Decrypt the symmetric key
symmetricKey = rsa.decrypt(enc_symmetricKey, privateKey)

# Decrypt the data
f = Fernet(symmetricKey)
data = f.decrypt(enc_data).decode('utf-8')

print("\nDecrypted data: ", data)