import random
from rumblet.classes.game.Colour import Colour
from rumblet.classes.terrain.TerrainName import TerrainName


class GrassCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = Colour.GREEN.value

    @classmethod
    def on_collision(cls, player):
        if random.randint(1, 5) <= 1:
            print(player.zone().get_random_native_pet(terrains=[TerrainName.GRASS.value]))


class WaterCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = Colour.BLUE.value

    @classmethod
    def on_collision(cls, player):
        if random.randint(1, 5) <= 1:
            print(player.zone().get_random_native_pet(terrains=[TerrainName.WATER.value]))
