import pygame
import constants as const 
from character import Character

pygame.init()

#Create game window
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Pawtect the Realm")

#Create player
kebo = Character(100, 100)

#Main game loop
run = True
while run: 
    #Draw player on the screen
    kebo.draw(screen)
    
    #Event handler
    for event in pygame.event.get():
        #Close game
        if event.type == pygame.QUIT:
            run = False
            
    #Update graphics
    pygame.display.update()
            
pygame.quit()