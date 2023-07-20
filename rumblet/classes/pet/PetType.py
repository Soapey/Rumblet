from dataclasses import dataclass


@dataclass
class PetType:
    name: str
    strengths: list
    weaknesses: list
    immunities: list
