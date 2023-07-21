import pygame
import sys
from rumblet.classes.player.Player import Player
from rumblet.classes.game.Colour import Colour
from rumblet.classes.game.Direction import Direction
from rumblet.classes.zone.ZonesList import ZonesList
from rumblet.classes.game.hud.HUDZone import HUDZone


class Game:
    def __init__(self, x_cells=20, y_cells=20, screen_width=1000, screen_height=1000, frame_rate=120, window_title="Rumblet"):
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

    def set_background(self):
        self.screen.fill(Colour.WHITE.value)

    def draw_cell(self, cell):
        left = cell.x * self.x_pixels_per_cell
        top = cell.y * self.y_pixels_per_cell
        width = self.x_pixels_per_cell
        height = self.y_pixels_per_cell
        rect = pygame.Rect(
            left,
            top,
            width,
            height
        )
        pygame.draw.rect(self.screen, cell.colour, rect)

    def draw_zone(self, zone):
        self.set_background()
        for cell in zone.area:
            self.draw_cell(cell)
        self.player.draw(self.screen)
        self.player.update_loc(self.screen_width, self.screen_height)

    def change_zone(self, direction: Direction):
        current_zone = self.player.zone()

        next_zone_name = getattr(current_zone, f"zone_{direction.value.lower()}_name")

        if not next_zone_name:
            return

        next_zone = ZonesList.zones.get(next_zone_name)

        self.draw_zone(next_zone)

    def run(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.hud_zone = HUDZone(self.screen, "", Colour.BLACK.value)

        pygame.display.set_caption(self.window_title)

        self.player = Player(
            id=None,
            name="Grant",
            current_zone_name=ZonesList.brawley_lower.name,
            money=999_999,
            x=150,
            y=150,
            width=self.x_pixels_per_cell,
            height=self.y_pixels_per_cell,
            colour=(133, 80, 255)
        )
        self.player.insert()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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

            self.draw_zone(self.player.zone())
            self.hud_zone.update_text(self.player.zone().name)

            pygame.display.flip()

            self.clock.tick(self.frame_rate)
