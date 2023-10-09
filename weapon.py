import pygame
import math

class Weapon():
    def __init__(self,image) -> None:
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        
        self.rect = self.image.get_rect()
        
    def update(self, player):
        self.rect.center = player.rect.center
        
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery) # negative because pygame y coordinates increase down the screen
        
        #Calculate the angle for the weapon based in the mouse
        self.angle = math.degrees(math.atan2(y_dist,x_dist))
        
    def draw(self,surface):
        self.image =pygame.transform.rotate(self.original_image,self.angle)
        #Draw the weapon around the player/rectangle
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
        