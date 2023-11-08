from abc import ABC, abstractmethod
import math
import pygame
import constants as const
import animation

class Character(ABC):
    def __init__(self, x, y, mob_animation, char_type, size, stats):
        self.char_type = char_type
        self.animation = animation.Animation(mob_animation, char_type, size, x, y, stats)    
        
    def collide_with_obstacles(self, dx, dy, obstacle_tiles):
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
                    
    def control_diagonal_speed(self,dx,dy):
        factor = (math.sqrt(2)/2)
        return (dx * factor), (dy * factor)
            
    @abstractmethod        
    def move():
        pass
    
            
        

    
    
            
        
  