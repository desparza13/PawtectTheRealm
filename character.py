import math
import pygame
import weapon
import constants as const
import stats
import animation

class Character():
    def __init__(self, x, y, health, mob_animation, char_type, boss, size, stats):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.animation = animation.Animation(mob_animation, char_type, size, x, y, stats)    
        
    def move(self, dx, dy, obstacle_tiles, exit_tile = None):
        screen_scroll = [0, 0]
        level_complete = False
        self.animation.stats.running = False
        
        if dx!= 0 or dy != 0:
            self.animation.stats.running = True
        #Check the direction of the character
        
        if dx < 0:
            self.animation.flip = True
        if dx > 0:
            self.animation.flip = False
            
        #control diagonal speed
        if dx!= 0 and dy!=0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        
        #check collision with obstacles
        #first we move the character
        self.animation.rect.x += dx 
        for obstacle in obstacle_tiles:
            #check collision in the x direction
            if obstacle[1].colliderect(self.animation.rect):
                if dx > 0:
                    self.animation.rect.right = obstacle[1].left
                elif dx < 0:
                    self.animation.rect.left = obstacle[1].right
        #check collision in the y direction
        self.animation.rect.y += dy 
        for obstacle in obstacle_tiles:
            #check collision in the y direction
            if obstacle[1].colliderect(self.animation.rect):
                if dy > 0:
                    self.animation.rect.bottom = obstacle[1].top
                elif dy < 0:
                    self.animation.rect.top = obstacle[1].bottom
        
        # logic only applicable to player
        if self.char_type == 0:
            #update scroll based on player position
            #move camera left and right
            if self.animation.rect.right > (const.SCREEN_WIDTH - const.SCROLL_THRESH):
                screen_scroll[0] = (const.SCREEN_WIDTH - const.SCROLL_THRESH) - self.animation.rect.right
                self.animation.rect.right = (const.SCREEN_WIDTH - const.SCROLL_THRESH)
            if self.animation.rect.left < const.SCROLL_THRESH:
                screen_scroll[0] = const.SCROLL_THRESH - self.animation.rect.left
                self.animation.rect.left = const.SCROLL_THRESH

            #move camera up and down
            if self.animation.rect.bottom > (const.SCREEN_HEIGHT - const.SCROLL_THRESH):
                screen_scroll[1] = (const.SCREEN_HEIGHT - const.SCROLL_THRESH) - self.animation.rect.bottom
                self.animation.rect.bottom = (const.SCREEN_HEIGHT - const.SCROLL_THRESH)
            if self.animation.rect.top < const.SCROLL_THRESH:
                screen_scroll[1] = const.SCROLL_THRESH - self.animation.rect.top
                self.animation.rect.top = const.SCROLL_THRESH # 'freeze' the player's position on the screen
            
            #check if the player has reached the exit tile
            if exit_tile[1].colliderect(self.animation.rect):
                # ensure player's close to the exit ladder
                exit_dist = math.sqrt(((self.animation.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.animation.rect.centery - exit_tile[1].centery) ** 2))
                if exit_dist < 20:
                    level_complete = True
                
        return screen_scroll, level_complete
    
    def ai(self, player, obstacle_tiles, screen_scroll, ballattack_image):
        clipped_line = ()
        stun_cooldown = 0
        ballattack = None
        ai_dx = 0
        ai_dy = 0
        #reposition the mobs based on screen scroll
        self.animation.rect.x += screen_scroll[0]
        self.animation.rect.y += screen_scroll[1]

        #create a line of sight from the enemy to the player
        line_of_sight = ((self.animation.rect.centerx, self.animation.rect.centery), (player.animation.rect.centerx, player.animation.rect.centery))
        #check if the line of sight collides with any obstacle
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)


        # check distance to player
        dist = math.sqrt((self.animation.rect.centerx - player.animation.rect.centerx)**2 + ((self.animation.rect.centery - player.animation.rect.centery)**2))
        # if there's no intersection, then the enemy is going to go towards the player
        should_move_towards_player = not clipped_line and dist > const.RANGE
        if should_move_towards_player:
            if self.animation.rect.centerx > player.animation.rect.centerx:
                ai_dx = -const.ENEMY_SPEED
            if self.animation.rect.centerx < player.animation.rect.centerx:
                ai_dx = const.ENEMY_SPEED
            if self.animation.rect.centery > player.animation.rect.centery:
                ai_dy = -const.ENEMY_SPEED
            if self.animation.rect.centery < player.animation.rect.centery:
                ai_dy = const.ENEMY_SPEED
        
        if self.animation.stats.alive: 
            if not self.animation.stats.stunned:
                #move towards the player
                self.move(ai_dx, ai_dy, obstacle_tiles)
                #attack the player
                self.attack_the_player(dist, player)
                #boss enemies shoot ballattacks
                ballattack_cooldown = 700
                if self.boss:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.animation.stats.last_attack >= ballattack_cooldown:
                            ballattack = weapon.BallAttack(ballattack_image, self.animation.rect.centerx, self.animation.rect.centery, player.animation.rect.centerx, player.animation.rect.centery)
                            self.animation.stats.last_attack = pygame.time.get_ticks()

            if self.animation.stats.hit:
                self.animation.stats.hit = False
                self.animation.stats.last_hit = pygame.time.get_ticks()
                self.animation.stats.stunned = True
                self.animation.stats.running = False
                self.animation.set_action(0) #0: idle
                
            if (pygame.time.get_ticks() - self.animation.stats.last_hit) > stun_cooldown:
                self.animation.stats.stunned = False
        return ballattack


    def attack_the_player(self, dist, player):
        #check if the enemy is attacking the player
        if dist < const.ATTACK_RANGE and not player.animation.stats.hit:
            player.animation.stats.health -= 10
            player.animation.stats.hit = True
            player.animation.stats.last_hit = pygame.time.get_ticks()
            
        

    
    
            
        
  