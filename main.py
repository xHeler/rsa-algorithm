from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


KEY_SIZE = 2048

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=KEY_SIZE,
    backend=default_backend()
)
public_key = private_key.public_key()

bmp_path = "data/test.bmp"

with open(bmp_path, 'rb') as f:
    bmp_file_header = f.read(14)
    bmp_info_header = f.read(40)
    data = f.read()

chunk_size = KEY_SIZE // 8 - 11
chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

encrypted_chunks = [public_key.encrypt(chunk, padding.PKCS1v15()) for chunk in chunks]
encrypted = b''.join(encrypted_chunks)

with open("encrypted_image.bmp", 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(encrypted)

decrypted_chunks = [private_key.decrypt(chunk, padding.PKCS1v15()) for chunk in encrypted_chunks]
decrypted = b''.join(decrypted_chunks)

with open("decrypted_image.bmp", 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(decrypted)
