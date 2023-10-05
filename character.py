import pygame
import constants

class Character():
    def __init__(self, x, y) -> None:
        #probar los mpvimientos con un rectangulo en lo que completamos los sprites
        self.rect = pygame.Rect(0, 0, 40, 40)
        #set character position
        self.rect.center = (x, y)
        
    def draw(self, surface):
        pygame.draw.rect(surface, constants.RED, self.rect)
        