from socket import socket, AF_INET, SOCK_STREAM
from dotenv import load_dotenv
import os

class Network:
    def __init__(self) -> None:
        self.client = socket(AF_INET, SOCK_STREAM)
        load_dotenv()
        self.server = os.getenv("SERVER_IP") or "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self) -> None:
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.err as e:
            str(e)