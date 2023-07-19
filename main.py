# import pygame
from rumblet.classes.db.SQLiteConnector import initialise_db

from rumblet.classes.player.Player import Player
from rumblet.classes.Pet import Pet


GAME_NAME = "Rumblet"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    initialise_db()

    player = Player(id=None, name="Grant", money=999_999)
    player.insert()
    player.give_max_lockstones()

    pet = Pet(id=None, player_id=player.id, species_name="Grasschu", level=1, experience=0, nickname="custom_nickname")
    pet.insert()
    pet.learn("Splash", 1)

    target_pet = Pet(id=None, player_id=None, species_name="Grasskachu", level=17, experience=0)

    lockstone = player.get_lockstone_by_name(lockstone_name="Basic Lockstone")
    target_pet.attempt_catch(player=player, lockstone=lockstone)

    # pygame.init()
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption(GAME_NAME)
    #
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     pygame.display.flip()
    # pygame.quit()


if __name__ == '__main__':
    main()
