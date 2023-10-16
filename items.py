import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_bone = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0: bone, 1: health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dummy_bone  = dummy_bone 
    
    def update(self, screen_scroll, player):
        #doesn't apply to the dummy_bone
        if not self.dummy_bone:
            #reposition based on screen scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        #check to see if item has been collected by the player
        if self.rect.colliderect(player.rect):
            #bone collected
            if self.item_type == 0 : # 0: Bone
                player.score += 1
            elif self.item_type == 1: # 1: Potion
                player.health += 10
                if player.health > 100:
                    player.health = 100 #maximum health of the player
                    
            self.kill() #kill the bone item
                
        #handle animation
        animation_cooldown = 150
        
        #update image
        self.image = self.animation_list[self.frame_index]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1 #move to the next frame
            self.update_time = pygame.time.get_ticks()  #reset the timer
            
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0  #reset frame index
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)