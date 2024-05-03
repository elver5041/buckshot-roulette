import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR
from dotenv import load_dotenv
import os

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(AF_INET, SOCK_STREAM)
        load_dotenv()
        self.server = os.getenv("SERVER_IP") or "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.active = True
        id = self.connect()
        print(id)

    def connect(self) -> str:
        try:
            self.client.connect(self.addr)
            return self.client.recv(1024).decode()
        except socket.error as e:
            self.active = False
            return str(e)
            
    def disconnect(self) -> None:
        self.client.shutdown(SHUT_RDWR)
        self.active = False

    def send(self, comm) -> None:
        try:
            self.client.send(str.encode(comm))
        except socket.error as e:
            print("server not active, message didn't reach it")
            self.active = False

n = Network()

while n.active:
    if (inp := input()) == "/q":
        n.disconnect()
    else:
        n.send(inp)
    