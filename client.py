#!/usr/bin/env python3
import socket
import sys
import select
class Client:
    def __init__(self, address = socket.gethostname(), port = 1247):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.HOST = address
        self.PORT = port
        self.sock.connect((self.HOST, self.PORT))
        print(f"Starting Connection to {self.HOST} on {self.PORT}")

    def send_message(self, msg):
        self.sock.send(msg.encode())
    def recv_message(self):
        data = self.sock.recv(1024).decode()
        return data
    def close(self):
        self.sock.close()
    
c = Client()
while True:
    inputs = [sys.stdin, c.sock]
    read_sockets,write_socket, error_socket = select.select(inputs,[],[])
    for socket in read_sockets:
        if socket == c.sock:
            message = c.sock.recv(1024).decode()
            print(message)
        else:
            message = sys.stdin.readline()  
            c.sock.send(message.encode())
            sys.stdout.write("<You>")  
            sys.stdout.write(message)  
            sys.stdout.flush()  