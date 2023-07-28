import random
from abc import ABC

import pygame

from rumblet.classes.battle.Battle import Battle
from rumblet.classes.game.Colour import Colour
from rumblet.classes.game.Constants import CELL_WIDTH, CELL_HEIGHT
from rumblet.classes.terrain.TerrainName import TerrainName


class Cell(ABC):
    def __init__(self, game, grid_cell_x, grid_cell_y, colour):
        self.game = game
        self.grid_cell_x = grid_cell_x
        self.grid_cell_y = grid_cell_y
        self.colour = colour

    def draw(self):
        left = self.grid_cell_x * CELL_WIDTH
        top = self.grid_cell_y * CELL_HEIGHT
        rect = pygame.Rect(
            left,
            top,
            CELL_WIDTH,
            CELL_HEIGHT
        )
        pygame.draw.rect(self.game.screen, self.colour, rect)


class GrassCell(Cell):
    def __init__(self, game, grid_cell_x, grid_cell_y):
        super().__init__(game, grid_cell_x, grid_cell_y, Colour.GREEN.value)

    def on_collision(self, player, zone):
        if random.randint(1, 5) <= 1:
            opponent_pet = zone.get_random_native_pet(terrains=[TerrainName.GRASS.value])
            opponent_party = {
                1: opponent_pet,
                2: None,
                3: None,
                4: None
            }
            battle = Battle(self.game, opponent_party, f"A wild {opponent_pet.species.name} appeared!")
            battle.start()


class WaterCell(Cell):
    def __init__(self, game, grid_cell_x, grid_cell_y):
        super().__init__(game, grid_cell_x, grid_cell_y, Colour.BLUE.value)

    def on_collision(self, player, zone):
        if random.randint(1, 5) <= 1:
            opponent_pet = zone.get_random_native_pet(terrains=[TerrainName.WATER.value])
            opponent_party = {
                1: opponent_pet,
                2: None,
                3: None,
                4: None
            }
            battle = Battle(self.game, opponent_party, f"A wild {opponent_pet.species.name} appeared!")
            battle.start()
