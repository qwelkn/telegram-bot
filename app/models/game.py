from app.config.const import ROLE
from random import random
from players import Player
from copy import deepcopy

class Game:
    def __init__(self, id_chat):
        self.id_chat = id_chat
        self.players = []
        self.phase = "night"

    def random_role(self):
        roles = deepcopy(ROLE[len(self.players)])
        for player in self.players:
            role = random.choice(roles)
            player.role = role 
            roles.remove(role)

a = Game(1)
a.random_role()