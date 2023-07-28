import sys

import pygame

from rumblet.classes.game.Colour import Colour
from rumblet.classes.game.Constants import X_CELLS, Y_CELLS, SCREEN_WIDTH, SCREEN_HEIGHT, \
    FRAME_RATE, WINDOW_TITLE
from rumblet.classes.game.hud.HUDZone import HUDZone
from rumblet.classes.player.Player import Player
from rumblet.classes.zone.Zones import Zones
from rumblet.classes.battle.BattleStatus import BattleStatus


class Game:
    def __init__(
            self,
            x_cells=X_CELLS,
            y_cells=Y_CELLS,
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            frame_rate=FRAME_RATE,
            window_title=WINDOW_TITLE
    ):
        self.x_cells = x_cells
        self.y_cells = y_cells
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x_pixels_per_cell = screen_width // x_cells
        self.y_pixels_per_cell = screen_height // y_cells
        self.clock = None
        self.screen = None
        self.frame_rate = frame_rate
        self.window_title = window_title
        self.player = None
        self.hud_zone = None
        self.battle = None

    def run(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.hud_zone = HUDZone(self.screen, "", Colour.BLACK.value)

        pygame.display.set_caption(self.window_title)

        self.player = Player.create_new_player(
            game=self,
            name="Grant",
            max_money=True,
            max_lockstones=True,
        )

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.battle:
                    mouse_click = event.pos

                    if self.battle.status == BattleStatus.WAITING:
                        if self.battle.buttons["Fight"].collidepoint(mouse_click):
                            self.battle.status = BattleStatus.CHOOSING_MOVE
                        elif self.battle.buttons["Run"].collidepoint(mouse_click):
                            self.battle.end()
                    elif self.battle.status == BattleStatus.CHOOSING_MOVE:
                        if self.battle.buttons["move_1_button"] and self.battle.buttons["move_1_button"].collidepoint(mouse_click):
                            self.battle.player_selected_pet.use_move(1, self.battle.opponent_selected_pet)
                        elif self.battle.buttons["move_2_button"] and self.battle.buttons["move_2_button"].collidepoint(mouse_click):
                            self.battle.player_selected_pet.use_move(2, self.battle.opponent_selected_pet)
                        elif self.battle.buttons["move_3_button"] and self.battle.buttons["move_3_button"].collidepoint(mouse_click):
                            self.battle.player_selected_pet.use_move(3, self.battle.opponent_selected_pet)
                        elif self.battle.buttons["move_4_button"] and self.battle.buttons["move_4_button"].collidepoint(mouse_click):
                            self.battle.player_selected_pet.use_move(4, self.battle.opponent_selected_pet)
                        self.battle.status = BattleStatus.WAITING

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        self.player.right_pressed = True
                    if event.key == pygame.K_UP:
                        self.player.up_pressed = True
                    if event.key == pygame.K_DOWN:
                        self.player.down_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        self.player.right_pressed = False
                    if event.key == pygame.K_UP:
                        self.player.up_pressed = False
                    if event.key == pygame.K_DOWN:
                        self.player.down_pressed = False

            if self.battle is None:
                player_zone = Zones(self).list.get(self.player.current_zone_name)
                player_zone.draw()
            elif self.battle:
                self.battle.draw()

            pygame.display.flip()

            self.clock.tick(self.frame_rate)
