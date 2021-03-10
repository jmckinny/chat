#!/usr/bin/env python3
import socket
import sys
import select
import threading
class Client:
    def __init__(self, address = socket.gethostname(), port = 1247):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.HOST = address
        self.PORT = port
        self.sock.connect((self.HOST, self.PORT))
        print(f"Starting Connection to {self.HOST} on {self.PORT}")

    def send_message(self, msg):
        self.sock.send(msg.encode())
    
    def start_listening(self):
        threading.Thread(target=self.listen).start()
    
    def listen(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                if msg:
                    print(msg)
            except:
                continue
    def close(self):
        self.sock.close()
    
c = Client()
c.start_listening()
while True:
    msg = input(">")
    c.send_message(msg)
