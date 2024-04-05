from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io
import getpass
import os


# Function to encrypt an image using AES with password
def encrypt_image(image_path, password):
    # Open the image
    image = Image.open(image_path)
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    img_bytes = img_byte_arr.getvalue()
    img_byte_arr.close()

    # Derive key from password using PBKDF2
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)  # 32 bytes for AES-256

    # Initialize AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC)
    # Encrypt the image bytes
    cipher_text = cipher.encrypt(pad(img_bytes, AES.block_size))

    return salt + cipher.iv + cipher_text


# Function to decrypt an image using AES with password
def decrypt_image(salt, iv, cipher_text, password):
    # Derive key from password using PBKDF2
    key = PBKDF2(password, salt, dkLen=32)  # 32 bytes for AES-256

    # Initialize AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt the cipher text
    decrypted_bytes = unpad(cipher.decrypt(cipher_text), AES.block_size)

    # Convert decrypted bytes to image
    image = Image.open(io.BytesIO(decrypted_bytes))
    return image


# Function to save encrypted image along with IV and salt
def save_encrypted_image(encrypted_image_path, salt, iv, cipher_text):
    with open(encrypted_image_path, "wb") as f:
        # Write the salt, IV, and encrypted image data to the file
        f.write(salt)
        f.write(iv)
        f.write(cipher_text)


# Function to load encrypted image, IV, and salt for decryption
def load_encrypted_image(encrypted_image_path):
    with open(encrypted_image_path, "rb") as f:
        # Read the salt from the file
        salt = f.read(16)  # Salt size is 16 bytes
        # Read the IV from the file
        iv = f.read(16)  # IV size is 16 bytes
        # Read the encrypted image data from the file
        cipher_text = f.read()

    return salt, iv, cipher_text


# Main menu function
def main_menu():
    print("Welcome to Image Encryption/Decryption Program")
    print("1. Encrypt Image")
    print("2. Decrypt Image")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice


# Encrypt image function
def encrypt_image_menu(image_path):
    password = getpass.getpass(prompt="Enter password for encryption: ")
    encrypted_data = encrypt_image(image_path, password)
    return encrypted_data


# Decrypt image function
def decrypt_image_menu(encrypted_data):
    password = getpass.getpass(prompt="Enter password for decryption: ")

    salt = encrypted_data[:16]  # First 16 bytes (16*8 bits)
    iv = encrypted_data[16:32]  # Next 16 bytes (16*8 bits)
    cipher_text = encrypted_data[32:]

    # Attempt decryption with the provided password
    try:
        decrypted_image = decrypt_image(salt, iv, cipher_text, password)
        decrypted_image.show()
        decrypted_image.save("temp.png")
        print("Extracted data saved as temp.png")
    except ValueError:
        print("Error: Incorrect password!")
    except Exception as e:
        print("Error:", e)


# Main program loop
