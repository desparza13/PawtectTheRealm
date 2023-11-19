from character import Character
import pygame
import config.constants as const
import math
import weapon
from music_controller import GameEventPublisher

class Boss(Character):
    """
    Concrete Product Class representing the Boss enemy character in the Pawtect the Realm game.
    This class inherits from the Character abstract base class.

    Attributes:
        boss_music_started
        publisher
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the Boss object with the same arguments as the Character class, and sets the
        flag for boss music to not started.
        """
        super().__init__(*args, **kwargs)
        self.boss_music_started = False
        
        
    def set_publisher(self, publisher: GameEventPublisher):
        """
        Sets the publisher for the boss to notify about game events such as starting and ending the boss fight.
        """
        self.publisher = publisher
        
        
    def move(self, dx, dy, obstacle_tiles):
        """
        Moves the boss character and checks for collisions with obstacles.
        """
        self.animation.stats.running = False
        # Is Boss moving?
        if dx!= 0 or dy != 0:
            self.animation.stats.running = True
                
        # Set the animation flip based on the direction of movement.
        self.animation.flip = dx < 0
            
        #Normalize diagonal speed
        if dx!= 0 and dy!=0:
            dx, dy = self.control_diagonal_speed(dx,dy)
        
        # Perform collision checks with the given obstacles.
        self.collide_with_obstacles(dx,dy,obstacle_tiles)
        
        
    def is_visible_on_screen(self, screen_scroll):
        """
        Checks if the boss is currently visible on screen.
        """
        screen_rect = pygame.Rect(screen_scroll[0], screen_scroll[1], const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        return self.animation.rect.colliderect(screen_rect)
    
    def manage_boss_music(self, screen_scroll):
        # Stop boss music and reset flag if the boss is not alive
        if not self.animation.stats.alive and self.boss_music_started:
            self.notify_boss_defeated()  
            self.boss_music_started = False
            
        # If the boss is alive, manage music based on visibility
        elif self.animation.stats.alive:
            # Start music if the boss becomes visible on screen
            if self.is_visible_on_screen(screen_scroll) and not self.boss_music_started:
                self.notify_boss_appeared()  
                self.boss_music_started = True
            # Stop music if the boss is no longer visible on screen
            elif not self.is_visible_on_screen(screen_scroll) and self.boss_music_started:
                self.notify_boss_defeated()  
                self.boss_music_started = False
                
                
    def ai(self, player, obstacle_tiles, screen_scroll, ballattack_image):
        """
        Defines the AI logic for the boss, including moving towards the player and attacking.
        """
        self.manage_boss_music(screen_scroll)

        clipped_line = ()
        stun_cooldown = 0
        ballattack = None
        ai_dx = 0
        ai_dy = 0
        
        # Reposition the boss based on screen scroll to keep it in the correct world position
        self.animation.rect.x += screen_scroll[0]
        self.animation.rect.y += screen_scroll[1]

        # Determine if the boss has a clear line of sight to the player
        line_of_sight = ((self.animation.rect.centerx, self.animation.rect.centery), (player.animation.rect.centerx, player.animation.rect.centery))
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                # Line of sight is blocked by an obstacle
                clipped_line = obstacle[1].clipline(line_of_sight)

        # Calculate distance to the player to determine if the boss should move or attack
        dist = math.sqrt((self.animation.rect.centerx - player.animation.rect.centerx)**2 + ((self.animation.rect.centery - player.animation.rect.centery)**2))
        
        # Determine boss's movement direction based on player's position if in range
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
        
        # Execute boss actions if alive and not stunned
        if self.animation.stats.alive: 
            if not self.animation.stats.stunned:
                # Move towards the player and attempt to attack
                self.move(ai_dx, ai_dy, obstacle_tiles)
                self.attack_the_player(dist, player)
                
                # Initiate a projectile attack if within range and cooldown has passed
                ballattack_cooldown = 700
                if dist < 500:
                    if pygame.time.get_ticks() - self.animation.stats.last_attack >= ballattack_cooldown:
                        ballattack = weapon.BallAttack(ballattack_image, self.animation.rect.centerx, self.animation.rect.centery, player.animation.rect.centerx, player.animation.rect.centery)
                        self.animation.stats.last_attack = pygame.time.get_ticks()

            # Reset boss stats if hit
            if self.animation.stats.hit:
                self.animation.stats.hit = False
                self.animation.stats.last_hit = pygame.time.get_ticks()
                self.animation.stats.stunned = True
                self.animation.stats.running = False
                self.animation.set_action(0) #0: idle
                
            if (pygame.time.get_ticks() - self.animation.stats.last_hit) > stun_cooldown:
                self.animation.stats.stunned = False
                
        # Return a BallAttack object if an attack was initiated, None otherwise
        return ballattack


    def attack_the_player(self, dist, player):
        """
        Initiates an attack on the player if within a certain range.
        """
        #check if the enemy is attacking the player
        if dist < const.ATTACK_RANGE and not player.animation.stats.hit:
            player.animation.stats.health -= 10
            player.animation.stats.hit = True
            player.animation.stats.last_hit = pygame.time.get_ticks()

    def notify_boss_appeared(self):
        """
        Notifies the game event publisher that the boss has appeared.
        """
        if self.publisher:
            self.publisher.start_boss_fight()

    def notify_boss_defeated(self):
        """
        Notifies the game event publisher that the boss has been defeated.
        """
        if self.publisher:
            self.publisher.end_boss_fight()


