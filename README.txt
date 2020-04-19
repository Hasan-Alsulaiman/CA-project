Phase 1 - Certificate Signing:

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




Email: hasan.alsulaimanaqa@agu.edu.tr
