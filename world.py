from abc import ABC, abstractmethod
import pygame

class World():
    """
    Represents the game world in a 2D environment. This class serves as a base
    for creating different types of game worlds.

    Attributes:
        map_tiles (list): A list to hold the details of all the tiles in the world.
        obstacle_tiles (list): A list of tiles that act as obstacles in the world.
        exit_tile (object): A reference to the tile that acts as an exit or goal.
        item_list (list): A list of items that are present in the world.
        player (object): A reference to the player character in the world.
        character_list (list): A list of non-player characters, typically enemies.
    """

    def __init__(self) -> None:
        """
        Initializes the World object with empty structures for its components.
        """
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.character_list = []  # Enemy list

    @abstractmethod
    def process_data(self) -> None:
        """
        Abstract method to process world data. This method should be implemented
        in subclasses to define how world data is processed.
        """
        pass

    def update(self, screen_scroll:list) -> None:
        """
        Updates the position of all tiles in the world based on screen scrolling.
        """
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]  # Update x-coordinate
            tile[3] += screen_scroll[1]  # Update y-coordinate
            tile[1].center = (tile[2], tile[3])  # Update tile center position

    def draw(self, surface:pygame.Surface) -> None:
        """
        Draws the tiles of the world onto a given surface.
        """
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])  # Draw each tile on the surface
