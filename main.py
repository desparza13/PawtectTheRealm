import pygame
import constants as const 
from character import Character

pygame.init()

#Create game window
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Pawtect the Realm")

#Create clock for mantaining frame rate
clock = pygame.time.Clock()

#Define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#Create player
kebo = Character(100, 100)

#Main game loop
run = True
while run: 
    #Control frame rate
    clock.tick(60)
    
    #Repaint background
    screen.fill(const.BG)
    
    #Calculate player movement
    dx = 0
    dy = 0
    if moving_left:
        dx -= 5
    if moving_right:
        dx += 5
    if moving_down:
        dy += 5
    if moving_up:
        dy -= 5
    
    #Move player
    kebo.move(dx, dy)
        
    #Draw player on the screen
    kebo.draw(screen)
    
    #Event handler
    for event in pygame.event.get():
        #Close game
        if event.type == pygame.QUIT:
            run = False
        #Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("Left")
                moving_left = True
            if event.key == pygame.K_d:
                print("Right")
                moving_right = True
            if event.key == pygame.K_w:
                print("Up")
                moving_up = True
            if event.key == pygame.K_s:
                print("Down")
                moving_down = True
                
        #Keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                print("Left")
                moving_left = False
            if event.key == pygame.K_d:
                print("Right")
                moving_right = False
            if event.key == pygame.K_w:
                print("Up")
                moving_up = False
            if event.key == pygame.K_s:
                print("Down")
                moving_down = False
            
    #Update graphics
    pygame.display.update()
            
pygame.quit()