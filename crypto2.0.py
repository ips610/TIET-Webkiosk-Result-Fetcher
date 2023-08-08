from Crypto.Cipher import AES
import hashlib
import binascii

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
msg = b'Message for AES-256-GCM encryption'
encryptedMsg = encrypt_AES_GCM(msg, derivedSecretKey)
print("encryptedMsg", {
    'ciphertext': binascii.hexlify(encryptedMsg[0]),
    'aesIV': binascii.hexlify(encryptedMsg[1]),
    'authTag': binascii.hexlify(encryptedMsg[2])
})

decryptedMsg = decrypt_AES_GCM(encryptedMsg, derivedSecretKey)
print("decryptedMsg", decryptedMsg)
