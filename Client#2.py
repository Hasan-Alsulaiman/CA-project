import socket
import sys
import pickle

ClientName = "Client#2"
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
file = open("Client#1PublicKey.pem", "rb")
public = file.read()
file.close()
print(public)


try:

    # Send data, public key + user id + request type
    message = {'key': public, 'name': ClientName, 'type': 'CSR'}
    print('sending {!r}'.format(message))
    sock.sendall(pickle.dumps(message))

    while True:
        data = sock.recv(1024)
        # amount_received += len(data)
        # print('received {!r}'.format(data))
        print("recieved: ", pickle.loads(data))
        # ask the client whether he wants to continue
        ans = input('\nTerminate connection? (y/n) :')
        if ans == 'n':
            continue
        else:
            break


finally:
    print('closing socket')
    sock.close()
