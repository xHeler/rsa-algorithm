from PIL import Image
import numpy as np

from prime_numbers import generate_keypair


def encrypt(public_key, plain_text):
    e, n = public_key
    encrypted_text = [pow(int(pixel), e, n) for pixel in plain_text]
    return encrypted_text

def decrypt(private_key, encrypted_text):
    d, n = private_key
    decrypted_text = [pow(int(pixel), d, n) for pixel in encrypted_text]
    return decrypted_text

def main():
    public_key, private_key = generate_keypair()

    # Open BMP image and convert it to a numpy array
    im = Image.open('all_gray.bmp')
    pixel_array = np.array(im, dtype=int)  # force all values to int

    # Convert pixel data to 1D numpy array
    pixel_data_1D = pixel_array.flatten()

    # Encrypt the image
    encrypted_pixel_data = encrypt(public_key, pixel_data_1D)

    # Convert back to original shape
    encrypted_pixel_array = np.array(encrypted_pixel_data).reshape(pixel_array.shape)
    
    # Save the encrypted image
    encrypted_im = Image.fromarray(encrypted_pixel_array.clip(0, 255).astype(np.uint8)) # clip values to range 0-255 and convert to uint8
    encrypted_im.save('encrypted.bmp')
    
    # Open encrypted image and convert it to a numpy array
    encrypted_im = Image.open('encrypted.bmp')
    encrypted_pixel_array = np.array(encrypted_im, dtype=int)  # force all values to int

    # Convert pixel data to 1D numpy array
    encrypted_pixel_data_1D = encrypted_pixel_array.flatten()

    # Decrypt the image
    decrypted_pixel_data = decrypt(private_key, encrypted_pixel_data_1D)

    # Convert back to original shape
    decrypted_pixel_array = np.array(decrypted_pixel_data).reshape(pixel_array.shape)
    
    # Save the decrypted image
    decrypted_im = Image.fromarray(decrypted_pixel_array.clip(0, 255).astype(np.uint8)) # clip values to range 0-255 and convert to uint8
    decrypted_im.save('decrypted.bmp')

if __name__ == "__main__":
    main()
