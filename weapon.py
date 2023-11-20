import random
import pygame
import math
import config.constants as const

class Projectile(pygame.sprite.Sprite):
    """
    A class to represent a projectile fired by a weapon.

    Attributes:
    ----------
    original_image : pygame.Surface
        The original image of the projectile before any rotation.
    angle : float
        The angle at which the projectile is moving.
    image : pygame.Surface
        The current image of the projectile after rotation.
    rect : pygame.Rect
        The rectangle that defines the position and size of the projectile image.
    dx : float
        The change in the x-coordinate of the projectile per update.
    dy : float
        The change in the y-coordinate of the projectile per update.
    """
    
    def __init__(self, image, x, y, angle) -> None:
        """
        Initializes the Projectile object with an image, position, and angle of movement.
        """
        super().__init__()
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = math.cos(math.radians(self.angle)) * const.PROJECTILE_SPEED
        self.dy = -math.sin(math.radians(self.angle)) * const.PROJECTILE_SPEED

    def update(self, screen_scroll, obstacle_tiles, enemy_list) -> tuple:
        """
        Update the projectile's position, check for collisions with obstacles and enemies, 
        and remove it if necessary.
        """
        self.update_position(screen_scroll)
        if self.collide_with_obstacles(obstacle_tiles):
            return 0, None
        hit_enemy = self.collide_with_enemies(enemy_list)
        if hit_enemy:
            return hit_enemy
        self.check_off_screen()
        return 0, None

    def update_position(self, screen_scroll):
        """
        Update the projectile's position based on the screen scroll.
        """
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

    def collide_with_obstacles(self, obstacle_tiles) -> bool:
        """
        Check for collisions with obstacles and remove the projectile if necessary.
        """
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()
                return True
        return False

    def collide_with_enemies(self, enemy_list) -> tuple:
        """
        Check for collisions with enemies and remove the projectile if it hits them.
        """
        for enemy in enemy_list:
            if enemy.animation.rect.colliderect(self.rect) and enemy.animation.stats.alive:
                damage = 10 + random.randint(0, 5)
                enemy.animation.stats.health -= damage
                enemy.animation.stats.hit = True
                self.kill()
                return damage, enemy.animation.rect
        return None

    def check_off_screen(self):
        """
        Check if the projectile exceeds the boundaries of the screen and removes it.
        """
        if (self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > const.SCREEN_HEIGHT):
            self.kill()

    def draw(self, surface) -> None:
        """
        Draws the projectile onto the given surface.
        """
        surface.blit(self.image, self.rect)
        
        
class Weapon:
    """
    A class to represent a weapon that can be used by the player.

    Attributes:
    ----------
    original_image : Surface
        The original image of the weapon before any rotation.
    projectile_image : Surface
        The image of the projectile that the weapon fires.
    angle : float
        The angle at which the weapon is currently pointing.
    image : Surface
        The current image of the weapon after rotation.
    rect : Rect
        The rectangle that defines the position and size of the weapon image.
    fired : bool
        A flag indicating whether the weapon has been fired.
    last_shot : int
        The timestamp of the last shot fired by the weapon.
    """
    
    def __init__(self, image, projectile_image) -> None:
        """
        Initializes the Weapon object with an image and a projectile image.
        """
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.projectile_image = projectile_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player) -> Projectile:
        """
        Update the weapon's position based on the player's position and fire a projectile if conditions are met.
        """
        shot_cooldown = 300  # Minimum time required between shots
        projectile = None

        # Align the weapon with the player's position
        self.rect.center = player.animation.rect.center

        # Calculate the angle between the weapon and the mouse cursor
        mouse_pos = pygame.mouse.get_pos()
        x_dist = mouse_pos[0] - self.rect.centerx
        y_dist = -(mouse_pos[1] - self.rect.centery)  # Pygame's y-axis is inverted

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # Check for mouse click and if the weapon is ready to fire again
        if (pygame.mouse.get_pressed()[0] and not self.fired and
                (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown):
            projectile = Projectile(self.projectile_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

        # Reset the fired flag when the mouse button is released
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return projectile

    def draw(self, surface) -> None:
        """
        Draws the weapon onto the given surface, rotating it around the player.
        """
        # Rotate the image based on the current angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Calculate the new center of the rotated image
        image_center_x = self.rect.centerx - (self.image.get_width() // 2)
        image_center_y = self.rect.centery - (self.image.get_height() // 2)

        # Draw the weapon on the surface
        surface.blit(self.image, (image_center_x, image_center_y))



        
class BallAttack(pygame.sprite.Sprite):
    """
    A class to represent a ball-like attack that moves towards a target.

    Attributes:
    ----------
    original_image : pygame.Surface
        The original image of the ball attack before any rotation.
    angle : float
        The angle at which the ball attack is moving.
    image : pygame.Surface
        The current image of the ball attack after rotation.
    rect : pygame.Rect
        The rectangle that defines the position and size of the ball attack image.
    dx : float
        The change in the x-coordinate of the ball attack per update.
    dy : float
        The change in the y-coordinate of the ball attack per update.
    """

    def __init__(self, image, x, y, target_x, target_y) -> None:
        """
        Initializes the BallAttack object with an image, position, and a target position.
        """
        super().__init__()
        self.original_image = image
        self.angle = math.degrees(math.atan2(-(target_y - y), target_x - x))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = math.cos(math.radians(self.angle)) * const.BALLATTACK_SPEED
        self.dy = -math.sin(math.radians(self.angle)) * const.BALLATTACK_SPEED

    def update(self, screen_scroll, player) -> None:
        """
        Update the ball attack's position and check for collisions with the player.
        """
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        if (self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > const.SCREEN_HEIGHT):
            self.kill()

        if player.animation.rect.colliderect(self.rect) and player.animation.stats.alive and not player.animation.stats.hit:
            player.animation.stats.hit = True
            player.animation.stats.last_hit = pygame.time.get_ticks()
            player.animation.stats.health -= 10
            self.kill()

    def draw(self, surface) -> None:
        """
        Draws the ball attack onto the given surface.
        """
        surface.blit(self.image, self.rect)
