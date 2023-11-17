import pygame
from pygame import mixer
import csv
import config.constants as const 
from damage_text import DamageText
from dungeon import Dungeon
from garden import Garden
from items import Item
from weapon import Weapon
from world import World
from screenfade import ScreenFade
from button import Button
from boss import Boss
from music_controller import GameEventPublisher, MusicController
from config import game_init, image_init
from ball_atack import BallAtack, BlueBallAtack, OrangeBallAtack, YellowBallAtack

"""
  FUNCTIONS AND VARIABLES FROM CONFIG/GAME_INIT.PY
"""
game_init.init_config()
screen = game_init.window_config()
clock = pygame.time.Clock()
sounds = game_init.load_audio_assets()
font = game_init.define_font()

#define game variables
level = 6
start_game = False
pause_game = False
start_intro = False
game_over = False

#Define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False


#Music controller observer
music_publisher = GameEventPublisher()
music_controller = MusicController()
music_publisher.subscribe(music_controller)

#load button images
restart_image = image_init.scale_img(pygame.image.load("assets/buttons/button_restart.png").convert_alpha(),const.BUTTON_SCALE)
start_image = image_init.scale_img(pygame.image.load("assets/buttons/button_start.png").convert_alpha(),const.BUTTON_SCALE)
exit_image = image_init.scale_img(pygame.image.load("assets/buttons/button_exit.png").convert_alpha(),const.BUTTON_SCALE)
resume_image = image_init.scale_img(pygame.image.load("assets/buttons/button_resume.png").convert_alpha(),const.BUTTON_SCALE)

#Load heart images
heart_empty = image_init.scale_img(pygame.image.load("assets/items/heart_empty.png").convert_alpha(),const.ITEM_SCALE)
heart_half = image_init.scale_img(pygame.image.load("assets/items/heart_half.png").convert_alpha(),const.ITEM_SCALE)
heart_full = image_init.scale_img(pygame.image.load("assets/items/heart_full.png").convert_alpha(),const.ITEM_SCALE)

#Load bone images
bone_images = []
for x in range(4):
    image = pygame.image.load(f"assets/items/bone_f{x}.png").convert_alpha()
    image = image_init.scale_img(image, const.ITEM_SCALE)
    bone_images.append(image)

#Load potion image
red_potion = image_init.scale_img(pygame.image.load("assets/items/potion_red.png").convert_alpha(),const.POTION_SCALE)

item_images = []
item_images.append(bone_images)
item_images.append(red_potion)

#Load weapon images
weapon_image = image_init.scale_img(pygame.image.load("assets/weapons/weapon1.png").convert_alpha(), const.WEAPON_SCALE)
projectile_image = image_init.scale_img(pygame.image.load("assets/weapons/projectile.png").convert_alpha(), const.WEAPON_SCALE)
ballatack1 = BallAtack()

#load tilemap images
tile_list = []
for x in range(const.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/tiles/garden/{x}.png").convert_alpha()
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
            image = image_init.scale_img(image, const.SCALE)
            # TODO: delete this print
            print(f"ADDED: {mob} in {animation} animation, frame {i}")
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
        if kebo.animation.stats.health >= ((i+1)*20): #One full heart = 20 health
            screen.blit(heart_full, (10 + i * 50,0)) 
        elif(kebo.animation.stats.health %20 > 0) and half_hear_drawn == False:
            screen.blit(heart_half, (10 + i * 50,0))
            half_hear_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50,0))

    #level
    draw_text(f"LEVEL: {level}", font, const.WHITE, const.SCREEN_WIDTH/2, 15)
    #show score
    draw_text(f" x {kebo.score}",font, const.WHITE, const.SCREEN_WIDTH - 100, 15)

#Function to reset levels
def reset_level() -> list:
    damage_text_group.empty()
    projectile_group.empty()
    item_group.empty()
    ballattack_group.empty()
    
    #create empty tile list
    w_data = []
    for row in range(const.ROWS):
        r = [-1] * const.COLS
        w_data.append(r)
    
    return w_data

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


world = Garden()
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
ballattack_group = pygame.sprite.Group()

score_bone = Item(const.SCREEN_WIDTH - 115, 26, 0, bone_images, True)
item_group.add(score_bone)
# add the items from the level data
for item in world.item_list:
    item_group.add(item)


# Create screen fade animation
intro_fade = ScreenFade(screen, 1, const.BLACK, 4)
death_fade = ScreenFade(screen, 2, const.PINK, 6)

