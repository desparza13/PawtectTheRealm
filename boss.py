from character import Character
import pygame
import config.constants as const
import math
import weapon

# TODO: add docstrings to refactorized methods

class Boss(Character):
    """
    Concrete Product Class representing the Boss enemy character in the Pawtect the Realm game.
    This class inherits from the Character abstract base class.

    Attributes:
        None
    """
    def move(self, dx, dy, obstacle_tiles):
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
          
    def ai(self, player, obstacle_tiles, screen_scroll, ballattack_image):
        clipped_line = ()
        stun_cooldown = 0
        ballattack = None
        ai_dx = 0
        ai_dy = 0
        #reposition the mobs based on screen scroll
        self.animation.rect.x += screen_scroll[0]
        self.animation.rect.y += screen_scroll[1]

        #create a line of sight from the enemy to the player
        line_of_sight = ((self.animation.rect.centerx, self.animation.rect.centery), (player.animation.rect.centerx, player.animation.rect.centery))
        #check if the line of sight collides with any obstacle
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)


        # check distance to player
        dist = math.sqrt((self.animation.rect.centerx - player.animation.rect.centerx)**2 + ((self.animation.rect.centery - player.animation.rect.centery)**2))
        # if there's no intersection, then the enemy is going to go towards the player
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
        
        if self.animation.stats.alive: 
            if not self.animation.stats.stunned:
                #move towards the player
                self.move(ai_dx, ai_dy, obstacle_tiles)
                #attack the player
                self.attack_the_player(dist, player)
                #boss enemies shoot ballattacks
                ballattack_cooldown = 700
                if dist < 500:
                    if pygame.time.get_ticks() - self.animation.stats.last_attack >= ballattack_cooldown:
                        ballattack = weapon.BallAttack(ballattack_image, self.animation.rect.centerx, self.animation.rect.centery, player.animation.rect.centerx, player.animation.rect.centery)
                        self.animation.stats.last_attack = pygame.time.get_ticks()

            if self.animation.stats.hit:
                self.animation.stats.hit = False
                self.animation.stats.last_hit = pygame.time.get_ticks()
                self.animation.stats.stunned = True
                self.animation.stats.running = False
                self.animation.set_action(0) #0: idle
                
            if (pygame.time.get_ticks() - self.animation.stats.last_hit) > stun_cooldown:
                self.animation.stats.stunned = False
        return ballattack


    def attack_the_player(self, dist, player):
        #check if the enemy is attacking the player
        if dist < const.ATTACK_RANGE and not player.animation.stats.hit:
            player.animation.stats.health -= 10
            player.animation.stats.hit = True
            player.animation.stats.last_hit = pygame.time.get_ticks()