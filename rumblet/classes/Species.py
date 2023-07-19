from dataclasses import dataclass
from rumblet.classes.PetType import PetType


@dataclass
class Species:
    dex_no: int
    name: str
    sprite_path: str
    type: PetType
    health: int
    defense: int
    attack: int
    speed: int
    end_health: int
    end_defense: int
    end_attack: int
    end_speed: int
    leveling_speed: int
    previous_evolution_name: str
    evolution_name: str
    evolution_level: int
