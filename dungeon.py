import config.constants as const 
from items import Item
from stats import Stats
from player import Player
from enemy import Enemy
from boss import Boss
from world import World

class Dungeon(World):
    """
    Dungeon is a subclass of World that is specialized for processing and setting up
    a dungeon environment in a game. It handles the creation of tiles, items, and characters,
    and places them in the game world based on a provided level data structure.
    """
    
    def process_data(self, data, tile_list, item_images, mob_animations):
        """
        Takes raw level data and processes it to populate the dungeon with tiles, items, and characters.
        """
        self.level_length = len(data) # Determine the horizontal length of the level based on the data provided.
        # Iterate over each row and column in the level data
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile] # Retrieve the image for the current tile
                image_rect = image.get_rect() # Get the image's rectangle for positioning
                image_x = x * const.TILE_SIZE # Calculate the actual x-coordinate in the dungeon
                image_y = y * const.TILE_SIZE # Calculate the actual y-coordinate in the dungeon
                image_rect.center = (image_x, image_y) # Position the center of the tile
                tile_data = [image, image_rect, image_x, image_y] # Bundle the tile data together

                # Determine actions based on the type of tile.
                #Obstacles
                if tile == 7: # Tile type for obstacles
                    self.obstacle_tiles.append(tile_data) # Append for collision detection
                #Exit
                elif tile == 8: # Tile type for level exit
                    self.exit_tile = tile_data # Set as the level's exit point
                #Bones
                elif tile == 9: # Tile type for a bone item
                    bone = Item(image_x, image_y, 0, item_images[0]) # Create a bone item
                    self.item_list.append(bone) # Add the item to the list of items
                    tile_data[0] = tile_list[0] # Replace the special tile with a regular floor tile
                #Potion
                elif tile == 10: # Tile type for a potion item.
                    potion = Item(image_x, image_y, 1, [item_images[1]]) # Create a potion item
                    self.item_list.append(potion) # Add the item to the list of items
                    tile_data[0] = tile_list[0] # Replace the special tile with a regular floor tile
                #Player
                elif tile == 11: # Tile type for the player character
                    player = Player(image_x, image_y, mob_animations, 0, 1, Stats(100)) # Create the player character (Kebo)
                    self.player = player # Set the player for the dungeon.
                    tile_data[0] = tile_list[0] # Replace the special tile with a regular floor tile
                #Enemies
                elif tile >= 12 and tile <= 16: # Tile types for various enemies
                    enemy = Enemy(image_x, image_y, mob_animations, tile - 11, 1, Stats(100)) # Create an enemy character
                    self.character_list.append(enemy) # Add the enemy to the list of characters
                    tile_data[0] = tile_list[0] # Replace the special tile with a regular floor tile
                #Boss
                elif tile == 17: # Tile type for the boss character
                    enemy = Boss(image_x, image_y, mob_animations, 6, 2, Stats(150)) # Create the boss character.
                    self.character_list.append(enemy) # Add the boss to the list of characters
                    tile_data[0] = tile_list[0]

                if tile >= 0: # blank spaces in map are represented with -1
                    self.map_tiles.append(tile_data)

    