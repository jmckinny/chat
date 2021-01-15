#!/usr/bin/env python3
import socket
import os
from threading import *

class Server:
    def __init__(self, port):
        self.sock = socket.socket()
        self.HOST = socket.gethostname()
        self.PORT = os.environ.get("PORT")
        if self.PORT == None:
            self.PORT = 1247
        self.sock.bind((self.HOST,self.PORT))
        print(f"Server \"{self.HOST}\" running on port {self.PORT}" )
    
    def new_client(self, socket, address):
        Handler(socket, address)
        

class Handler(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.start()

    def run(self):
        print('Client sent:', self.socket.recv(1024).decode())


s = Server(1247)
s.sock.listen(5)
print("Ready and Listening")
while True:
    clientsocket, address = s.sock.accept()
    s.new_client(clientsocket, address)
