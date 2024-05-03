import random

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
    def __init__(self, r:int) -> None:
        self.alive: bool = True
        self.round: int = r
        self.items_per_round: int = min(2*r, 4)
        self.n: int = random.randint(3, 8)
        self.items: tuple[Inventory,Inventory] = (Inventory(), Inventory())
        self.shells: list[str] = [random.choice([BLANK, LIVE]) for _ in range(self.n)]

        print("".join(self.shells))
        random.shuffle(self.shells)

    def play_round(self) -> None:
        for i in self.shells:
            n_items = min(self.items_per_round, 8-len(self.items[0]))
            for i in range(n_items):
                yield NotImplementedError
            v = input()
            print(i)

class GameSession:
    def __init__(self) -> None:
        self.r = 0

    def play_round(self) -> None:
        lol = Round(self.r)
        self.r += 1
        yield NotImplementedError