import config.constants as const 
from items import Item
from stats import Stats
from player import Player
from enemy import Enemy
from boss import Boss
from world import World

# TODO: fix process_data

class Garden(World):
    """
    A class that represents a garden level in the game. It processes the level data to place tiles, 
    obstacles, items, and characters. Inherits from the World class.
    """
    def process_data(self, data, tile_list, item_images, mob_animations) -> None:
        """
        Processes the level data for the garden level, creating tiles, items, and characters based on the data.
        """
        # Initialize the level length based on the data provided.
        self.level_length = len(data)

        # Iterate through each value in level data file.
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                # Get the image and rect for the current tile
                image = tile_list[tile]
                image_rect = image.get_rect()
                # Calculate the exact position for the tile
                image_x = x * const.TILE_SIZE
                image_y = y * const.TILE_SIZE
                # Center the tile using the calculated position
                image_rect.center = (image_x, image_y)
                # Store tile data including image and position
                tile_data = [image, image_rect, image_x, image_y]

                # Check the tile type and create corresponding objects
                #Obstacle
                if tile == 7:
                    self.obstacle_tiles.append(tile_data) #used for collision
                #Exit
                elif tile == 8:
                    self.exit_tile = tile_data
                #Bones
                elif tile == 9:
                    # Create an item and replace the tile image with a floor tile.
                    bone = Item(image_x, image_y, 0, item_images[0])
                    self.item_list.append(bone)
                    tile_data[0] = tile_list[0]
                #Potion
                elif tile == 10:
                    # Create an item and replace the tile image with a floor tile.
                    potion = Item(image_x, image_y, 1, [item_images[1]])
                    self.item_list.append(potion)
                    tile_data[0] = tile_list[0]
                # Player character (Kebo)
                elif tile == 11:
                    # Create an item and replace the tile image with a floor tile.
                    player = Player(image_x, image_y, mob_animations, 0, 1, Stats(100))
                    self.player = player
                    tile_data[0] = tile_list[0]
                #Enemies
                elif tile >= 12 and tile <= 16:
                    # Create an item and replace the tile image with a floor tile.
                    enemy = Enemy(image_x, image_y, mob_animations, tile - 11, 1, Stats(100))
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                #Boss
                elif tile == 17:
                    # Create an item and replace the tile image with a floor tile.
                    enemy = Boss(image_x, image_y, mob_animations, 6, 2, Stats(150))
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]

                # If the tile is not representing a blank space, add it to the map tiles.
                if tile >= 0: 
                    self.map_tiles.append(tile_data)

    