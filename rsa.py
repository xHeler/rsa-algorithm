from prime_numbers import generate_keypair



def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plaintext)

public_key, private_key = generate_keypair()
message = "Hello RSA!"
cipher = encrypt(public_key, message)
print(f'Ciphertext: {cipher}')
decrypted_message = decrypt(private_key, cipher)
print(f'Decrypted Message: {decrypted_message}')






