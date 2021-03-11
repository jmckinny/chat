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

    def __str__(self):
        return f"{self.name}@{self.address[0]}"

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
        self.commands = {"nick": self.nick_command, "who": self.who_command, "msg": self.msg_command}
        self.motd = "Welcome to the chat room"
        print(f"Server \"{self.HOST}\" running on port {self.PORT}" )
    
    def new_client(self,connection,address):
        client = Client(connection,address)
        self.clients.append(client)
        print(f"{client}:{client.address[1]} connected to the server")
        join_msg = f"{client} connected to the server"
        self.broadcast(join_msg.encode(),client)
        Thread(target = self.client_thread, args=(client,)).start()

    def broadcast(self,message,sender = None):
        for client in self.clients:
            if client != sender:
                try:
                    client.socket.send(message)
                except:
                    client.socket.close()
                    self.clients.remove(client)
    
    def client_thread(self, client):
        client.socket.send(self.motd.encode())
        while True:
            try:
                msg = client.socket.recv(1024).decode()
                if msg:
                    if msg[0] == "/":
                        print(f"[{client}] Command: " + msg )
                        self.command_handler(client,msg)
                    else:
                        message_to_send = f"<{client}> {msg}"
                        print(message_to_send)
                        self.broadcast(message_to_send.encode(),client)
                else:
                    print(f"Closing {client}:{client.address[1]}")
                    client.socket.close()
                    self.clients.remove(client)
            except:
                continue
    
    def get_client(self,name):
        for client in self.clients:
            if client.name == name:
                return client
        return None


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
        if self.get_client(new_name) != None:
            client.socket.send("That name is already taken".encode())
        else:
            self.broadcast(f"{client.name} is now known as {new_name}".encode(),client)
            client.name = new_name
            

    def who_command(self,client,args):
        result = f"There are {len(self.clients)} users online:\n"
        for c in self.clients:
            result += f"{c.name}@{c.address[0]}\n"
        client.socket.send(result.encode())

    def msg_command(self,client,args):
        name = re.sub(r"\W+", "", args[0].strip())
        msg = re.sub(r"\W+", "", args[1].strip())
        reciever = self.get_client(name)
        print(reciever)
        if reciever != None:
            reciever.socket.send(f"[{client}]: {msg}".encode())
        else:
            client.socket.send(f"User {name} does not exist".encode())




s = Server(1247)
s.sock.listen(5)
print("Ready and Listening")
while True:
    connection, address = s.sock.accept()
    s.new_client(connection, address)
