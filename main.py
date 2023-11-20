import pygame
import config.constants as const 
from damage_text import DamageText
from weapon import Weapon
from boss import Boss
from music_controller import GameEventPublisher, MusicController
from config import game_init, image_init, event_handler
from ball_attack_decorator import Ball

game_init.init_config()
screen = game_init.window_config()
clock = pygame.time.Clock()
sounds = game_init.load_audio_assets()
font = game_init.define_font()

#define game variables
level = 1
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

# LOADING ASSETS AS DICTIONARIES
# Buttons
buttons = image_init.create_buttons()
# Heart
heart = image_init.load_heart_images()
# Bone and potion images, appended to a list
bone_images = image_init.load_four_frame_animation("bone")
red_potion = image_init.load_single_image("potion_red")
item_images = []
item_images.append(bone_images)
item_images.append(red_potion)
# Weapons and projectiles
weapon_image = image_init.load_single_image("weapon")
projectile_image = image_init.load_single_image("projectile")
ballattack1 = Ball()
# Background
cover = image_init.load_single_image("cover")
game_over_cover = image_init.load_single_image("game_over")

# LOADING ANIMATIONS AND TILES
tile_list = image_init.load_tile_images(level)
mob_animations = image_init.load_mob_animations()
intro_fade, death_fade = game_init.create_screen_fades(screen)

# CREATING GROUPS FOR LEVELS
damage_text_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
ballattack_group = pygame.sprite.Group()

# Information for the first level
world_data, world = game_init.restate_world(level)
world.process_data(world_data, tile_list, item_images, mob_animations)
kebo = world.player
weapon = Weapon(weapon_image, projectile_image)

#Extract enemies from world_data
enemy_list = world.character_list
score_bone = image_init.create_score_bone(bone_images)
item_group.add(score_bone)

# add the items from the level data
for item in world.item_list:
    item_group.add(item)

run = True
while run: 
    clock.tick(60)
    
    # SHOW GAME MENU
    if start_game == False: 
        screen.blit(cover, (0, 0))
        if buttons["start_button"].draw(screen):
            start_game = True
            start_intro = True
        if buttons["exit_button"].draw(screen):
            run = False
    else:
    # SHOW PAUSE MENU   
        if pause_game == True:
            pygame.mixer.music.set_volume(0)
            sounds["pause_sound"].play()
            screen.fill(const.MENU_BG)
            if buttons["resume_button"].draw(screen):
                pause_game = False
            if buttons["exit_button"].draw(screen):
                run = False
        else:
            screen.fill(const.BG)
            if kebo.animation.stats.alive:
                sounds["pause_sound"].stop()
                pygame.mixer.music.set_volume(0.3)
                
                #Calculate player movement
                dx, dy = event_handler.calculate_player_movement(moving_left, moving_right, moving_down, moving_up)
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
                        colorBallAttack = enemy.define_ball_color(ballattack1)
                        ballattack_image = image_init.scale_img(pygame.image.load(colorBallAttack.use()).convert_alpha(), const.BALLATTACK_SCALE)
                        ballattack = enemy.ai(kebo, world.obstacle_tiles, screen_scroll, ballattack_image)
                        if ballattack: 
                            ballattack_group.add(ballattack)
                    else:
                        enemy.ai(kebo, world.obstacle_tiles, screen_scroll)
                    if enemy.animation.stats.alive:
                        enemy.animation.update()
                
                damage_text_group.update(screen_scroll)
                item_group.update(screen_scroll, kebo, sounds["bone_sound"], sounds["heal_sound"])
                ballattack_group.update(screen_scroll, kebo)
                world.update(screen_scroll)   
                
            #DRAW 
            world.draw(screen)
            kebo.animation.draw(screen)
            weapon.draw(screen)
            for projectile in projectile_group:
                projectile.draw(screen)
            for ballattack in ballattack_group:
                ballattack.draw(screen)
            for enemy in enemy_list:
                if enemy.animation.stats.alive:
                    enemy.animation.draw(screen)

            damage_text_group.draw(screen)
            item_group.draw(screen)
            game_init.draw_info_top_bar(screen, kebo, heart, level, font)
            score_bone.draw(screen)

            #Check if level is complete
            if level_complete:
                music_publisher.end_boss_fight()
                sounds["level_up_sound"].play()
                start_intro = True
                damage_text_group, projectile_group, item_group, ballattack_group = game_init.reset_groups(damage_text_group, projectile_group, item_group, ballattack_group)
                level, world_data, world = game_init.next_level(level, world, world_data)
                tile_list = image_init.load_tile_images(level)
                world.process_data(world_data, tile_list, item_images, mob_animations)
                
                temporary_health = kebo.animation.stats.health
                temporary_score = kebo.score
                kebo = world.player
                kebo.animation.stats.health = temporary_health
                kebo.score = temporary_score
                enemy_list = world.character_list
                score_bone = image_init.create_score_bone(bone_images)
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
                    screen.blit(game_over_cover, (0, 0))
                    if buttons["restart_button"].draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        damage_text_group, projectile_group, item_group, ballattack_group = game_init.reset_groups(damage_text_group, projectile_group, item_group, ballattack_group)
                        #load in level data and create world
                        world_data, world = game_init.restate_world(level)
                        tile_list = image_init.load_tile_images(level)
                        world.process_data(world_data, tile_list, item_images, mob_animations)
                        temporary_score = kebo.score
                        kebo = world.player
                        kebo.score = temporary_score
                        enemy_list = world.character_list
                        score_bone = image_init.create_score_bone(bone_images)
                        item_group.add(score_bone)
                        for item in world.item_list:
                            item_group.add(item)
                    
    for event in pygame.event.get():
        #Close game
        run = event_handler.is_game_closed(event)
        #Keyboard presses and releases for the movement and pause state
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game = True
            else: pause_game = False   
        moving_left, moving_right, moving_up, moving_down = event_handler.check_keyboard(event)
    
    pygame.display.update()       
pygame.quit()