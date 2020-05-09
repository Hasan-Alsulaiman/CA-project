import socket
import sys
import pickle

ClientName = "Client#1"
# CSR = cert sign request / CERTUP = cert upload / CERTREQ = cert request
msgType = "CERTREQ"
# user id of another client whose cert is requested
requested = "Client#2"


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

# recieve any initial data from server
while True:
    data = sock.recv(1024)
    if(data):
        response = pickle.loads(data)
        # if server asked for username
        if ( response== 'Please Enter your username'):
            print("recieved: ", pickle.loads(data))
            # enter username
            ans = input('username: ')
            # send username
            sock.sendall(pickle.dumps(ans))
            print('sending', ans)
        # if server fails to find user
        s = 'Username not found!, if you want to sign up send "register: <username>", else send "c" to close connection'
        if (response ==s ):
            print(s)
            ans2 = input('response: ')
            sock.sendall(pickle.dumps(ans2))
            # if user chose to close connection
            if(ans2 == 'c'):
                sock.close()
                print('closing socket')
                break
        if(response=='Welcome'):
            break
    else:
        break

if (response =='Welcome'):
            # get public key
    file = open("Client#1PublicKey.pem", "rb")
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
            message = {'key': cert, 'name': ClientName, 'type': msgType}
            print('sending {!r}'.format(message))
            sock.sendall(pickle.dumps(message))
        # to request the certificate of a certain user
        elif(msgType == "CERTREQ"):
            # send user id of the user whose cert is requested
            message = {'request': requested, 'name': ClientName, 'type': msgType}
            print('sending {!r}'.format(message))
            sock.sendall(pickle.dumps(message))

        while True:
            # recieve data from server
            data = sock.recv(1024)
            if (data):
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
