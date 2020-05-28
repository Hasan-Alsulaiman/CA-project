import socket
import threading
import time
import aes
import pickle
import keysharing

# thread for recieving
def reciever(server,myname):
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        print(clientsock, clientAddress,"connected")
        peerdata = clientsock.recv(1024)
        if(peerdata):
            print("incoming msg...")
            data = pickle.loads(peerdata)
            print("encrypted msg: ",data[0])
            # decrypt the encrypted password using my private key
            password = keysharing.dec(myname+"PrivateKey.pem",b"myPassword",data[2])
            decmsg = aes.dec(data[0],password,data[1])
            print("msg: ",decmsg)
        else:
            break
        break


# thread for sending
def sender(target,targetname):
    # Create a TCP/IP socket
    sock = socket.create_connection(('localhost', target))
    msg = input("Enter your messege: ")
    password = input("please choose a password: ")
    # encrypt the msg with the password
    cyphertext, iv = aes.enc(msg,password)
    # encrypt the password using target user's public key
    encpassword = keysharing.enc(targetname+"PublicKey.pem",password)
    # put the msg in serial mode for sending
    msgtobesent = pickle.dumps([cyphertext,iv,encpassword])
    sock.sendall(msgtobesent)
    ex = input("terminate connection?<y>/<n>")
    if(ex=='y'):
        print("closing socket..")
        sock.close()
        return
def communication(myname,myport,targetname,targetport):
    LOCALHOST = "127.0.0.1"
    PORT = myport
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    # thread to handle listening
    R = threading.Thread(target=reciever, args=(server,myname))
    R.start()
    print("listening for incoming connections...")
    # thread to send
    S = threading.Thread(target=sender, args=(targetport,targetname))
    i = input("would you like to send a msg?<y>/<n> ")
    if (i =='y'):
        S.start()
    
# communication(11000,12000)