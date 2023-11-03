import math
import pygame
import constants as const
import stats

class Animation():
    HIT_COOLDOWN = 1000  # Cooldown period for hit animation

    def __init__(self, mob_animation, char_type, size, x, y, stats):
        self.animation_list = mob_animation[char_type]
        self.frame_index = 0
        self.action = 0 #Idle action by default
        self.update_time = pygame.time.get_ticks() 
        self.flip = False
        self.image = self.animation_list[self.action][self.frame_index]
        self.char_type = char_type
        #set character position
        self.rect = self._create_rect(size, x, y)
        #stats
        self.stats = stats
        
    def _create_rect(self, size, x, y):
        rect = pygame.Rect(0, 0, const.TILE_SIZE * size, const.TILE_SIZE * size)
        rect.center = (x, y)
        return rect
    
    def draw(self, surface):
        offset_y = const.OFFSET * const.SCALE if self.char_type == 0 else 0
        surface.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y - offset_y))
            
    def update_animation_timing(self):
        '''Check if enough time has passed since the last update'''
        if pygame.time.get_ticks() - self.update_time > 90:
            self.frame_index +=1 #move to the next frame
            self.update_time = pygame.time.get_ticks() #reset the timer
            
    def reset_animation_if_finished(self):
        '''Check if the animation has finished'''
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0 #reset frame index
    
    def update_health_status(self):
        if self.stats.health <= 0:
            self.stats.health = 0
            self.stats.alive = False
    
    def has_hit_cooldown_passed(self):
        return pygame.time.get_ticks() - self.stats.last_hit > Animation.HIT_COOLDOWN
    
    def update_hit_cooldown(self):
        '''Update timer to reset player taking the hit (1 hit per second)'''
        if self.char_type == 0 and self.stats.hit and self.has_hit_cooldown_passed():
            self.stats.hit = False        
    
    def set_action(self,new_action):
            #check if the new action is different to the previous one
            if new_action != self.action:
                self.action = new_action
                #update the animation settings
                self.frame_index=0
                self.update_time = pygame.time.get_ticks()
                
    def update(self):
        '''Method for handling character animation '''
        self.update_health_status()
        self.update_hit_cooldown()
        current_action = 1 if self.stats.running else 0 # 1 running / 0 idle
        self.set_action(current_action)
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_animation_timing()
        self.reset_animation_if_finished()
