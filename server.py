# https://www.youtube.com/watch?v=qbL4hPWcnFM&list=PLzMcBGfZo4-kR7Rh-7JCVDN8lm3Utumvq&index=3
# https://youtu.be/qbL4hPWcnFM?si=6m96HMcMhVkRRjEg&t=307

import os
from dotenv import load_dotenv
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep
from game import GameSession

load_dotenv()

SERVER = os.getenv("SERVER_IP") or "127.0.0.1"
PORT = 5555

server_active = True

def game_thread(conn) -> None:
    conn.send(str.encode("connected"))
    id = conn.fileno()
    while True: 
        try:
            data = conn.recv(1024)
            reply = data.decode("utf-8")

            if not data:
                print(f"[{id}] disconnected safely")
                break
            print(f"[{id}] said: '{reply}'")
            conn.sendall(str.encode(reply))
        except socket.error as e:
            print(f"[{id}] {str(e)}")
            break
    print(f"[{id}] closed connection")
    conn.close()

def main() -> None:
    s = socket.socket(AF_INET, SOCK_STREAM)
    try:
        s.bind((SERVER, PORT))
    except socket.error as e:
        str(e)
    s.listen(2)
    print("server online")

    conns: list[socket.socket] = []
    while server_active and len(conns)<2:
        conn, addr = s.accept()
        conn.send(str.encode(str(conn.fileno())))
        conns.append(conn)
        
        print(f"[{conn.fileno()}] accepted ip:",addr)
        #Thread(target=game_thread, args=(conn,)).start()
    for connection in conns:
        connection.send("Game found".encode())
    sleep(0.1)
    game = GameSession(conns[0],conns[1])
    print(f"game started between {game.players[0].fileno()} and {game.players[1].fileno()}")
    game.play_round()


mt = Thread(target=main)
mt.daemon = True
mt.start()

while True:
    if input() == "q":
        break