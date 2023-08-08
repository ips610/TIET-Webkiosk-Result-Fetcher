from Crypto.Cipher import AES
import hashlib
import binascii
from cryptography.fernet import Fernet


# we will be encrypting the below string.
message = "hello geeks"

# generate a key for encryption and decryption
# You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key

key = Fernet.generate_key()
print(key)
# Instance the Fernet class with the key

fernet = Fernet(key)
# then use the Fernet class instance
# to encrypt the string string must
# be encoded to byte string before encryption
encMessage = fernet.encrypt(message.encode())

print("original string: ", message)
print("encrypted string: ", encMessage)

# decrypt the encrypted string with the
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods


def derive_key(secretKey):
    # Use SHA-256 to derive a 256-bit (32-byte) key from the provided key
    key_derived = hashlib.sha256(secretKey).digest()
    return key_derived

def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(encryptedMsg, secretKey):
    (ciphertext, nonce, authTag) = encryptedMsg
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

# Replace this with your own secret key
secretKey = b'7CuCmt3kZYdc1NurpLVnWDe6tPf1'

# Derive a 256-bit key from the input secret key
derivedSecretKey = derive_key(secretKey)
print(derivedSecretKey)
# msg = b'Message for AES-256-GCM encryption'
encryptedMsg = encrypt_AES_GCM(encMessage, derivedSecretKey)
# print("encryptedMsg", {
#     'ciphertext': binascii.hexlify(encryptedMsg[0]),
#     'aesIV': binascii.hexlify(encryptedMsg[1]),
#     'authTag': binascii.hexlify(encryptedMsg[2])
# })
print(encryptedMsg)
decryptedMsg = decrypt_AES_GCM(encryptedMsg, derivedSecretKey)
print("decryptedMsg", decryptedMsg)

decMessage = fernet.decrypt(decryptedMsg).decode()

print("decrypted string: ", decMessage)