#create button
restart_button = Button(const.SCREEN_WIDTH //2 -175, const.SCREEN_HEIGHT // 2 - 50, restart_image)
start_button = Button(const.SCREEN_WIDTH //2 -145, const.SCREEN_HEIGHT // 2 - 150, start_image)
exit_button = Button(const.SCREEN_WIDTH //2 -110, const.SCREEN_HEIGHT // 2 + 50, exit_image)
resume_button = Button(const.SCREEN_WIDTH //2 -175, const.SCREEN_HEIGHT // 2 - 150, resume_image)

#Main game loop
run = True
while run: 
    #Control frame rate
    clock.tick(60)
    
    if start_game == False:
        #game menu
        screen.fill(const.MENU_BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game == True:
            pygame.mixer.music.set_volume(0)

            sounds["pause_sound"].play()
            screen.fill(const.MENU_BG)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False
        else:
            #Repaint background
            screen.fill(const.BG)
            
            if kebo.animation.stats.alive:
                sounds["pause_sound"].stop()
                pygame.mixer.music.set_volume(0.3)

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
                screen_scroll, level_complete = kebo.move(dx, dy, world.obstacle_tiles, world.exit_tile)
                
                #UPDATE
                #   player
                kebo.animation.update()
                if kebo.animation.stats.alive == False:
                    sounds["game_over_sound"].play()
                #   projectile
                projectile = weapon.update(kebo)
                if projectile:
                    projectile_group.add(projectile)
                    sounds["shot_sound"].play()
                for projectile in projectile_group:
                    damage, damage_pos = projectile.update(screen_scroll, world.obstacle_tiles, enemy_list)
                    if damage: 
                        damage_text = DamageText(damage_pos.centerx,damage_pos.y,str(damage),const.RED, font)
                        damage_text_group.add(damage_text)
                        sounds["hit_sound"].play()
                    
                #  Update other objects in the world
                for enemy in enemy_list:
                    if isinstance(enemy,Boss):
                        enemy.set_publisher(music_publisher)
                        if enemy.animation.stats.health >=100:
                            colorBallAtack = BlueBallAtack(ballatack1)
                        elif enemy.animation.stats.health >=50:
                            colorBallAtack = OrangeBallAtack(ballatack1)
                        elif enemy.animation.stats.health >=0:
                            colorBallAtack = YellowBallAtack(ballatack1)

                        ballattack_image = image_init.scale_img(pygame.image.load(colorBallAtack.use()).convert_alpha(), const.BALLATTACK_SCALE)
                        ballattack = enemy.ai(kebo, world.obstacle_tiles, screen_scroll, ballattack_image)
                        if ballattack: 
                            ballattack_group.add(ballattack)
                    else:
                        enemy.ai(kebo, world.obstacle_tiles, screen_scroll)
                    # if kebo.hit:
                    #     hurt_sound.play()
                    
                    if enemy.animation.stats.alive:
                        # TODO: add an animation or indicator that the enemy's dead besides stopping its movement
                        enemy.animation.update()
                
                damage_text_group.update(screen_scroll)
                item_group.update(screen_scroll, kebo, sounds["bone_sound"], sounds["heal_sound"])
                ballattack_group.update(screen_scroll, kebo)
                world.update(screen_scroll)   
                
            #DRAW 
            #  tiles on screen (world)
            world.draw(screen)
            #   player on the screen
            kebo.animation.draw(screen)
            #   Weapon on the screen
            weapon.draw(screen)
            
            #   Projectiles on the screen
            for projectile in projectile_group:
                projectile.draw(screen)
            
            #projectile_group.draw(screen)

            #  ballattacks on the screen
            for ballattack in ballattack_group:
                ballattack.draw(screen)
            
            #   enemies on screen
            for enemy in enemy_list:
                if enemy.animation.stats.alive:
                    enemy.animation.draw(screen)

            damage_text_group.draw(screen)
            item_group.draw(screen)
            draw_info()
            score_bone.draw(screen)

            #Check if level is complete
            if level_complete:
                music_publisher.end_boss_fight()
                sounds["level_up_sound"].play()
                start_intro = True
                level += 1
                world_data = reset_level()
                #load in level data and create world
                with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter = ",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = Garden()
                world.process_data(world_data, tile_list, item_images, mob_animations)
                temporary_health = kebo.animation.stats.health
                temporary_score = kebo.score
                kebo = world.player
                kebo.animation.stats.health = temporary_health
                kebo.score = temporary_score
                enemy_list = world.character_list
                score_bone = Item(const.SCREEN_WIDTH - 115, 26, 0, bone_images, True)
                item_group.add(score_bone)
                for item in world.item_list:
                    item_group.add(item)

            #Show intro
            if start_intro:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0
                    
            #Show death screen
            if kebo.animation.stats.alive == False: 
                if death_fade.fade():
                    
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        
                        world_data = reset_level()
                        #load in level data and create world
                        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter = ",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = Garden()
                        world.process_data(world_data, tile_list, item_images, mob_animations)
                        temporary_score = kebo.score
                        kebo = world.player
                        kebo.score = temporary_score
                        enemy_list = world.character_list
                        score_bone = Item(const.SCREEN_WIDTH - 115, 26, 0, bone_images, True)
                        item_group.add(score_bone)
                        for item in world.item_list:
                            item_group.add(item)
                    
            
    #Event handler
    for event in pygame.event.get():
        #Close game
        if event.type == pygame.QUIT:
            run = False
        #Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True
                
        #Keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            
    #Update graphics
    pygame.display.update()
            
pygame.quit()