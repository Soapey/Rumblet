from math import floor

import pygame

from rumblet.classes.game.Colour import Colour
from rumblet.classes.battle.BattleStatus import BattleStatus
from rumblet.classes.game.Constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Battle:
    def __init__(self, game, other_party, starting_message):
        self.buttons = dict()
        self.menu_border = 10
        self.menu_height = 400
        self.menu_width = SCREEN_WIDTH - (self.menu_border * 2)
        self.ui_font = pygame.font.SysFont("Arial", 16)
        self.ui_font_colour = (0, 0, 0)
        self.game = game

        self.player_current_pet_party_slot = 1
        self.opponent_current_pet_party_slot = 1

        self.player = game.player
        self.player_party = self.player.party()
        self.player_selected_pet = self.player_party.get(self.player_current_pet_party_slot)

        self.other_party = other_party
        self.opponent_selected_pet = self.other_party.get(1)

        self.status = BattleStatus.WAITING
        self.buttons = dict()

    def draw_waiting_menu(self):
        fight_button = self.create_button("Fight", self.menu_border, SCREEN_HEIGHT-self.menu_border-self.menu_height, self.menu_width//2, self.menu_height//2)
        run_button = self.create_button("Run", self.menu_border+(self.menu_width//2), SCREEN_HEIGHT-self.menu_border-self.menu_height, self.menu_width//2, self.menu_height//2)

        self.buttons["Fight"] = fight_button
        self.buttons["Run"] = run_button

    def draw_move_choice_menu(self):
        move_1_button = self.create_button(
            text=self.player_selected_pet.move_1_name,
            x=self.menu_border,
            y=SCREEN_HEIGHT-self.menu_border-self.menu_height,
            width=self.menu_width//2,
            height=self.menu_height//2
        ) if self.player_selected_pet.move_1_name else None

        move_2_button = self.create_button(
            text=self.player_selected_pet.move_2_name,
            x=self.menu_border+(self.menu_width//2),
            y=SCREEN_HEIGHT-self.menu_border-self.menu_height,
            width=self.menu_width//2,
            height=self.menu_height//2
        ) if self.player_selected_pet.move_2_name else None

        move_3_button = self.create_button(
            text=self.player_selected_pet.move_3_name,
            x=self.menu_border,
            y=SCREEN_HEIGHT-(self.menu_border+self.menu_height)+(self.menu_height//2),
            width=self.menu_width//2,
            height=self.menu_height//2
        ) if self.player_selected_pet.move_3_name else None

        move_4_button = self.create_button(
            text=self.player_selected_pet.move_4_name,
            x=self.menu_border+(self.menu_width//2),
            y=SCREEN_HEIGHT-(self.menu_border+self.menu_height)+(self.menu_height//2),
            width=self.menu_width//2,
            height=self.menu_height//2
        ) if self.player_selected_pet.move_4_name else None

        print(move_1_button, move_2_button, move_3_button, move_4_button, sep="||")

        self.buttons["move_1_button"] = move_1_button
        self.buttons["move_2_button"] = move_2_button
        self.buttons["move_3_button"] = move_3_button
        self.buttons["move_4_button"] = move_4_button

    def create_button(self, text, x, y, width, height, font_colour=Colour.BLACK.value, colour=Colour.WHITE.value, highlight_colour=Colour.BLUE.value):
        mouse_cursor = pygame.mouse.get_pos()

        button = pygame.Rect(x, y, width, height)

        if button.collidepoint(mouse_cursor):
            pygame.draw.rect(self.game.screen, highlight_colour, button)
        else:
            pygame.draw.rect(self.game.screen, colour, button)

        text = self.ui_font.render(text, True, font_colour)
        text_rect = text.get_rect(center=(x+(width//2), y+(height//2)))
        self.game.screen.blit(text, text_rect)

        return button

    def draw_health_bar(self, width, height, x, y, pet):
        current_rect_width = floor(width * (pet.current_health / pet.health))
        current_rect = pygame.Rect(x, y, current_rect_width, height)
        current_rect_colour = Colour.GREEN.value

        max_rect = pygame.Rect(x, y, width, height)
        max_rect_colour = Colour.RED.value

        pygame.draw.rect(self.game.screen, max_rect_colour, max_rect)
        pygame.draw.rect(self.game.screen, current_rect_colour, current_rect)

        hp_text = self.ui_font.render(f"{pet.nickname} HP: {pet.current_health} / {pet.health}", True, Colour.BLACK.value)
        self.game.screen.blit(hp_text, (x, y + height + 5))

    def set_background(self):
        self.game.screen.fill(Colour.WHITE.value)

    def draw_health_bars(self):
        self.draw_health_bar(200, 30, 0, 0, self.opponent_selected_pet)
        self.draw_health_bar(200, 30, 0, 60, self.player_selected_pet)

    def draw(self):
        self.set_background()
        self.draw_health_bars()

        if self.status == BattleStatus.WAITING:
            self.draw_waiting_menu()
        elif self.status == BattleStatus.CHOOSING_MOVE:
            self.draw_move_choice_menu()

    def start(self):
        self.game.battle = self

    def end(self):
        self.game.battle = None



