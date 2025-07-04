from app.config.const import ROLE
import random
from app.models.players import Player
from copy import deepcopy

class Game:
    def __init__(self, id_chat, player):
        self.id_chat = id_chat
        self.players = player
        self.phase = "night"

    def random_role(self):
        roles = deepcopy(ROLE[len(self.players)])
        for player in self.players:
            role = random.choice(roles)
            player.role = role 
            roles.remove(role)

    def kill(self, player: Player):
        mafia_count = 0

        for player in self.players:
            if player.role == "мафія":
                mafia_count += 1

        for player in self.players:
            if player.votes >= mafia_count * 0.5:
                player.is_alive = False
                
        self.log.append(f"Цієї ночі був вбити {player.name}")
        return "Мафія зробила свій хід. Хтось помре"
    
    def heal(self, player: Player, doctor: Player):
        if doctor.role == "лікар":
            if not player.is_alive:
                player.is_alive = True
                self.log.append(f"Цієї ночі лікар врятував {player.name}")
            elif player.is_alive:
                self.log.append("Цієї ночі аптечка лікаря не знадобилась")
            return "Лікар виїхав на чергування"
            
        elif doctor.role != "лікар" or not doctor.is_alive:
            return "Ви не можете лікувати"

# a = Game(1)
# a.random_role()