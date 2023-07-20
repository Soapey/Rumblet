from dataclasses import dataclass


@dataclass
class Lockstone:
    name: str
    sprite_path: str
    base_capture_rate: float
