import random
import socket
from threading import Thread
from asyncio import Semaphore

INVENTORY_SPACE = 8
BLANK = '/'
LIVE = '|'

ITEMS = ['MAGNIFYING_GLASS',
    'CIGARETTE_PACK',
    'CAN_OF_BEER',
    'HANDSAW',
    'PAIR_OF_HANDCUFFS',
    'BURNER_PHONE',
    'INVERTER',
    'INJECTION_OF_ADRENALINE',
    'BOX_OF_EXPIRED_MEDICINE']

class Inventory:
    def __init__(self) -> None:
        self.inventory: dict[int:str] = {}

    def get_item(self) -> tuple[str, list[int]]:
        item = random.choice(ITEMS)
        possible_pos = [i for i in range(INVENTORY_SPACE) if i not in self.inventory]
        return (item, possible_pos)

    def place_item(self, i:str, p:int) -> None:
        self.inventory[p] = i

    def use_item(self, p:int) -> str:
        return self.inventory.pop(p)

    def __len__(self) -> int:
        return len(self.inventory)

    def __str__(self) -> str:
        stri = ["╔", "║", "╠", "║", "╚"]
        for i in range(0,INVENTORY_SPACE,2):
            leng = 1
            w1 = " "
            w2 = " "
            if i in self.inventory:
                w1 = self.inventory[i]
                leng = len(w1)
            if i+1 in self.inventory:
                w2 = self.inventory[i+1]
                leng = max(leng, len(w2))
            stri[0] += "═" * leng + "╦"
            stri[1] += w1.center(leng) + "║"
            stri[2] += "═" * leng + "╬"
            stri[3] += w2.center(leng) + "║"
            stri[4] += "═" * leng + "╩"
        stri[0] = stri[0][:-1] + "╗"
        stri[2] = stri[2][:-1] + "╣"
        stri[4] = stri[4][:-1] + "╝"
        return "\n".join(stri)


class Round:
    def __init__(self, r:int, players: tuple[socket.socket,socket.socket]) -> None:
        self.players = players
        self.alive: bool = True
        self.round: int = r
        self.items_per_round: int = min(2*r, 4)
        self.n: int = random.randint(3, 8)
        self.hps: tuple[int, int] = random.randint(3, 8)
        self.inventories: tuple[Inventory,Inventory] = (Inventory(), Inventory())
        self.shells: list[str] = [random.choice([BLANK, LIVE]) for _ in range(self.n)]

        print("".join(self.shells))
        random.shuffle(self.shells)

    def select_items(self, player:socket.socket, items:Inventory, sem:Semaphore):
        n_items = min(self.items_per_round, INVENTORY_SPACE-len(items))
        for i in range(n_items):
            (item, spaces) = items.get_item()
            player.send(f"{item}|{spaces}".encode())
        sem.release()

    async def play_round(self) -> None:
        for i in self.shells:
            threads = []
            sem = Semaphore(2)

            async with sem:
                for player, items in zip(self.players, self.inventories):
                    sem.acquire()
                    threads.append(Thread(target=self.select_items, args=(player,items,sem)))
                sem.acquire(2)

            
                
            for i in range(self.n_items):
                player.get_item()
                
            v = input()
            print(i)

class GameSession:
    def __init__(self, p1:socket.socket, p2:socket.socket) -> None:
        self.r = 0
        self.players = (p1, p2)

    def play_round(self) -> None:
        round = Round(self.r, self.players)
        self.r += 1
        while round.alive:
            round.play_round()
            