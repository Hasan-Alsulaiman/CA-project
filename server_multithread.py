import socket, threading, pickle, signIt, base64, os.path,verifyIt
# password to my private key
password = b'myPassword'
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
        # get username
        msg = 'Please Enter your username'
        self.csocket.sendall(pickle.dumps(msg))
        # the username that the client sent
        ans = self.csocket.recv(1024)
        if(ans):
            username = pickle.loads(ans)
            print("username: ",username)
            # check if username exists in database UserList.json
            Authentication = verifyIt.verifyUser(username)
            if(Authentication):
                print("user authenticated successfully")
                msg = 'Welcome'
                self.csocket.sendall(pickle.dumps(msg))
            else:
                print('user authentication failed!')
                msg = 'Username not found!, if you want to sign up send "register: <username>", else send "c" to close connection'
                self.csocket.sendall(pickle.dumps(msg))
                result = self.csocket.recv(1024)
                if(result):
                    ans2 = pickle.loads(result)
                    print(ans2)
                    if(ans2 == 'c'):
                        print("bye")
                        clientsocket.close()
                    elif(ans2[:8]=='register'):
                        print("registering new user")
    def run(self):
        print ("Connection from : ", clientAddress)
        while True:
            data = self.csocket.recv(1024)
            if data:
                dataUnpickled = pickle.loads(data)
                # if the incoming msg is a certificate signing request
                if(dataUnpickled['type']=='CSR'):
                    print("Recieved a certificate signing request...")
                    print("RECIEVED DATA: ",dataUnpickled['key'])
                    # sign the clients public key and return the signature
                    SignedKey = signIt.signMe("CA_PrivateKey.pem",dataUnpickled['key'],password)
                    print('sending data back to the client')
                    KeyNameSignature = {'CLIENT ID':dataUnpickled['name'],'CLIENT KEY':dataUnpickled['key'],'SIGNED CLIENT KEY':SignedKey}
                    self.csocket.sendall(pickle.dumps(KeyNameSignature))
                    print('finished ;)')
                    # Save the Public key in PEM format  
                    with open(dataUnpickled['name']+'.sig', "wb") as f:  
                        f.write(base64.b64encode(SignedKey))
                # if the incoming msg is a certificate upload
                elif(dataUnpickled['type']=='CERTUP'):
                    print("Recieved a certificate ...")
                    print("RECIEVED DATA: ",dataUnpickled['key'])
                    # Save the certificate key   
                    with open(dataUnpickled['name']+'.sig', "wb") as f:  
                        f.write(base64.b64encode(dataUnpickled['key']))
                    # send back an acknowledge
                    self.csocket.sendall(pickle.dumps('ack'))
                # if incoming msg is cert request
                elif(dataUnpickled['type']=='CERTREQ'):
                    print("Recieved a certificate request...")
                    print("RECIEVED DATA: ",dataUnpickled['request'])
                    # send back the cert of requested user (if exists)
                    check = os.path.exists(dataUnpickled['request']+'.sig')
                    if(check):
                        print(dataUnpickled['request']+' certificate found, sending...')
                        with open(dataUnpickled['request']+'.sig', "rb") as f:
                            certificate = f.read()
                            f.close()
                            msg = {'cert':certificate,'id':dataUnpickled['request']}
                            self.csocket.sendall(pickle.dumps(msg))
                            print('finished ;)')
                    else:
                        msg = dataUnpickled['request']+" certificate does not exist"
                        print(msg)
                        self.csocket.sendall(pickle.dumps(msg))

                        


                

            else:
                print("bye")
                break

LOCALHOST = "127.0.0.1"
PORT = 10000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
