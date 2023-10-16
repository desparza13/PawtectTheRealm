import math
import pygame
import weapon
import constants as const

class Character():
    def __init__(self, x, y, health, mob_animation, char_type, boss, size):
        self.char_type = char_type
        self.boss = boss
        self.flip = False
        self.score = 0
        #animation 
        self.animation_list = mob_animation[char_type]
        self.frame_index = 0
        self.action = 0 #0: idle, 1: run
        self.update_time = pygame.time.get_ticks() #How much time has passed since the last time we update the frame
        self.running = False
        
        #set character position
        self.image = self.animation_list[self.action][self.frame_index] 
        self.rect = pygame.Rect(0, 0, const.TILE_SIZE * size, const.TILE_SIZE * size)
        self.rect.center = (x, y)
        self.health = health
        self.alive = True
        
        # character hitting and getting hit
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.stunned = False
        self.last_attack = pygame.time.get_ticks()

        
    def move(self, dx, dy, obstacle_tiles, exit_tile = None):
        screen_scroll = [0, 0]
        level_complete = False
        self.running = False
        
        if dx!= 0 or dy != 0:
            self.running = True
        #Check the direction of the character
        
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
            
        #control diagonal speed
        if dx!= 0 and dy!=0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        
        #check collision with obstacles
        #first we move the character
        self.rect.x += dx 
        for obstacle in obstacle_tiles:
            #check collision in the x direction
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                elif dx < 0:
                    self.rect.left = obstacle[1].right
        #check collision in the y direction
        self.rect.y += dy 
        for obstacle in obstacle_tiles:
            #check collision in the x direction
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                elif dy < 0:
                    self.rect.top = obstacle[1].bottom
        
        # logic only applicable to player
        if self.char_type == 0:
            #update scroll based on player position
            #move camera left and right
            if self.rect.right > (const.SCREEN_WIDTH - const.SCROLL_THRESH):
                screen_scroll[0] = (const.SCREEN_WIDTH - const.SCROLL_THRESH) - self.rect.right
                self.rect.right = (const.SCREEN_WIDTH - const.SCROLL_THRESH)
            if self.rect.left < const.SCROLL_THRESH:
                screen_scroll[0] = const.SCROLL_THRESH - self.rect.left
                self.rect.left = const.SCROLL_THRESH

            #move camera up and down
            if self.rect.bottom > (const.SCREEN_HEIGHT - const.SCROLL_THRESH):
                screen_scroll[1] = (const.SCREEN_HEIGHT - const.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = (const.SCREEN_HEIGHT - const.SCROLL_THRESH)
            if self.rect.top < const.SCROLL_THRESH:
                screen_scroll[1] = const.SCROLL_THRESH - self.rect.top
                self.rect.top = const.SCROLL_THRESH # 'freeze' the player's position on the screen
            
            #check if the player has reached the exit tile
            if exit_tile[1].colliderect(self.rect):
                # ensure player's close to the exit ladder
                exit_dist = math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.rect.centery - exit_tile[1].centery) ** 2))
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
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
        #check if the line of sight collides with any obstacle
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)


        # check distance to player
        dist = math.sqrt((self.rect.centerx - player.rect.centerx)**2 + ((self.rect.centery - player.rect.centery)**2))
        # if there's no intersection, then the enemy is going to go towards the player
        if not clipped_line and dist > const.RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -const.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = const.ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -const.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = const.ENEMY_SPEED
        
        if self.alive: 
            if not self.stunned:
                #move towards the player
                self.move(ai_dx, ai_dy, obstacle_tiles)
                #attack the player
                self.attack_the_player(dist, player)
                #boss enemies shoot ballattacks
                ballattack_cooldown = 700
                if self.boss:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.last_attack >= ballattack_cooldown:
                            ballattack = weapon.BallAttack(ballattack_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                            self.last_attack = pygame.time.get_ticks()

            if self.hit:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0) #0: idle
                
            if (pygame.time.get_ticks() - self.last_hit) > stun_cooldown:
                self.stunned = False
        
        return ballattack


    def attack_the_player(self, dist, player):
        #check if the enemy is attacking the player
        if dist < const.ATTACK_RANGE and not player.hit:
            player.health -= 10
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            
        
    def update(self):
        '''Method for handle character animation '''
        #check if character has died
        if self.health <= 0:
            self.health =0
            self.alive = False

        # timer to reset player taking the hit (1 hit per second)
        hit_cooldown = 1000
        if self.char_type == 0:
            if self.hit and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False

                
        #check what action the player is performing
        if self.running == True:
            self.update_action(1) #1 : run
        else:
            self.update_action(0) #0: idle
            
        animation_cooldown = 90 #speed of the animation
        
        #Handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1 #move to the next frame
            self.update_time = pygame.time.get_ticks() #reset the timer
            
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0 #reset frame index
    
    def update_action(self,action):
        #check if the new action is different to the previous one
        if action != self.action:
            self.action = action
            #update the animation settings
            self.frame_index=0
            self.update_time = pygame.time.get_ticks()
            
        
    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False) #image, flip horizontal, flip vertical
        
        if self.char_type == 0: 
            #Add the offset to the image so that it appears in the center of the rectangle
            surface.blit(flipped_image, (self.rect.x,self.rect.y - (const.OFFSET * const.SCALE))) 
        else:
            surface.blit(flipped_image, self.rect) #draw the image

        #pygame.draw.rect(surface, const.RED, self.rect, 1) #empty rectangle with the image
        