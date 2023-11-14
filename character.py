from abc import ABC, abstractmethod
import math
import pygame
import config.constants as const
import animation

class Character(ABC):
    """
    Abstract base class representing a generic character in the Pawtect the Realm game.
    This class should be subclassed to create specific character types.

    Attributes:
        char_type (str): The type of character (e.g., 'player', 'enemy').
        animation (Animation): An animation object managing the character's sprites and movements.
    """
    
    def __init__(self, x, y, mob_animation, char_type, size, stats):
        '''
        Initialize a new character
        '''
        self.char_type = char_type
        self.animation = animation.Animation(mob_animation, char_type, size, x, y, stats)    
        
    def collide_with_obstacles(self, dx, dy, obstacle_tiles):
        '''
        Handles character collision with obstacles
        '''
        #Move the character
        self.animation.rect.x += dx 
        for obstacle in obstacle_tiles:
            #Check collision in the x direction
            if obstacle[1].colliderect(self.animation.rect):
                if dx > 0: #Moving right
                    self.animation.rect.right = obstacle[1].left
                elif dx < 0: #Moving left
                    self.animation.rect.left = obstacle[1].right
        #Check collision in the y direction
        self.animation.rect.y += dy 
        for obstacle in obstacle_tiles:
            #check collision in the y direction
            if obstacle[1].colliderect(self.animation.rect):
                if dy > 0: #Moving down
                    self.animation.rect.bottom = obstacle[1].top
                elif dy < 0: #Moving up
                    self.animation.rect.top = obstacle[1].bottom
                    
    def control_diagonal_speed(self,dx,dy):
        '''
        Adjusts the character's speed when moving diagonally to maintain a consistent overall velocity.
        '''
        factor = (math.sqrt(2)/2)
        return (dx * factor), (dy * factor)
            
    @abstractmethod        
    def move():
        '''
        Abstract method to be implemented by subclasses to define character movement.
        '''
        pass
