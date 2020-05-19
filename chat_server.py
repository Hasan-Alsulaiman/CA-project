import socket, threading, pickle,ast 


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)

    def run(self):
        while True:
            msg = self.csocket.recv(1024)
            
            if(msg):
                user_info = pickle.loads(msg)
                currentuser = user_info['ClientName']
                chatlist = {'list':[{
                    "username":currentuser,
                    "address":clientAddress,
                    "target":user_info['destination'],
                    "type":user_info['type'],
                    "payload":user_info['payload'],
                    "status": 'online'
                }]
                }
                with open('chatlist.txt','r') as f:
                    oldlist0= f.read()
                    oldlist = ast.literal_eval(oldlist0)

                    print((oldlist))
                    # variable the controls adding new user
                    newuser = True
                    for i in range(len(oldlist['list'])):
                        print(i,"old:" ,oldlist['list'][i]['username'])
                        # if the user is in the list, update his info
                        if(oldlist['list'][i]['username']==chatlist['list'][0]['username']):
                            print(i,'match found, updating...')
                            oldlist['list'][i]=chatlist['list'][0]
                            # dont add new user since inpout user is already signed
                            newuser=False
                    if(newuser):
                        oldlist['list'].append(chatlist['list'][0])



                with open('chatlist.txt','w') as f:
                    # save to file
                    f.write(str(oldlist))
                
                # send list back to student
                self.csocket.sendall(pickle.dumps(oldlist))


                print(chatlist)
            else:
                # when user signs out
                chatlist['list'][0]['status']='offline'
                with open('chatlist.txt','r') as f:
                    oldlist0= f.read()
                    oldlist = ast.literal_eval(oldlist0)
        
                    for i in range(len(oldlist['list'])):
                        # find the user and update his info
                        if(oldlist['list'][i]['username']==chatlist['list'][0]['username']):
                            print(oldlist['list'][i]['username'],'is offline!')
                            oldlist['list'][i]=chatlist['list'][0]
                with open('chatlist.txt','w') as f:
                    f.write(str(oldlist))
                break
        print(chatlist)


LOCALHOST = "127.0.0.1"
PORT = 20000
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