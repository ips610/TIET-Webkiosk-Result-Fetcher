from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding as symmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Key generation using PBKDF2HMAC
password = b"mysecretpassword"
salt = b"secretsalt"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    iterations=100000,
    salt=salt,
    length=32,  # AES-256 requires a 256-bit key
)

key = kdf.derive(password)

# Encryption using AES
cipher = Cipher(algorithms.AES(key), modes.CFB8(iv=b"initialization_vector"), backend=default_backend())
encryptor = cipher.encryptor()

data = b"Hello, world!"
encrypted_data = encryptor.update(data) + encryptor.finalize()

# Decryption using AES
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

print("Original Data:", data)
print("Encrypted Data:", encrypted_data)
print("Decrypted Data:", decrypted_data)
