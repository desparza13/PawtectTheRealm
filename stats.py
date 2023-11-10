import math
import pygame
import constants as const

class Stats():
    """
    A class to maintain the status and statistics of a game character.

    Attributes:
        stunned (bool): Flag indicating whether the character is stunned.
        running (bool): Flag indicating whether the character is running.
        hit (bool): Flag indicating whether the character has recently been hit.
        alive (bool): Flag indicating whether the character is alive.
        health (int): Current health of the character.
        last_hit (int): Timestamp of the last time the character was hit.
        last_attack (int): Timestamp of the last time the character attacked.
    """
    def __init__(self, health):
        '''
        Initializes the Stats object with the given health value.
        '''
        #Status
        self.stunned = False
        self.running = False
        self.hit = False
        self.alive = True
        self.health = health
        #Times
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()

