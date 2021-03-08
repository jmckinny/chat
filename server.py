#!/usr/bin/env python3
import socket
import os
from threading import *

class Client:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address


class Server:
    def __init__(self, port):
        self.sock = socket.socket()
        self.HOST = socket.gethostname()
        self.PORT = os.environ.get("PORT")
        self.clients = []
        if self.PORT == None:
            self.PORT = 1247
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST,self.PORT))

        print(f"Server \"{self.HOST}\" running on port {self.PORT}" )
    
    def new_client(self,connection,address):
        client = Client(connection,address)
        self.clients.append(client)
        print(f"{address[0]} connected to the server")
        Thread(target = self.client_thread, args=(client,)).start()

    def broadcast(self,message,sender):
        for client in self.clients:
            if client != sender:
                try:
                    client.socket.send(message)
                except:
                    client.socket.close()
                    self.clients.remove(client)
    
    def client_thread(self, client):
        client.socket.send("Welcome to the chatroom".encode())
        while True:
            try:
                
                msg = client.socket.recv(1024).decode()
                if msg:
                    message_to_send = f"<{client.address[0]}> {msg}"
                    print(message_to_send)
                    self.broadcast(message_to_send,client)
                else:
                    print(f"Closing {client.address}")
                    client.socket.close()
                    self.clients.remove(client)
            except:
                continue
   


s = Server(1247)
s.sock.listen(5)
print("Ready and Listening")
while True:
    connection, address = s.sock.accept()
    s.new_client(connection, address)
