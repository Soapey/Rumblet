import pygame


class HUDZone:
    def __init__(self, screen, text, text_colour):
        self.screen = screen
        self.text = text
        self.colour = text_colour
        self.font = pygame.font.SysFont("Arial", 16)
        self.update_text(text)

    def update_text(self, new_text):
        img = self.font.render(new_text, True, self.colour)
        self.screen.blit(img, (0, 0))
        self.text = new_text
