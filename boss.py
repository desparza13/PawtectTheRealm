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
        stun_cooldown = 0
        ballattack = None
        ai_dx = 0
        ai_dy = 0
        
        # Reposition the boss based on screen scroll to keep it in the correct world position
        self.update_position_with_screen_scroll(screen_scroll)

        # Determine if the boss has a clear line of sight to the player
        line_of_sight = self.create_line_of_sight(player)
        visible_to_boss = self.is_player_visible(obstacle_tiles,line_of_sight)

        # Calculate distance to the player to determine if the boss should move or attack
        dist = self.calculate_distance_to_player(player)
        
        # Determine boss's movement direction based on player's position if in range
        should_move_towards_player = visible_to_boss and dist > const.RANGE
        ai_dx, ai_dy = self.determine_ai_movement(player, should_move_towards_player)
        
        # Execute boss actions if alive and not stunned
        ballattack = self.execute_ai_actions(ai_dx,ai_dy,obstacle_tiles, player, dist, ballattack_image, stun_cooldown)
                
        # Return a BallAttack object if an attack was initiated, None otherwise
        return ballattack
    
    def update_position_with_screen_scroll(self, screen_scroll):
        """
        Updates the boss's position based on the screen scroll.
        """
        self.animation.rect.x += screen_scroll[0]
        self.animation.rect.y += screen_scroll[1]

    def create_line_of_sight(self, player):
        """
        Creates a line of sight from the boss to the player for visibility checks.
        """
        return ((self.animation.rect.centerx, self.animation.rect.centery), (player.animation.rect.centerx, player.animation.rect.centery))
    
    def is_player_visible(self, obstacle_tiles, line_of_sight):
        """
        Checks if the player is visible to the boss, considering obstacles.
        """
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                 # Line of sight is blocked by an obstacle
                return False
        return True
    
    def calculate_distance_to_player(self, player):
        """
        Calculates the distance from the boss to the player.
        """
        return math.sqrt((self.animation.rect.centerx - player.animation.rect.centerx)**2 + 
                         ((self.animation.rect.centery - player.animation.rect.centery)**2))
        
    def determine_ai_movement(self, player,should_move_towards_player):
        """
        Determines the movement direction for the AI based on whether the player is visible and in range.
        """
        ai_dx, ai_dy = 0, 0
        if should_move_towards_player:
            if self.animation.rect.centerx > player.animation.rect.centerx:
                ai_dx = -const.ENEMY_SPEED
            if self.animation.rect.centerx < player.animation.rect.centerx:
                ai_dx = const.ENEMY_SPEED
            if self.animation.rect.centery > player.animation.rect.centery:
                ai_dy = -const.ENEMY_SPEED
            if self.animation.rect.centery < player.animation.rect.centery:
                ai_dy = const.ENEMY_SPEED
        return ai_dx, ai_dy
    
    def attack_with_ball(self,dist,ballattack_image, ballattack_cooldown,player):
        ''' 
        Handles the boss's ball attack
        '''
        ballattack = None
        if dist < 500:
            if pygame.time.get_ticks() - self.animation.stats.last_attack >= ballattack_cooldown:
                ballattack = weapon.BallAttack(ballattack_image, self.animation.rect.centerx, self.animation.rect.centery, player.animation.rect.centerx, player.animation.rect.centery)
                self.animation.stats.last_attack = pygame.time.get_ticks()
                
        return ballattack
    
    def handle_hit_stun(self):
        """
        Handles the boss being hit and potentially stunned.
        """
        if self.animation.stats.hit:
            self.animation.stats.hit = False
            self.animation.stats.last_hit = pygame.time.get_ticks()
            self.animation.stats.stunned = True
            self.animation.stats.running = False
            self.animation.set_action(0) #0: idle
    
    def execute_ai_actions(self, ai_dx, ai_dy, obstacle_tiles, player, dist, ballattack_image, stun_cooldown):
        """
        Executes the actions determined by the AI logic, including moving and attacking the player.
        """
        ballattack = None
        if self.animation.stats.alive: 
            if not self.animation.stats.stunned:
                # Move towards the player and attempt to attack
                self.move(ai_dx, ai_dy, obstacle_tiles)
                self.attack_the_player(dist, player)
                
                # Initiate a projectile attack if within range and cooldown has passed
                ballattack_cooldown = 700
                ballattack = self.attack_with_ball(dist, ballattack_image, ballattack_cooldown, player)
                
            # Reset boss stats if hit
            self.handle_hit_stun()
                
            if (pygame.time.get_ticks() - self.animation.stats.last_hit) > stun_cooldown:
                self.animation.stats.stunned = False
        
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


