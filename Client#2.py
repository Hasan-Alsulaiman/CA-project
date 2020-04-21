import socket
import sys
import pickle

ClientName = "Client#2"
# CSR = cert sign request / CERTUP = cert upload / CERTREQ = cert request
msgType = "CSR"
# user id of another client whose cert is requested
requested = "Client#1"

def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n
        for n in dir(socket)
        if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# Create a TCP/IP socket
sock = socket.create_connection(('localhost', 10000))

print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])
print()

# get public key
file = open("Client#2PublicKey.pem", "rb")
public = file.read()
file.close()


try:
    # to send a certificate signing request
    if(msgType == "CSR"):

        # Send public key + user id + request type
        message = {'key': public, 'name': ClientName, 'type': msgType}
        print('sending {!r}'.format(message))
        sock.sendall(pickle.dumps(message))
    # to send my certificate for upload
    elif(msgType == "CERTUP"):
        # open the certificate file 
        file = open(ClientName+'.sig', "rb")
        cert = file.read()
        file.close()
        # Send certificate + user id + request type
        message = {'key':cert, 'name': ClientName, 'type': msgType}
        print('sending {!r}'.format(message))
        sock.sendall(pickle.dumps(message))
    # to request the certificate of a certain user
    elif(msgType == "CERTREQ"):
        # send user id of the user whose cert is requested
        message = {'requested':requested, 'name': ClientName, 'type': msgType}
        print('sending {!r}'.format(message))
        sock.sendall(pickle.dumps(message))


    while True:
        # recieve data from server
        data = sock.recv(1024)
        print("recieved: ", pickle.loads(data))
        # ask the client whether he wants to continue
        ans = input('\nTerminate connection? (y/n) :')
        # prompt user to close the connection
        if ans == 'n':
            continue
        else:
            break


finally:
    print('closing socket')
    sock.close()
