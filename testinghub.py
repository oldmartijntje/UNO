import random

class player():
    def __init__(self, age, name) -> None:
        self.age = age
        self.name = name

amount_players = 10
players = list()
for i in range(amount_players):
    players.append(player(age=random.randrange(1, 99), # Makes random age between 1 and 99
                          name=''.join(random.choice([chr(i) for i in range(ord('a'),ord('z'))]) for _ in range(10)))) # Makes random string of lenght 10

for player in players:
    print(f"{player.name} is {player.age} years old")