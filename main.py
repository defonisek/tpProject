import random

def fightRound2pl():
    while player1.hp>0 or

def fightRound3pl():
    pass
class Player():
    def __init__(self,hp, kz):
        self.hp = hp
        self.kz = kz

    def attak(self):
        if self.kz-random.randint(1,20)>=0:
            self.hp -= random.randint(1,8)

    def defence(self):
        self.kz+=3
    def defenceoff(self):
        self.kz -= 3

    def hill(self):
        pass

class Npc():
    def __init__(self,hp, kz):
        self.hp = hp
        self.kz = kz

    def attak(self):
        if self.kz-random.randint(1,20)>=0:
            self.hp -= random.randint(1,8)

player1 = Player(hp=20, kz=14)
player1.attak()
print(player1.hp)



