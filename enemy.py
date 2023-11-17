from character import Character
import pygame
import config.constants as const
import math

class Enemy(Character):
    """
    Concrete Product Class representing the Enemy (sprites) in the Pawtect the Realm game.
    This class inherits from the Character abstract base class.

    Attributes:
        None
    """
    def move(self, dx, dy, obstacle_tiles):
        """
        Moves the enemy character while considering collisions.
        """
        # If there is movement, set the running status to True.
        self.animation.stats.running = False
        self.animation.stats.running = bool(dx or dy)
        
        # Determine direction based on movement to flip the sprite accordingly.
        self.animation.flip = dx < 0
            
        # Normalize speed if moving diagonally to maintain consistent movement speed.
        if dx and dy:
            dx, dy = self.control_diagonal_speed(dx,dy)
        
        # Check for collisions with the obstacles.
        self.collide_with_obstacles(dx,dy,obstacle_tiles)

    
    def ai(self, player, obstacle_tiles, screen_scroll):
        """
        Artificial Intelligence behavior for the enemy, determining movement and attacks.
        """
        clipped_line = ()
        stun_cooldown = 0
        ai_dx = 0
        ai_dy = 0
        # Reposition based on screen scroll to maintain world position.
        self.animation.rect.x += screen_scroll[0]
        self.animation.rect.y += screen_scroll[1]

        # Create a line of sight and check if there are any obstacles in the way
        line_of_sight = ((self.animation.rect.centerx, self.animation.rect.centery), (player.animation.rect.centerx, player.animation.rect.centery))
        
        # Check for collision with line of sight to determine if the enemy can see the player
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)


        # Calculate the distance to the player to decide on movement and attack
        dist = math.sqrt((self.animation.rect.centerx - player.animation.rect.centerx)**2 + ((self.animation.rect.centery - player.animation.rect.centery)**2))
        
        #If the player is in range and visible, determine the movement direction.
        should_move_towards_player = not clipped_line and dist > const.RANGE
        if should_move_towards_player:
            if self.animation.rect.centerx > player.animation.rect.centerx:
                ai_dx = -const.ENEMY_SPEED
            if self.animation.rect.centerx < player.animation.rect.centerx:
                ai_dx = const.ENEMY_SPEED
            if self.animation.rect.centery > player.animation.rect.centery:
                ai_dy = -const.ENEMY_SPEED
            if self.animation.rect.centery < player.animation.rect.centery:
                ai_dy = const.ENEMY_SPEED
        
        # If the enemy is alive and not stunned, execute movement and attack.
        if self.animation.stats.alive: 
            if not self.animation.stats.stunned:
                self.move(ai_dx, ai_dy, obstacle_tiles)
                self.attack_the_player(dist, player)

            # Handle the enemy being hit and apply a stun effect.
            if self.animation.stats.hit:
                self.animation.stats.hit = False
                self.animation.stats.last_hit = pygame.time.get_ticks()
                self.animation.stats.stunned = True
                self.animation.stats.running = False
                self.animation.set_action(0) #0: idle
                
            if (pygame.time.get_ticks() - self.animation.stats.last_hit) > stun_cooldown:
                self.animation.stats.stunned = False


    def attack_the_player(self, dist, player):
        """
        Attacks the player if within a certain range and the player isn't already hit.
        """
        # If the player is within attack range and not already hit, reduce health and set the hit status.
        if dist < const.ATTACK_RANGE and not player.animation.stats.hit:
            player.animation.stats.health -= 10
            player.animation.stats.hit = True
            player.animation.stats.last_hit = pygame.time.get_ticks()