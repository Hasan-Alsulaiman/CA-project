from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives.asymmetric import padding  
from cryptography.hazmat.primitives import hashes  
from cryptography.hazmat.primitives.serialization import load_pem_private_key  
from cryptography.hazmat.primitives.serialization import load_pem_public_key  
import cryptography.exceptions
import base64

# this function takes CA's public K + user Public K + signature and verifies it
keypath = ''
def verifyMe(keypath,sigPath,TextPath):
    file = open(TextPath, "rb")
    TextToVerify = file.read()
    file.close()
    print("text to verify:",TextToVerify)
    file = open(sigPath, "rb")
    sig = file.read()
    file.close()
    sig = base64.b64decode(sig)
    print("signature: ", sig)
    key = load_pem_public_key(open(keypath, 'rb').read(),default_backend())  
    try:
        ciphertext = key.verify(  
            sig,  
            TextToVerify,  
            padding.PSS(  
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),  
                    salt_length=padding.PSS.MAX_LENGTH,  
            ),  
            hashes.SHA256()  
        ) 
    except cryptography.exceptions.InvalidSignature as e:
        print('ERROR: Payload and/or signature files failed verification!')
# keypath to server public key
keypath = 'CA_PublicKey.pem'
# path to signed user key
sig = 'Hasan.sig'
#path to user public key
text = 'Client#1PublicKey.pem'
# verifyMe(keypath,sig,text)