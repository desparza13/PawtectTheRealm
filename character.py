import math
import pygame
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

        
    def move(self, dx, dy):
        screen_scroll = [0, 0]
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
            
        self.rect.x += dx
        self.rect.y += dy

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
        
        return screen_scroll
    
    def ai(self, screen_scroll):
        #this will be the AI for enemy
        #reposition the mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
                
        
    def update(self):
        '''Method for handle character animation '''
        #check if character has died
        if self.health <= 0:
            self.health =0
            self.alive = False
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

        pygame.draw.rect(surface, const.RED, self.rect, 1) #empty rectangle with the image
        