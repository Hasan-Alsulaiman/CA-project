### Phase 1 - Certificate Signing:

this system consist of a TCP multi-threaded server "server_multithread.py" acting as a certificate authority CA and two clients "Client#1" and "Client#2", together they simulate a group of user who need to get their private keys signed by the CA, the CA and both clients have generated and saved their keys previously (private keys are encrypted, public keys are not).

how it works:
1. first run the server in a terminal.
2. run any or both of the clients, each from a separate terminal.
3. after a client successfully connects, the server reserves a separate thread for it, and the client will send a message to the server, it contains:
    • client id
    • client's public key
    • type (this is set to CSR at this phase)
4. the server then takes the client's public key and signs it using the server's private key and sends the signed key back to client, also, it saves a copy of that in a file named after the client's id.
5. at this point, the client side is prompted to close the connection.
6. during all of this the server continues to listen for new connections.

note: because each client is handled in a different thread at the server, we can handle multiple clients, and even if one client experiences an error the others will continue to work unaffected. 

### Phase 2 - Certificate Exchange:
in this phase, users can do more than just create certificates, they now can request another user's certificate from the server. they can also upload their own certificate to the certificate sharing server.
     note: the certificate sharing server is also multi-threaded, it runs on the same ip as the certificate signing server, but there is no overlap between them since each of them runs on a different thread.
     in order for the server to distinguish between the different functions it must perform for the client, the client selects the desired function using the "type" variable in the message he sends, the type can be:
     
- type = CSR / for certificate signing request
   in this case the client uploads his public key + his id + type = CSR
- type = CERTUP / for certificate upload
   in this case the client uploads his signed key + his id + type = CERTUP
- type = CERTREQ / for certificate request
   in this case the client uploads the id of requested user + his id + type = CERTREQ
    
### phase 3 - Authentication:
once a client connects to the server he is asked for his username and password, if he is registered he can continue as usual, otherwise he can register as a new user.
     after successfully signing in, the client is prompted to pick an operation by entering the operation's name.

### phase 4 - inter-client communications
in this phase two clients will connect and share messages between each other, the messages are encrypted using AES and the password is secured using asymmetric encryption.
  #### operation steps:

- run `Client#1.py`
- choose "to listen for new connections"
- now open a new command line and run `Client#2.py`
- choose "to start new connection"
- now you can send and recieve messages

     

whenever one of the users terminates his connection, he will return to listening mode and the other user can start a new connection and send messages (the sender and reciever can exchange roles)
the reason we do things in this order is because we cant start a new connection if no one is listening for it.



hasan.alsulaimanaqa@agu.edu.tr
