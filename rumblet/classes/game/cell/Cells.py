import random
from abc import ABC

from rumblet.classes.game.Colour import Colour
from rumblet.classes.terrain.TerrainName import TerrainName


class Cell(ABC):
    def __init__(self, grid_cell_x, grid_cell_y, colour):
        self.grid_cell_x = grid_cell_x
        self.grid_cell_y = grid_cell_y
        self.colour = colour


class GrassCell(Cell):
    def __init__(self, grid_cell_x, grid_cell_y):
        super().__init__(grid_cell_x, grid_cell_y, Colour.GREEN.value)

    @classmethod
    def on_collision(cls, player):
        if random.randint(1, 5) <= 1:
            print(player.zone().get_random_native_pet(terrains=[TerrainName.GRASS.value]))


class WaterCell(Cell):
    def __init__(self, grid_cell_x, grid_cell_y):
        super().__init__(grid_cell_x, grid_cell_y, Colour.BLUE.value)

    @classmethod
    def on_collision(cls, player):
        if random.randint(1, 5) <= 1:
            print(player.zone().get_random_native_pet(terrains=[TerrainName.WATER.value]))
