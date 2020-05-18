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
def chat(user_info,server_port):
    # Create a TCP/IP socket
    sock = socket.create_connection(('localhost', server_port))
    sock.sendall(pickle.dumps(user_info))
    
    end = input('end connection? <y>/<n>')
    if(end == 'y'):
        sock.close()




families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# check what the user wants to do
while True:
    operation = input("Enter the number of desired operation:\n <1> certificate operations\n <2> chat\n> ")
    if(operation == '1'):
        server_port = 10000
        break
    elif(operation == '2'):
        server_port = 20000
        break
    else:
        print("the number you entered does not match an existing operation!")
        continue
print (server_port)

# chat operations
if(server_port == 20000):
    msg='hi'
    user_info = {'ClientName':ClientName,'destination':requested,'type':'key'}
    chat(user_info,server_port)
elif(server_port==10000):


    # Create a TCP/IP socket
    sock = socket.create_connection(('localhost', server_port))

    print('Family  :', families[sock.family])
    print('Type    :', types[sock.type])
    print('Protocol:', protocols[sock.proto])
    address, port = sock.getsockname()
    print("address/port: ",address, port)




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
