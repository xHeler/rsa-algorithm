from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


KEY_SIZE = 128

# Replace the following strings with your own PEM-encoded private and public keys
private_key_pem = b'''
-----BEGIN RSA PRIVATE KEY-----
MGICAQACEQCUjEOXbKhFlUUWhTJjRud/AgMBAAECEHWK78kYT6aOmnzIRr1lqNEC
CQDaaUpnCwYsQwIJAK4c8zdydEIVAghEdmKzIBqEPwIJAKJeJQIEHh6xAghblY0g
qRDOTg==
-----END RSA PRIVATE KEY-----
'''

public_key_pem = b'''
-----BEGIN RSA PUBLIC KEY-----
MBgCEQCUjEOXbKhFlUUWhTJjRud/AgMBAAE=
-----END RSA PUBLIC KEY-----
'''

# Load private key from PEM string
private_key = load_pem_private_key(private_key_pem, password=None, backend=default_backend())

# Load public key from PEM string
public_key = load_pem_public_key(public_key_pem, backend=default_backend())

bmp_path = "data/test.bmp"

with open(bmp_path, 'rb') as f:
    bmp_file_header = f.read(14)
    bmp_info_header = f.read(40)
    data = f.read()

chunk_size = KEY_SIZE // 8 - 11
chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

encrypted_chunks = [public_key.encrypt(chunk, padding.PKCS1v15()) for chunk in chunks]
encrypted = b''.join(encrypted_chunks)

with open("rsa_lib/encrypted.bmp", 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(encrypted)

decrypted_chunks = [private_key.decrypt(chunk, padding.PKCS1v15()) for chunk in encrypted_chunks]
decrypted = b''.join(decrypted_chunks)

with open("rsa_lib/decrypted.bmp", 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(decrypted)
