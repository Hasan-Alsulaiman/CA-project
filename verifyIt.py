from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives.asymmetric import padding  
from cryptography.hazmat.primitives import hashes  
from cryptography.hazmat.primitives.serialization import load_pem_private_key  
from cryptography.hazmat.primitives.serialization import load_pem_public_key  
import cryptography.exceptions
import base64
import json

# this function takes CA's public K + user Public K + signature and verifies it
keypath = ''
def verifyMe(keypath,sigPath,PublicKey):
    file = open(PublicKey, "rb")
    publicKey = file.read()
    file.close()
    print("text to verify:",publicKey)
    file = open(sigPath, "rb")
    sig = file.read()
    file.close()
    sig = base64.b64decode(sig)
    print("signature: ", sig)
    key = load_pem_public_key(open(keypath, 'rb').read(),default_backend())  
    try:
        ciphertext = key.verify(  
            sig,  
            publicKey,  
            padding.PSS(  
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),  
                    salt_length=padding.PSS.MAX_LENGTH,  
            ),  
            hashes.SHA256()  
        ) 
        error = False
    except cryptography.exceptions.InvalidSignature as e:
        error = True
    if(error):
        print('ERROR: Payload and/or signature files failed verification!')
    else:
        print("succsess!")

# this function authenticates a newly connected user, prompts him to sign up if not already
def verifyUser(ans):
    print('checking...')
    # open the user list
    with open ('UserList.json','r') as f:
        users = json.load(f)
        f.close()
    print('opened list...')
    # check for that particular user
    if(ans in users["list"][0]):
        # if exists, return True
        return True
    else:
        # if not exists return False
        return False


# keypath to server public key
# keypath = 'CA_PublicKey.pem'
# path to signed user key
# sig = 'Client#2.sig'
#path to user public key
# publicKey = 'Client#2PublicKey.pem'
# call the function
# verifyMe(keypath,sig,publicKey)
print(verifyUser('hasan'))
