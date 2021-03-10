#!/usr/bin/env python3
import socket
import re
import os
from threading import *

class Client:
    def __init__(self, socket, address, name = "anon"):
        self.name = name
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
        self.commands = {"nick": self.nick_command}

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
                    if msg[0] == "/":
                        print("Command: " + msg )
                        self.command_handler(client,msg)
                    else:
                        message_to_send = f"<{client.name}@{client.address[0]}> {msg}"
                        print(message_to_send)
                        self.broadcast(message_to_send.encode(),client)
                else:
                    print(f"Closing {client.address}")
                    client.socket.close()
                    self.clients.remove(client)
            except:
                continue

    def command_handler(self,client,msg):
        data = msg[1:].split(" ")
        command = data[0]
        args = data[1:]
        func = self.commands[command]
        func(client,args)


    def nick_command(self,client,args):
        new_name = re.sub(r"\W+", "", args[0].strip())
        if len(new_name) > 9:
            client.socket.send("Name must be 9 chars or less".encode())
        else:
            client.name = new_name
        




s = Server(1247)
s.sock.listen(5)
print("Ready and Listening")
while True:
    connection, address = s.sock.accept()
    s.new_client(connection, address)
