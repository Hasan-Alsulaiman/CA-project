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

# open a socket for client to listen to other clients
comtype = input("for chatting press 1\nfor certificate ops press 2\n")
chattype = input("for recieving msg press 1\nfor sending press 2\n")
# recieve msg
if(comtype == '1' and chattype =='1'):
    print('listening..')
    LOCALHOST = "127.0.0.1"
    PORT = 11000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))

    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        print(clientsock, clientAddress,"connected")
        peerdata = clientsock.recv(1024)
        if(peerdata):
            peerdatadecode = pickle.loads(peerdata)
            print(peerdatadecode)
        else:
            break
elif(comtype == '2'):

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
            print(response)
            if(response =='Welcome'):
                break
            ans0 = input("Ans: ")
            sock.sendall(pickle.dumps(ans0))

        else:
            break
    if (response =='Welcome'):
        msgType = input("pick an operation:\n csr = cert sign request \n certup = cert upload \n certreq = cert request\n")
        if(msgType.upper() == "CERTREQ"):
            requested = input("write the username of requested cert 'i.e, Client#2': ")

                # get public key
        file = open("Client#1PublicKey.pem", "rb")
        public = file.read()
        file.close()


        try:
            # to send a certificate signing request
            if(msgType.upper() == "CSR"):

                # Send public key + user id + request type
                message = {'key': public, 'name': ClientName, 'type': msgType}
                print('sending {!r}'.format(message))
                sock.sendall(pickle.dumps(message))
            # to send my certificate for upload
            elif(msgType.upper() == "CERTUP"):
                # open the certificate file
                file = open(ClientName+'.sig', "rb")
                cert = file.read()
                file.close()
                # Send certificate + user id + request type
                message = {'key': cert, 'name': ClientName, 'type': msgType}
                print('sending {!r}'.format(message))
                sock.sendall(pickle.dumps(message))
            # to request the certificate of a certain user
            elif(msgType.upper() == "CERTREQ"):
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
