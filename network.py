import socket
from threading import Thread
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR
from dotenv import load_dotenv
import os
from signal import signal, SIGINT

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(AF_INET, SOCK_STREAM)
        load_dotenv()
        self.server = os.getenv("SERVER_IP") or "127.0.0.1"
        self.port = 5555
        self.active = True
        self.connected = False
        id = 0
        id = int(self.connect())
        print(f"Welcome, user [{id}]")

    def connect(self) -> str:
        try:
            self.client.connect((self.server, self.port))
            return self.client.recv(1024).decode()
        except socket.error as e:
            print(f"server gave: {e}")
            exit(-1)
            
    def disconnect(self) -> None:
        self.client.shutdown(SHUT_RDWR)
        self.active = False

    def send(self, txt:str) -> None:
        try:
            self.client.send(str.encode(txt))
        except socket.error:
            print("server not active, message didn't reach it")
            self.active = False

    def recive(self) -> str:
        return self.client.recv(2048).decode()

n = Network()

def playing_game(n: Network):
    print(n.recive())
    print(n.recive())
    print(n.recive())
    n.connected = True
    state = "items"
    while True:
        if state == "items":
            item,pos = n.recive().split("|")
            pos = eval(pos)
            print(item, pos)
            txt = "select one of the positions above to place the item in: "
            while int(a:=input(txt)) not in pos: pass
            n.send(input())
            print(n.recive())

def closing_func() -> None:
    n.disconnect()

def main() -> None:
    
    signal(SIGINT,closing_func)
    playing_game(n)

if __name__ == "__main__":
    main()