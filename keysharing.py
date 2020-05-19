from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives.asymmetric import rsa  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.serialization import load_pem_private_key  
from cryptography.hazmat.primitives.serialization import load_pem_public_key  
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

#give the function public key and a msg to encrypt
# or
# give it a private key and cipher to decrypt
  
# to encrypt the symetric key using the reciever's public key
def enc(keypath,symkey):
    public_key = load_pem_public_key(open(keypath, 'rb').read(),default_backend())
    symkey = bytes(symkey,encoding='utf-8')
    encrypted = public_key.encrypt(
    symkey,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))
    return encrypted
# to decrypt a symmetric key thats been encrypted with public key of user
def dec(keypath,password,encryptedkey):
    key = load_pem_private_key(open(keypath, 'rb').read(),password,default_backend())
    original_message = key.decrypt(
    encryptedkey,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
    return original_message.decode('utf-8')



results = enc("Client#2PublicKey.pem",'1234')
print(results)
print(dec("Client#2PrivateKey.pem",b'myPassword',results))