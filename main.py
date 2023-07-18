import pygame
from rumblet.classes.Pet import Pet


GAME_NAME = "Rumblet"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    pichu = Pet(id=None, template_key="Pichu", level=1, experience=0, nickname="adjustednickname", move_1_key="Splash")
    target_pikachu = Pet(id=None, template_key="Pikachu", level=16, experience=0, nickname="Target Pikachu")

    adjusted_experience = pichu.speed_adjust_experience(1_000_000)
    print(adjusted_experience)
    pichu.give_experience(adjusted_experience)

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
