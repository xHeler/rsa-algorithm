import struct


def encrypt_ecb(key, plaintext):
    block_size = len(key)
    padded_plaintext = pad_data(plaintext, block_size)
    ciphertext = bytearray()
    for i in range(0, len(padded_plaintext), block_size):
        block = padded_plaintext[i:i + block_size]
        encrypted_block = bytearray(a ^ b for a, b in zip(block, key))
        ciphertext += encrypted_block
    return bytes(ciphertext)

def decrypt_ecb(key, ciphertext):
    block_size = len(key)
    plaintext = bytearray()
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        decrypted_block = bytearray(a ^ b for a, b in zip(block, key))
        plaintext += decrypted_block
    return bytes(unpad_data(plaintext))


def pad_data(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad_data(data):
    padding_length = data[-1]
    return data[:-padding_length]


key = b"testtestsecret!"

bmp_file_path = "data/test.bmp"
with open(bmp_file_path, 'rb') as f:
    bmp_file_header = f.read(14)
    bmp_info_header = f.read(40)
    data = f.read()

encrypted_data = encrypt_ecb(key, data)

# Save the encrypted data to a BMP file
encrypted_file_path = "ecb/encrypted.bmp"
with open(encrypted_file_path, 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(struct.pack('I', len(encrypted_data)))  # Write the size of the data in 4-byte chunks
    for val in encrypted_data:
        while val > 0:
            chunk = val & 0xFFFFFFFF  # Get the lowest 32 bits of the value
            f.write(struct.pack('!I', chunk))
            val >>= 32  # Shift the value right by 32 bits

decrypted_data = decrypt_ecb(key, encrypted_data)

decrypted_file_path = "ecb/decrypted.bmp"
with open(decrypted_file_path, 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(decrypted_data)
