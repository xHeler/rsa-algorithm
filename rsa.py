import random
import struct


# Miller-Rabin primality test
def is_prime(n, k=5):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_large_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y


def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def generate_keypair(bits):
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    e, n = pk
    return [pow(char, e, n) for char in plaintext]


def decrypt(sk, ciphertext):
    d, n = sk
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])


# Generate RSA keys
KEY_SIZE = 128
public_key, private_key = generate_keypair(KEY_SIZE)

# Load the encrypted data from the file
encrypted_file_path = "data/test.bmp"
with open(encrypted_file_path, 'rb') as f:
    bmp_file_header = f.read(14)
    bmp_info_header = f.read(40)
    data = f.read()

encrypted_data = encrypt(public_key, data)

# Save the encrypted data to a BMP file
encrypted_file_path = "rsa/encrypted.bmp"
with open(encrypted_file_path, 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(struct.pack('I', len(encrypted_data)))  # Write the size of the data in 4-byte chunks
    for val in encrypted_data:
        while val > 0:
            chunk = val & 0xFFFFFFFF  # Get the lowest 32 bits of the value
            f.write(struct.pack('!I', chunk))
            val >>= 32  # Shift the value right by 32 bits

decrypted_data = decrypt(private_key, encrypted_data)
decrypted_file_path = "rsa/decrypted.bmp"
with open(decrypted_file_path, 'wb') as f:
    f.write(bmp_file_header)
    f.write(bmp_info_header)
    f.write(bytes(decrypted_data, 'latin-1'))