from character import Character
import pygame
import config.constants as const
import math

class Enemy(Character):
    """
    Enemy is a subclass of Character representing enemy sprites in the game.
    It contains methods for AI behavior such as movement and attacking the player.

    """

    def move(self, dx, dy, obstacle_tiles) -> None:
        """
        Overrides the move method to handle enemy-specific movement logic, including
        collision detection and sprite flipping based on movement direction.
        """
        # Set running status based on movement.
        self.animation.stats.running = bool(dx or dy)
        
        # Flip sprite based on horizontal direction.
        self.animation.flip = dx < 0
            
        # Normalize diagonal movement.
        if dx and dy:
            dx, dy = self.control_diagonal_speed(dx, dy)
        
        # Handle collision with obstacles.
        self.collide_with_obstacles(dx, dy, obstacle_tiles)
    
    def ai(self, player, obstacle_tiles, screen_scroll) -> None:
        """
        Processes AI behavior, determining how the enemy moves and attacks the player.
        """
        # Reposition based on screen scroll.
        self.update_position_with_screen_scroll(screen_scroll)

        # Determine if the enemy can see the player.
        line_of_sight = self.create_line_of_sight(player)
        visible_to_enemy = self.is_player_visible(obstacle_tiles, line_of_sight)

        # Calculate distance to the player.
        dist = self.calculate_distance_to_player(player)

        # Determine movement based on AI logic.
        ai_dx, ai_dy = self.determine_ai_movement(player, visible_to_enemy, dist)
        
        # Execute movement and attacks if the enemy is active.
        self.execute_ai_actions(ai_dx, ai_dy, obstacle_tiles, player, dist)

    def update_position_with_screen_scroll(self, screen_scroll) -> None:
        """
        Updates the enemy's position based on the screen scroll.
        """
        self.animation.rect.x += screen_scroll[0]
        self.animation.rect.y += screen_scroll[1]

    def create_line_of_sight(self, player) -> tuple:
        """
        Creates a line of sight from the enemy to the player for visibility checks.
        """
        return ((self.animation.rect.centerx, self.animation.rect.centery), 
                (player.animation.rect.centerx, player.animation.rect.centery))

    def is_player_visible(self, obstacle_tiles, line_of_sight) -> bool:
        """
        Checks if the player is visible to the enemy, considering obstacles.
        """
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                return False
        return True

    def calculate_distance_to_player(self, player) -> float:
        """
        Calculates the distance from the enemy to the player.
        """
        return math.sqrt((self.animation.rect.centerx - player.animation.rect.centerx)**2 + 
                        (self.animation.rect.centery - player.animation.rect.centery)**2)

    def determine_ai_movement(self, player, visible_to_enemy, dist) -> tuple:
        """
        Determines the movement direction for the AI based on whether the player is visible and in range.
        """
        ai_dx, ai_dy = 0, 0
        if visible_to_enemy and dist > const.RANGE:
            ai_dx = -const.ENEMY_SPEED if self.animation.rect.centerx > player.animation.rect.centerx else const.ENEMY_SPEED
            ai_dy = -const.ENEMY_SPEED if self.animation.rect.centery > player.animation.rect.centery else const.ENEMY_SPEED
        return ai_dx, ai_dy

    def execute_ai_actions(self, ai_dx, ai_dy, obstacle_tiles, player, dist) -> None:
        """
        Executes the actions determined by the AI logic, including moving and attacking the player.
        """
        if self.animation.stats.alive and not self.animation.stats.stunned:
            self.move(ai_dx, ai_dy, obstacle_tiles)
            self.attack_the_player(dist, player)
            self.handle_hit_stun()
            
        if (pygame.time.get_ticks() - self.animation.stats.last_hit) > 0:
                self.animation.stats.stunned = False
                
    def handle_hit_stun(self) -> None:
        """
        Handles the enemy being hit and potentially stunned.
        """
        if self.animation.stats.hit:
            self.animation.stats.hit = False
            self.animation.stats.last_hit = pygame.time.get_ticks()
            self.animation.stats.stunned = True
            self.animation.stats.running = False
            self.animation.set_action(0) #idle
    
    def attack_the_player(self, dist, player) -> None:
        """
        Attempts to attack the player if they're within range and not already hit.
        """
        if dist < const.ATTACK_RANGE and not player.animation.stats.hit:
            player.animation.stats.health -= 10
            player.animation.stats.hit = True
            player.animation.stats.last_hit = pygame.time.get_ticks()
