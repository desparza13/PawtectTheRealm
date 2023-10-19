import random
import pygame
import math
import constants as const

class Weapon():
    def __init__(self,image, projectile_image) -> None:
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.projectile_image = projectile_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks() #How much time has passed since the last time we fired
        
    def update(self, player):
        shot_cooldown = 300 #speed of the fired
        projectile = None
        
        self.rect.center = player.rect.center
        
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery) # negative because pygame y coordinates increase down the screen
        
        #Calculate the angle for the weapon based in the mouse
        self.angle = math.degrees(math.atan2(y_dist,x_dist))
        
        #Get mouseclick
        if pygame.mouse.get_pressed()[0] and self.fired ==False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown: #0: left button , 1: middle button, 2: right button
            projectile = Projectile(self.projectile_image,self.rect.centerx,self.rect.centery,self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        #reset mouseclick
        if pygame.mouse.get_pressed()[0]==False:
            self.fired = False
        return projectile
        
    def draw(self,surface):
        self.image =pygame.transform.rotate(self.original_image,self.angle)
        #Draw the weapon around the player/rectangle
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image,self.angle - 90) # -90 because the way the sprite itself is orientated
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * const.PROJECTILE_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * const.PROJECTILE_SPEED) #negative because pygame y coordinate increases down the screen
    
    def update(self, screen_scroll, obstacle_tiles, enemy_list):
        #reset variables
        damage = 0
        damage_pos = None
        
        #reposition based on speed and on the screen_scroll of the player
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check collision with walls
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        
        #check if projectile has gone off screen
        if self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > const.SCREEN_HEIGHT:
            self.kill() #kill the projectile
            
        #check collision between projectile and enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive: #if two rectangles are overlapping
                damage = 10 + random.randint(0,5) #damage between 10-15
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill() #kill the projectile
                break
            
        return damage,damage_pos
        
    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))


class BallAttack(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        # Calculate the angle for the ballattack
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image,self.angle - 90) 
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * const.BALLATTACK_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * const.BALLATTACK_SPEED) #negative because pygame y coordinate increases down the screen
    
    # if we decide to kill ballattacks when hitting walls, add 'obstacle_tiles' as a parameter
    def update(self, screen_scroll, player):
        #reposition based on speed and on the screen_scroll of the player
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        #check if it has gone off screen
        if self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > const.SCREEN_HEIGHT:
            self.kill() 

        #check collision between ballattack and player
        if player.rect.colliderect(self.rect) and player.alive and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -= 10
            self.kill()


    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
   