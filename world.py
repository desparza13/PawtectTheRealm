from abc import ABC, abstractmethod
from items import Item
from player import Player
from stats import Stats
from enemy import Enemy

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

    @abstractmethod
    def setup_tiles(self, tile, tile_data, tile_list, item_images, mob_animations) -> None:
        """
        Abstract method to setup tiles in the world. This method should be implemented
        in subclasses to define which tiles are setup in the world.
        """
        pass

    def update(self, screen_scroll) -> None:
        """
        Updates the position of all tiles in the world based on screen scrolling.
        """
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]  # Update x-coordinate
            tile[3] += screen_scroll[1]  # Update y-coordinate
            tile[1].center = (tile[2], tile[3])  # Update tile center position

    def draw(self, surface) -> None:
        """
        Draws the tiles of the world onto a given surface.
        """
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])  # Draw each tile on the surface

    def handle_colliding_tile(self, tile, tile_data) -> None:
        """
        Handles the creation of colliding tiles (obstacles and exits) on the map.
        """
        if tile == 7:
            self.obstacle_tiles.append(tile_data) # Obstacle
        else:
            self.exit_tile = tile_data # Exit

    def handle_items(self, tile, tile_data, item_images, tile_list) -> None:
        """
        Handles the creation of items on the map.
        """
        if tile == 9: # Bone
            bone = Item(tile_data[2], tile_data[3], 0, item_images[0])
            self.item_list.append(bone)
            
        else: # Potion
            potion = Item(tile_data[2], tile_data[3], 1, [item_images[1]])
            self.item_list.append(potion)

        tile_data[0] = tile_list[0]

    def handle_enemies(self, tile, tile_data, mob_animations, tile_list) -> None:
        """
        Handles the creation of enemies on the map.
        """
        enemy = Enemy(tile_data[2], tile_data[3], mob_animations, tile - 11, 1, Stats(120))
        self.character_list.append(enemy)
        tile_data[0] = tile_list[0] 

    def handle_player(self, tile_data, mob_animations, tile_list) -> None:
        """
        Handles the creation of the player character on the map.
        """
        player = Player(tile_data[2], tile_data[3], mob_animations, 0, 1, Stats(100))
        self.player = player
        tile_data[0] = tile_list[0]