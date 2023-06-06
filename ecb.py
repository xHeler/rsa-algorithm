from itertools import zip_longest


def pad_data(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding


def unpad_data(data):
    padding_length = data[-1]
    return data[:-padding_length]


def encrypt_ecb(key, plaintext):
    block_size = len(key)
    padded_plaintext = pad_data(plaintext, block_size)
    ciphertext = b""
    for i in range(0, len(padded_plaintext), block_size):
        block = padded_plaintext[i:i+block_size]
        encrypted_block = bytes(a ^ b for a, b in zip(block, key))
        ciphertext += encrypted_block
    return ciphertext


def decrypt_ecb(key, ciphertext):
    block_size = len(key)
    plaintext = b""
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        decrypted_block = bytes(a ^ b for a, b in zip(block, key))
        plaintext += decrypted_block
    return unpad_data(plaintext)


# Key and plaintext
key = b'SecretKey1234567'
plaintext = b'This is a secret message'

# Encrypt using ECB
ciphertext = encrypt_ecb(key, plaintext)

# Decrypt
decrypted_text = decrypt_ecb(key, ciphertext)

print('Original data:', plaintext)
print('Encrypted data:', ciphertext)
print('Decrypted data:', decrypted_text)
