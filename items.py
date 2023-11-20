import pygame

class Item(pygame.sprite.Sprite):
    """
    Item is a class that represents an item in the game world that can be collected by the player.

    Attributes:
        item_type (int): The type of item. 0: bone, 1: health potion
        animation_list (list): A list of images that make up the item's animation.
        frame_index (int): The current frame of the item's animation.
        update_time (int): The time at which the item's animation was last updated.
        image (pygame.Surface): The current image of the item.
        rect (pygame.Rect): The rectangle that represents the item's position and size.
        dummy_bone (bool): A flag that indicates whether the item is a dummy bone.
    """
    def __init__(self, x, y, item_type, animation_list, dummy_bone=False) -> None:
        """
        Initializes a new item with specified characteristics and position.
        If the dummy_bone is set to True, the item will not move with the screen scroll and
        will instead be positioned at a fixed location in the game world.
        """
        super().__init__()
        self.item_type = item_type  # 0: bone, 1: health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]  # Set initial image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Position the item
        self.dummy_bone = dummy_bone

    def update(self, screen_scroll, player, bone_sound, heal_sound) -> None:
        """
        Updates the item's position and animation whether it is a dummy bone or not.
        """
        if not self.dummy_bone:
            self.reposition_with_scroll(screen_scroll)
        self.check_collection(player, bone_sound, heal_sound)
        self.update_animation()

    def reposition_with_scroll(self, screen_scroll) -> None:
        """
        Repositions the item with the screen scroll according to the player's movement.
        """
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def check_collection(self, player, bone_sound, heal_sound) -> None:
        """
        Checks if the player has collected the item and performs the appropriate action.
        """
        if self.rect.colliderect(player.animation.rect):
            if self.item_type == 0:  # Bone
                self.collect_bone(player, bone_sound, heal_sound)
            elif self.item_type == 1:  # Potion
                self.collect_potion(player, heal_sound)
            self.kill()

    def player_gained_health(self, player) -> None:
        """
        Updates the player's health by 10 points and caps it at 100.
        """
        player.animation.stats.health += 10
        if player.animation.stats.health > 100:
            player.animation.stats.health = 100
        
    def collect_bone(self, player, bone_sound, heal_sound) -> None:
        """
        Updates the player's score and plays a sound effect when a bone is collected.
        """
        # give +10 health points if the player has 10 bones
        if player.score >= 9:
            self.player_gained_health(player)
            player.score = 0
            heal_sound.play()
        player.score += 1
        bone_sound.play()

    def collect_potion(self, player, heal_sound) -> None:
        """
        Updates the player's health and plays a sound effect when a potion is collected.
        """
        self.player_gained_health(player)
        heal_sound.play()

    def update_animation(self) -> None:
        """
        Updates the item's current animation frame.
        """
        animation_cooldown = 150
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, surface) -> None:
        """
        Draws the item on the provided surface.
        """
        surface.blit(self.image, self.rect)
