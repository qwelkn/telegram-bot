class Player:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.role = None
        self.is_alive = True 
        self.votes = 0