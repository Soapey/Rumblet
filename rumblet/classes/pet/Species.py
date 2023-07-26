class Species:
    def __init__(self, dex_no, name, sprite_path, type, health, defense, attack, speed, end_health, end_defense, end_attack, end_speed, leveling_speed, previous_evolution_name, evolution_name, evolution_level, learnable_moves, terrains):
        self.dex_no = dex_no
        self.name = name
        self.sprite_path = sprite_path
        self.type = type
        self.health = health
        self.defense = defense
        self.attack = attack
        self.speed = speed
        self.end_health = end_health
        self.end_defense = end_defense
        self.end_attack = end_attack
        self.end_speed = end_speed
        self.leveling_speed = leveling_speed
        self.previous_evolution_name = previous_evolution_name
        self.evolution_name = evolution_name
        self.evolution_level = evolution_level
        self.learnable_moves = learnable_moves
        self.terrains = terrains
