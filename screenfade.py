import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MIDDLE_HEIGHT, MIDDLE_WIDTH

class ScreenFade:
    """
    ScreenFade is a class that handles the screen fade effect for the game.
    This action takes place when every new level starts.

    Attributes:
        screen (pygame.Surface): The game window.
        direction (int): The direction of the fade effect.
        color (tuple): The color of the fade effect.
        speed (int): The speed of the fade effect.
        fade_counter (int): The counter for the fade effect.
    """
    def __init__(self, screen, direction, color, speed) -> None:
        """
        Initializes the ScreenFade object.
        """
        self.screen = screen
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self) -> bool:
        """
        Handles the screen fade effect based on the specified direction.
        """
        self.fade_counter += self.speed
        fade_complete = False

        if self.direction == 1:
            fade_complete = self.fade_diagonal()
        elif self.direction == 2:
            fade_complete = self.fade_vertical()

        return fade_complete

    def fade_diagonal(self) -> bool:
        """
        Handles a diagonal fade effect by drawing four rectangles expanding outward from the center.
        """
        left_x = 0 - self.fade_counter
        right_x = MIDDLE_WIDTH + self.fade_counter
        top_y = 0 - self.fade_counter
        bottom_y = MIDDLE_HEIGHT + self.fade_counter

        # Draw the four rectangles
        pygame.draw.rect(self.screen, self.color, (left_x, 0, MIDDLE_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, self.color, (right_x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, self.color, (0, top_y, SCREEN_WIDTH, MIDDLE_HEIGHT))
        pygame.draw.rect(self.screen, self.color, (0, bottom_y, SCREEN_WIDTH, SCREEN_HEIGHT))

        return self.fade_counter >= SCREEN_WIDTH

    def fade_vertical(self) -> bool:
        """
        Handles a vertical fade effect in a single rectangle drawn on the screen.
        """
        pygame.draw.rect(self.screen, self.color, (0, 0, SCREEN_WIDTH, self.fade_counter))
        return self.fade_counter >= SCREEN_HEIGHT
