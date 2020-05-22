import socket
import threading
import time

def reciever(server):
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        print(clientsock, clientAddress,"connected")
        peerdata = clientsock.recv(1024)


    
def sender(target):
    # Create a TCP/IP socket
    sock = socket.create_connection(('localhost', target))
    ex = input("terminate connection?<y>/<n>")
    if(ex=='y'):
        sock.close()
def communication(myport,targetport):
    LOCALHOST = "127.0.0.1"
    PORT = myport
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))

    R = threading.Thread(target=reciever, args=(server,))
    R.start()
    S = threading.Thread(target=sender, args=(targetport,))
    i = input("would you like to send a msg?<y>/<n>")
    if (i =='y'):
        S.start()

# communication(11000,12000)