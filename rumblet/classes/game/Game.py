import pygame
import sys
from rumblet.classes.player.Player import Player
from rumblet.classes.game.Colour import Colour
from rumblet.classes.game.Direction import Direction
from rumblet.classes.zone.ZonesList import ZonesList
from rumblet.classes.game.hud.HUDZone import HUDZone
from rumblet.classes.game.Constants import X_CELLS, Y_CELLS, CELL_WIDTH, CELL_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, WINDOW_TITLE


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

    def set_background(self):
        self.screen.fill(Colour.WHITE.value)

    def draw_cell(self, cell):
        width = CELL_WIDTH
        height = CELL_HEIGHT
        left = cell.grid_cell_x * width
        top = cell.grid_cell_y * height
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

        self.player = Player.create_new_player(
            name="Grant",
            max_money=True,
            max_lockstones=True
        )

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
