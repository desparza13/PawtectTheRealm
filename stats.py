import math
import pygame
import constants as const

class Stats():
    def __init__(self, health):
        #Status
        self.stunned = False
        self.running = False
        self.hit = False
        self.alive = True
        self.health = health
        #Times
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        
    
        
        
