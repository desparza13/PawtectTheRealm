import pygame
import csv
import constants as const 
from character import Character
from damage_text import DamageText
from items import Item
from weapon import Weapon
from world import World

pygame.init()

#Create game window
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Pawtect the Realm")

#Create clock for mantaining frame rate
clock = pygame.time.Clock()

#define game variables
level = 2
scree_scroll = [0, 0]

#Define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#Define font variables
font = pygame.font.Font("font/Minecraftia-Regular.ttf", 20)
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

#Load bone images
bone_images = []
for x in range(4):
    image = pygame.image.load(f"assets/items/bone_f{x}.png").convert_alpha()
    image = scale_img(image, const.ITEM_SCALE)
    bone_images.append(image)

#Load potion image
red_potion = scale_img(pygame.image.load("assets/items/potion_red.png").convert_alpha(),const.POTION_SCALE)

item_images = []
item_images.append(bone_images)
item_images.append(red_potion)

#Load weapon images
weapon_image = scale_img(pygame.image.load("assets/weapons/weapon1.png").convert_alpha(),const.WEAPON_SCALE)
projectile_image = scale_img(pygame.image.load("assets/weapons/projectile.png").convert_alpha(),const.WEAPON_SCALE)

#load tilemap images
tile_list = []
for x in range(const.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (const.TILE_SIZE, const.TILE_SIZE))
    tile_list.append(tile_image)

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

#Function for outputtong text onto the screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y))
   
#Function for displaying game info (top bar)
def draw_info():
    #Draw the rect of the panel
    pygame.draw.rect(screen, const.PANEL_INFO, (0,0,const.SCREEN_WIDTH,50))
    pygame.draw.line(screen,const.WHITE,(0,50), (const.SCREEN_WIDTH,50)) #separate the panel info and the screen game
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

    #level
    draw_text(f"LEVEL: {level}", font, const.WHITE, const.SCREEN_WIDTH/2, 15)
    #show score
    draw_text(f" x {kebo.score}",font, const.WHITE, const.SCREEN_WIDTH - 100, 15)


#create empty tile list
world_data = []
for row in range(const.ROWS):
    r = [-1] * const.COLS
    world_data.append(r)
#load in level data and create world
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

#Create player and enemies
kebo = world.player

#Create player's weapon
weapon = Weapon(weapon_image, projectile_image)

#extrat enemies from world data
enemy_list = world.character_list

#Create sprite groups
damage_text_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_bone = Item(const.SCREEN_WIDTH - 115, 26, 0, bone_images, True)
item_group.add(score_bone)
# add the items from the level data
for item in world.item_list:
    item_group.add(item)




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
    screen_scroll = kebo.move(dx, dy, world.obstacle_tiles)
        
    #UPDATE 
    #   player
    kebo.update()
    
    #   projectile
    projectile = weapon.update(kebo)
    if projectile:
        projectile_group.add(projectile)
    
    for projectile in projectile_group:
        damage, damage_pos = projectile.update(screen_scroll, world.obstacle_tiles, enemy_list)
        if damage: 
            damage_text = DamageText(damage_pos.centerx,damage_pos.y,str(damage),const.RED, font)
            damage_text_group.add(damage_text)
        
    #  Update other objects in the world
    for enemy in enemy_list:
        enemy.ai(kebo, world.obstacle_tiles, screen_scroll)
        enemy.update()
    
    damage_text_group.update(screen_scroll)
    item_group.update(screen_scroll, kebo)

    world.update(screen_scroll)    
    #DRAW 
    #  tiles on screen (world)
    world.draw(screen)
    
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
    item_group.draw(screen)
    draw_info()
    score_bone.draw(screen)
    
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