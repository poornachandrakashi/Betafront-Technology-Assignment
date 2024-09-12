class Pokemon:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.type1 = data.get('type1', '')
        self.type2 = data.get('type2', '')
        self.attack = int(data.get('attack', 0))
        self.defense = int(data.get('defense', 0))