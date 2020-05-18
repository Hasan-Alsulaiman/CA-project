import socket, threading, pickle


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
                user_list = {currentuser:{
                    'address':clientAddress,
                    'target':user_info['destination'],
                    'type':user_info['type'],
                    'status': 'online'
                }
                }
                print(user_list)
            else:
                user_list[currentuser]['status']='offline'
                break
        print(user_list)


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