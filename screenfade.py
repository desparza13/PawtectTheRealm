import pygame
import constants as const

class ScreenFade():
    def __init__(self, screen, direction, color, speed) -> None:
        self.screen = screen
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self) -> bool:
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(self.screen, self.color, (0 - self.fade_counter, 0, const.SCREEN_WIDTH//2, const.SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, self.color, (const.SCREEN_WIDTH//2 + self.fade_counter, 0, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, self.color, (0, 0 - self.fade_counter, const.SCREEN_WIDTH, const.SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, self.color, (0, const.SCREEN_HEIGHT//2 + self.fade_counter, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        elif self.direction== 2: #vertical screen fade down
            pygame.draw.rect(self.screen, self.color, (0, 0, const.SCREEN_WIDTH,0 + self.fade_counter))
        if self.fade_counter >= const.SCREEN_WIDTH:
            fade_complete = True

        return fade_complete