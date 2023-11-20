from abc import ABC, abstractmethod
import math
import animation

class Character(ABC):
    """
    Abstract base class representing a generic character in the Pawtect the Realm game.
    This class should be subclassed to create specific character types.

    Attributes:
        char_type (int): The type of character.
        animation (Animation): An animation object managing the character's sprites and movements.
    """
    
    def __init__(self, x, y, mob_animation, char_type, size, stats) -> None:
        '''
        Initialize a new character
        '''
        self.char_type = char_type
        self.animation = animation.Animation(mob_animation, char_type, size, x, y, stats)    
        
    def collide_with_obstacles(self, dx, dy, obstacle_tiles) -> None:
        '''
        Handles character collision with obstacles in both x and y directions.
        '''
        self.x_collision(dx, obstacle_tiles)
        self.y_collision(dy, obstacle_tiles)

    def x_collision(self, dx, obstacle_tiles) -> None:
        '''
        Handles character collision with obstacles in the x direction.
        '''
        self.animation.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.animation.rect):
                if dx > 0:  # Moving right
                    self.animation.rect.right = obstacle[1].left
                elif dx < 0:  # Moving left
                    self.animation.rect.left = obstacle[1].right

    def y_collision(self, dy, obstacle_tiles) -> None:
        '''
        Handles character collision with obstacles in the y direction.
        '''
        self.animation.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.animation.rect):
                if dy > 0:  # Moving down
                    self.animation.rect.bottom = obstacle[1].top
                elif dy < 0:  # Moving up
                    self.animation.rect.top = obstacle[1].bottom
                    
    def control_diagonal_speed(self,dx,dy) -> tuple:
        '''
        Adjusts the character's speed when moving diagonally to maintain a consistent overall velocity.
        '''
        factor = (math.sqrt(2)/2)
        return (dx * factor), (dy * factor)
            
    @abstractmethod        
    def move() -> None:
        '''
        Abstract method to be implemented by subclasses to define character movement.
        '''
        pass
