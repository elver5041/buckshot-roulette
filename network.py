import socket
from socket import AF_INET, SOCK_STREAM
from dotenv import load_dotenv
import os

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(AF_INET, SOCK_STREAM)
        load_dotenv()
        self.server = os.getenv("SERVER_IP") or "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        id = self.connect()
        print(id)
    def connect(self) -> str:
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            str(e)

n = Network()