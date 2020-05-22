import socket
import threading
import time

def reciever(name):
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        print(clientsock, clientAddress,"connected")
        peerdata = clientsock.recv(1024)


    
def sender(name):
    # Create a TCP/IP socket
    sock = socket.create_connection(('localhost', 11000))
    ex = input("terminate connection?<y>/<n>")
    if(ex=='y'):
        sock.close()
if __name__ == "__main__":
    LOCALHOST = "127.0.0.1"
    PORT = 12000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))

    x = threading.Thread(target=reciever, args=(server,))
    x.start()
    y = threading.Thread(target=sender, args=(1000,))
    y.start()

