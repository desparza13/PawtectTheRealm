from character import Character
import math
import config.constants as const

class Player(Character):
    """
    Concrete Product Class representing the Player character in the Pawtect the Realm game.
    This class inherits from the Character abstract base class.

    Attributes:
        score (int): The player's score.
    """
    def __init__(self, x, y, mob_animation, char_type, size, stats) -> None:
        """
        Initializes a new player with specified characteristics and position.
        """
        super().__init__(x, y, mob_animation, char_type, size, stats)
        self.score = 0 # Initialize player's score to 0.

    def check_exit_tile(self, exit_tile) -> bool:
        """
        Checks if the player is colliding with the exit tile and is close enough to trigger level completion.
        """
        center_x = (self.animation.rect.centerx - exit_tile[1].centerx) ** 2
        center_y = (self.animation.rect.centery - exit_tile[1].centery) ** 2
        # Collision check with the exit tile.
        if exit_tile[1].colliderect(self.animation.rect):
            # Calculate the distance to the center of the exit tile.
            exit_dist = math.sqrt(center_x + center_y)
            # If close enough, player can exit the level.
            if exit_dist < 20:
                return True
        return False
    
    def update_screen_scroll(self, screen_scroll) -> None:
        """
        Adjusts the screen's scroll position based on the player's movement.
        """
        # Screen boundaries and scroll threshold.
        screen_width = const.SCREEN_WIDTH
        scroll_thresh = const.SCROLL_THRESH
        screen_height = const.SCREEN_HEIGHT
        
        # Update horizontal scroll position.
        self.update_horizontal_scroll(screen_width, scroll_thresh, screen_scroll)
        # Update vertical scroll position.
        self.update_vertical_scroll(screen_height, scroll_thresh, screen_scroll)

    def update_horizontal_scroll(self, screen_width, scroll_thresh, screen_scroll) -> None:
        """
        Adjusts the horizontal scroll position based on the player's horizontal movement.
        """
        if self.animation.rect.right > (screen_width - scroll_thresh):
            screen_scroll[0] = (screen_width - scroll_thresh) - self.animation.rect.right
            self.animation.rect.right = (screen_width - scroll_thresh)
        if self.animation.rect.left < scroll_thresh:
            screen_scroll[0] = scroll_thresh - self.animation.rect.left
            self.animation.rect.left = scroll_thresh

    def update_vertical_scroll(self, screen_height, scroll_thresh, screen_scroll) -> None:
        """
        Adjusts the vertical scroll position based on the player's vertical movement.
        """
        if self.animation.rect.bottom > (screen_height - scroll_thresh):
            screen_scroll[1] = (screen_height - scroll_thresh) - self.animation.rect.bottom
            self.animation.rect.bottom = (screen_height - scroll_thresh)
        if self.animation.rect.top < scroll_thresh:
            screen_scroll[1] = scroll_thresh - self.animation.rect.top
            self.animation.rect.top = scroll_thresh

    def move(self, dx, dy, obstacle_tiles, exit_tile = None) -> tuple:
        '''
        Controls the player's animation when moving and handles collision with obstacles.
        '''
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
            dx, dy = self.control_diagonal_speed(dx,dy)
        
        #check collision with obstacles
        self.collide_with_obstacles(dx,dy,obstacle_tiles)
        
        # logic only applicable to player
        #update scroll based on player position
        self.update_screen_scroll(screen_scroll)
            
        #check if the player has reached the exit tile
        level_complete = self.check_exit_tile(exit_tile)
                
        return screen_scroll, level_complete
    