from character import Character
import math
import constants as const

class Player(Character):
    def __init__(self, x, y, mob_animation, char_type, size, stats):
        super().__init__(x, y, mob_animation, char_type, size, stats)
        self.score = 0

    def check_exit_tile(self, exit_tile):
        if exit_tile[1].colliderect(self.animation.rect):
                # ensure player's close to the exit ladder
                exit_dist = math.sqrt(((self.animation.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.animation.rect.centery - exit_tile[1].centery) ** 2))
                if exit_dist < 20:
                    return True
        return False
    
    def update_screen_scroll(self,screen_scroll):
        screen_width = const.SCREEN_WIDTH
        scroll_thresh = const.SCROLL_THRESH
        scroll_height = const.SCREEN_HEIGHT
        
        #move camera left and right
        if self.animation.rect.right > (screen_width - scroll_thresh):
            screen_scroll[0] = (screen_width - scroll_thresh) - self.animation.rect.right
            self.animation.rect.right = (screen_width - scroll_thresh)
        if self.animation.rect.left < scroll_thresh:
            screen_scroll[0] = scroll_thresh - self.animation.rect.left
            self.animation.rect.left = scroll_thresh

        #move camera up and down
        if self.animation.rect.bottom > (scroll_height - scroll_thresh):
            screen_scroll[1] = (scroll_height - scroll_thresh) - self.animation.rect.bottom
            self.animation.rect.bottom = (scroll_height - scroll_thresh)
        if self.animation.rect.top < scroll_thresh:
            screen_scroll[1] = scroll_thresh - self.animation.rect.top
            self.animation.rect.top = scroll_thresh # 'freeze' the player's position on the screen
    
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
            dx, dy = self.control_diagonal_speed(dx,dy)
        
        #check collision with obstacles
        self.collide_with_obstacles(dx,dy,obstacle_tiles)
        
        # logic only applicable to player
        #update scroll based on player position
        self.update_screen_scroll(screen_scroll)
            
        #check if the player has reached the exit tile
        level_complete = self.check_exit_tile(exit_tile)
                
        return screen_scroll, level_complete
    