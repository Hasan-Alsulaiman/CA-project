import hashlib, binascii, os, json

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

# function takes two password and a position of a user in a list, compares two passwords
def verify_password(username, provided_password,position):
    with open ('UserList.json','r') as f:
        users = json.load(f)
        f.close()
    stored_password = users["list"][position][username]["password"]
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


# C = hash_password("hi")

# V = verify_password("alli","123",1)
# print(V)
