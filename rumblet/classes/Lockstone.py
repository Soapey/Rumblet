from dataclasses import dataclass


@dataclass
class Lockstone:
    name: str
    sprite_path: str
    level_1_capture_rate: float
