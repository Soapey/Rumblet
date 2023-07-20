# import pygame
from rumblet.classes.db.SQLiteConnector import initialise_db

from rumblet.classes.player.Player import Player
from rumblet.classes.pet.Pet import Pet
from rumblet.classes.pet.SpeciesList import SpeciesList
from rumblet.classes.move.MoveList import MoveList


GAME_NAME = "Rumblet"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    initialise_db()

    player = Player(id=None, name="Grant", money=999_999)
    player.insert()
    player.give_max_lockstones()

    pet = Pet(obj_id=None, player_id=player.id, species_name=SpeciesList.dewleaf.name, level=1, experience=0, nickname="YEAHHH DAT BOI")
    pet.insert()
    pet.learn(MoveList.hydrostream_rush.name, 1)

    target_pet = Pet(obj_id=None, player_id=None, species_name=SpeciesList.aqualily.name, level=17, experience=0)

    pet.use_move(1, target_pet)

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
