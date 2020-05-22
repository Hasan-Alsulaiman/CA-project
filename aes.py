import os,hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def enc(msg,password):
    message = msg.encode()
# Prepare PKCS#7 padded plaintext
# in aes cbc the msg must be a multiple of 16, this is y we need padding/depadding
    padder    = padding.PKCS7(128).padder()
    message = padder.update(message) + padder.finalize()
    backend = default_backend()
    key = hashlib.sha256(password.encode("utf-8")).digest()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    decryptor = cipher.decryptor()
    msg = decryptor.update(ct) + decryptor.finalize()
    return ct,iv

def dec(ct,password,iv):
    backend = default_backend()
    key = hashlib.sha256(password.encode("utf-8")).digest()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    msg = decryptor.update(ct) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(msg)
    decrypted += unpadder.finalize()
    return decrypted


# ct,iv = enc('a secret message','1234')
# d = dec(ct,'1234',iv)
# print(d)