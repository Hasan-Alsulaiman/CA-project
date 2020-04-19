from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives.asymmetric import padding  
from cryptography.hazmat.primitives import hashes  
from cryptography.hazmat.primitives.serialization import load_pem_private_key  
from cryptography.hazmat.primitives.serialization import load_pem_public_key  
import base64


# this function signs variable "TextToSign" using private key that is pointed to using "keypath" 
# the "password" is used to decrypt the private key
# function returns "sig" a signed key
def signMe(keypath, TextToSign,password):
    # open specified keyPath and get key

    key = load_pem_private_key(open(keypath, 'rb').read(),password,default_backend())  

    sig = key.sign(  
    TextToSign,  
    padding.PSS(  
        mgf=padding.MGF1(algorithm=hashes.SHA256()),  
        salt_length=padding.PSS.MAX_LENGTH,  
    ),  
    hashes.SHA256()
    )
    return sig


password = b'myPassword'
keypath = 'CA_PrivateKey.pem'



