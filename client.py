#!/usr/bin/env python3
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 1247

s.connect((HOST,PORT))
print(f"Starting Connection to {HOST} on {PORT}")

def send_message(msg):
    s.send(msg.encode())

send_message("Hello Server!")