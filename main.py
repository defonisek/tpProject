import random

class player():
    def __init__(self,hp, kz):
        self.hp = hp
        self.kz = kz

    def attac(self):
        if self.kz-random.randint(1,20)>=0:
            self.hp -= random.randint(1,8)

player1 = player(hp=20, kz=14)
player1.attac()
print(player1.hp)



