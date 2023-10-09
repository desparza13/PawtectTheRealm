import pygame
import constants as const 
from character import Character
from damage_text import DamageText
from weapon import Weapon
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

#Define font variables
font = pygame.font.SysFont("timesnewroman",20)
#print(pygame.font.get_fonts())

#helped function to scale image
def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()
    new_image = pygame.transform.scale(image, (width * scale, height * scale))
    return new_image

#Load heart images
heart_empty = scale_img(pygame.image.load("assets/items/heart_empty.png").convert_alpha(),const.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/items/heart_half.png").convert_alpha(),const.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/items/heart_full.png").convert_alpha(),const.ITEM_SCALE)

#Load weapon images
weapon_image = scale_img(pygame.image.load("assets/weapons/weapon1.png").convert_alpha(),const.WEAPON_SCALE)
projectile_image = scale_img(pygame.image.load("assets/weapons/projectile.png").convert_alpha(),const.WEAPON_SCALE)

#Load characters images
animation_types = ["idle", "run"]
mob_types = ["kebo","black_cat", "brown_cat","orange_cat", "budgie", "budgie2", "big_demon"]

mob_animations = []

for mob in mob_types:
    #load character images
    animation_list = []
    for animation in animation_types:
        #reset temporary list of images
        temp_list = []
        for i in range(4):
            image = pygame.image.load(f"assets/characters/{mob}/{animation}/{i}.png").convert_alpha()
            image = scale_img(image, const.SCALE)
            temp_list.append(image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)
    
#Function for displaying game info
def draw_info():
    pygame.draw.rect(screen, const.PANEL_INFO, (0,0,const.SCREEN_WIDTH,50))
    pygame.draw.line(screen,const.WHITE,(0,50), (const.SCREEN_WIDTH,50))
    #draw lives
    half_hear_drawn = False
    for i in range(5):
        if kebo.health >= ((i+1)*20): #One full heart = 20 health
            screen.blit(heart_full, (10 + i * 50,0))
        elif(kebo.health %20 > 0) and half_hear_drawn == False:
            screen.blit(heart_half, (10 + i * 50,0))
            half_hear_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50,0))
            

#Create player
kebo = Character(100, 100, 10, mob_animations,0)

#Create enemy
enemy = Character(200, 300, 100, mob_animations,1)

#Create player's weapon
weapon = Weapon(weapon_image, projectile_image)

#Create empty enemy list 
enemy_list = []
enemy_list.append(enemy)

#Create sprite groups
damage_text_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()


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
        
    #Update 
    #   player
    kebo.update()
    
    #   projectile
    projectile = weapon.update(kebo)
    if projectile:
        projectile_group.add(projectile)
    
    for projectile in projectile_group:
        damage, damage_pos = projectile.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx,damage_pos.y,str(damage),const.RED, font)
            damage_text_group.add(damage_text)
        
    #   enemies
    for enemy in enemy_list:
        enemy.update()
    
    damage_text_group.update()
    
    #Draw 
    #   player on the screen
    kebo.draw(screen)
    
    #   Weapon on the screen
    weapon.draw(screen)
    
    #   Projectiles on the screen
    for projectile in projectile_group:
        projectile.draw(screen)
    
    projectile_group.draw(screen)

    #   enemies on screen
    for enemy in enemy_list:
        enemy.draw(screen)
    
    damage_text_group.draw(screen)
    draw_info()
    
    #Event handler
    for event in pygame.event.get():
        #Close game
        if event.type == pygame.QUIT:
            run = False
        #Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                # print("Left")
                moving_left = True
            if event.key == pygame.K_d:
                # print("Right")
                moving_right = True
            if event.key == pygame.K_w:
                # print("Up")
                moving_up = True
            if event.key == pygame.K_s:
                # print("Down")
                moving_down = True
                
        #Keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                # print("Left")
                moving_left = False
            if event.key == pygame.K_d:
                # print("Right")
                moving_right = False
            if event.key == pygame.K_w:
                # print("Up")
                moving_up = False
            if event.key == pygame.K_s:
                # print("Down")
                moving_down = False
            
    #Update graphics
    pygame.display.update()
            
pygame.quit()