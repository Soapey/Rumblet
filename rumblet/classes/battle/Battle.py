import pygame
from rumblet.classes.game.Colour import Colour


class Battle:
    def __init__(self, game, other_party):
        self.ui_font = pygame.font.SysFont("Arial", 16)
        self.ui_font_colour = (0, 0, 0)
        self.game = game
        self.player = game.player
        self.player_party = self.player.party()
        self.other_party = other_party
        self.player_current_pet_party_slot = 1
        self.opponent_current_pet_party_slot = 1
        self.log = list()

    def set_background(self):
        self.game.screen.fill(Colour.WHITE.value)

    def update_health_bars(self):
        player_pet = self.player_party.get(self.player_current_pet_party_slot)
        opponent_pet = self.other_party.get(self.opponent_current_pet_party_slot)

        player_pet_health_bar = self.ui_font.render(f"{player_pet.nickname} HP: {player_pet.current_health} / {player_pet.health}", True, self.ui_font_colour)
        opponent_pet_health_bar = self.ui_font.render(f"{opponent_pet.nickname}: {opponent_pet.current_health} / {opponent_pet.health}", True, self.ui_font_colour)

        self.game.screen.blit(opponent_pet_health_bar, (0, 0))
        self.game.screen.blit(player_pet_health_bar, (0, 50))

    def draw(self):
        self.set_background()
        self.update_health_bars()

    def start(self):
        self.game.battle = self

    def end(self):
        self.game.battle = None



