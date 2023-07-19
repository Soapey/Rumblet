# import pygame


GAME_NAME = "Rumblet"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    from rumblet.classes.Pet import Pet
    from rumblet.classes.PetMove import PetMove

    my_pet = Pet(id=None, player_id=None, species_name="Grasschu", level=1, experience=0, nickname="Grant's Grasschu")

    my_pet_move_1 = PetMove(id=None, pet_id=None, move_key="Splash", current_fuel=10, pet=my_pet)
    my_pet.moves[1] = my_pet_move_1

    my_pet.give_experience(5_000)

    print(f"{my_pet.nickname}'s current attack is {my_pet.current_attack}.")

    target_pet = Pet(id=None, player_id=None, species_name="Grasschu", level=15, experience=0, nickname="Grasschu")
    target_pet.give_level(3)

    my_pet.use_move(1, target_pet)

    print(f"{target_pet.nickname}'s health is now {target_pet.current_health}/{target_pet.health}.")

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
