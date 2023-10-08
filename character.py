import math
import pygame
import constants as const

class Character():
    def __init__(self, x, y, animation_list) -> None:
        #probar los mpvimientos con un rectangulo en lo que completamos los sprites
        self.rect = pygame.Rect(0, 0, 40, 40)
        #set character position
        self.rect.center = (x, y)
        
        #animation 
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks() #How much time has passed since the last time we update the frame
        self.image = animation_list[self.frame_index] 

        self.flip = False

        
    def move(self, dx, dy):
        #Check the direction of the character
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
            
        #control diagonal speed
        if dx!= 0 and dy!=0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
            
        self.rect.x += dx
        self.rect.y += dy
        
    def update(self):
        '''Method for handle character animation '''
        animation_cooldown = 90 #speed of the animation
        
        #Handle animation
        #update image
        self.image = self.animation_list[self.frame_index]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1 #move to the next frame
            self.update_time = pygame.time.get_ticks() #reset the timer
            
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0 #reset frame index
        
    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False) #image, flip horizontal, flip vertical
        surface.blit(flipped_image, self.rect) #draw the image
        pygame.draw.rect(surface, const.RED, self.rect, 1) #empty rectangle with the image
        