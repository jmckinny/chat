#!/usr/bin/env python3
import socket
import sys
class Client:
    def __init__(self, address = socket.gethostname(), port = 1247):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.HOST = address
        self.PORT = port
        self.sock.connect((self.HOST, self.PORT))
        print(f"Starting Connection to {self.HOST} on {self.PORT}")

    def send_message(self, msg):
        self.sock.send(msg.encode())
    
    def close(self):
        self.sock.close()
    
c = Client()
c.send_message(sys.argv[1])