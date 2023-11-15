import pygame

class Item(pygame.sprite.Sprite):
    """
    Class to represent collectible items in the game. Inherits from pygame's Sprite class.

    Attributes:
        item_type (int): The type of item, where 0 is bone and 1 is health potion.
        animation_list (list): A list of Surfaces for the item's animation.
        frame_index (int): The current frame index in the animation list.
        update_time (int): The timestamp of the last update to control animation speed.
        image (pygame.Surface): The current image of the item's animation.
        rect (pygame.Rect): The rectangle that defines the item's position.
        dummy_bone (bool): A flag to indicate whether the item is a dummy for display purposes only.
    """
    
    def __init__(self, x, y, item_type, animation_list, dummy_bone = False):
        """
        Initializes the item with its type, animation, position, and dummy flag.
        """
        pygame.sprite.Sprite.__init__(self) # Initialize the parent class
        self.item_type = item_type # 0: bone, 1: health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index] # Set initial image
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y) # Position the item
        self.dummy_bone  = dummy_bone 
    
    def update(self, screen_scroll, player, bone_sound, heal_sound):
        """
        Updates the item's animation and checks for collection by the player.
        """
        # If the item is not a dummy, reposition it based on screen scroll
        if not self.dummy_bone:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
            
        # Check if the item has been collected by the player
        if self.rect.colliderect(player.animation.rect):
            # If it's a bone, increase the player's score and play a sound
            if self.item_type == 0 : # 0: Bone
                player.score += 1
                bone_sound.play()
            # If it's a potion, increase the player's health and play a sound
            elif self.item_type == 1: # 1: Potion
                player.animation.stats.health += 10
                heal_sound.play()
                # Cap the player's health at a maximum value
                if player.animation.stats.health > 100:
                    player.animation.stats.health = 100 
                    
            self.kill() # Remove the item from the game
                
        # Handle animation updates
        animation_cooldown = 150 # Time in milliseconds between frame changes
        
        # Update the item's image to the current frame
        self.image = self.animation_list[self.frame_index]
        
        # Update the image to the next frame if cooldown time has passed
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1 #move to the next frame
            self.update_time = pygame.time.get_ticks()  #reset the timer
            
        # If the animation has reached the end, reset to the first frame
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0  #reset frame index
        
    def draw(self, surface):
        """
        Draws the item onto the given surface.
        """
        surface.blit(self.image, self.rect)