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

#helped function to scale image
def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()
    new_image = pygame.transform.scale(image, (width * scale, height * scale))
    return new_image

#Character images
animation_list = []
for i in range(4):
    image = pygame.image.load(f"assets/characters/kebo/idle/{i}.png").convert_alpha()
    image = scale_img(image, const.SCALE)
    animation_list.append(image)

#Create player
kebo = Character(100, 100, animation_list)

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
        dx -= const.SPEED
    if moving_right:
        dx += const.SPEED
    if moving_down:
        dy += const.SPEED
    if moving_up:
        dy -= const.SPEED
    
    #Move player
    kebo.move(dx, dy)
        
    #Update player
    kebo.update()
    
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