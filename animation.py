import math
import pygame
import config.constants as const
import stats

class Animation():
    """
    A class that handles the animation states and frames for a character in the Pawtect the Realm game.

    Attributes:
        animation_list (list): A nested list where each sublist represents an animation state containing frames.
        frame_index (int): The current frame index within the animation state.
        action (int): The current action or state of the animation.
        update_time (int): Timestamp of the last update to control animation timing.
        flip (bool): Whether the image should be flipped horizontally.
        image (Surface): The current image of the animation frame.
        char_type (str): The type of character that is being animated.
        rect (Rect): The rectangle representing the position and size of the character.
        stats (Stats): An object containing the character's stats such as health and whether it's alive.
    """
    HIT_COOLDOWN = 1000  # Cooldown period for hit animation

    def __init__(self, mob_animation, char_type, size, x, y, stats):
        '''
        Initializes the Animation object with the given parameters.
        '''
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
        '''
        Creates a rectangle for the character's position and size.
        '''
        rect = pygame.Rect(0, 0, const.TILE_SIZE * size, const.TILE_SIZE * size)
        rect.center = (x, y)
        return rect
    
    def draw(self, surface):
        '''
        Draws the character's current animation frame onto a surface.
        '''
        offset_y = const.OFFSET * const.SCALE if self.char_type == 0 else 0
        surface.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y - offset_y))
            
    def update_animation_timing(self):
        '''
        Updates the animation frame index based on timing, advancing the animation.
        '''
        if pygame.time.get_ticks() - self.update_time > 90:
            self.frame_index +=1 #move to the next frame
            self.update_time = pygame.time.get_ticks() #reset the timer
            
    def reset_animation_if_finished(self):
        '''
        Resets the animation frame index if the end of the animation list is reached.
        '''
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0 #reset frame index
    
    def update_health_status(self):
        '''
        Updates the character's health status, setting alive status to False if health is depleted.
        '''
        if self.stats.health <= 0:
            self.stats.health = 0
            self.stats.alive = False
    
    def has_hit_cooldown_passed(self):
        '''
        Checks if the cooldown period after a hit has passed.
        '''
        return pygame.time.get_ticks() - self.stats.last_hit > Animation.HIT_COOLDOWN
    
    def update_hit_cooldown(self):
        '''Update timer to reset player taking the hit (1 hit per second)'''
        if self.char_type == 0 and self.stats.hit and self.has_hit_cooldown_passed():
            self.stats.hit = False        
    
    def set_action(self,new_action):
        '''
        Changes the action state of the animation to a new one.
        '''
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index=0
            self.update_time = pygame.time.get_ticks()
                
    def update(self):
        '''
        The main method to update the character's animation state and frame index.
        '''
        self.update_health_status()
        self.update_hit_cooldown()
        current_action = 1 if self.stats.running else 0 # 1 running / 0 idle
        self.set_action(current_action)
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_animation_timing()
        self.reset_animation_if_finished()
