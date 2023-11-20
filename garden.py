import config.constants as const
from enemy import Enemy 
from stats import Stats
from boss import Boss
from world import World

class Garden(World):
    """
    Garden is a subclass of World that is specialized for processing and setting up
    a garden environment in a game. It handles the creation of tiles, items, and characters,
    and places them in the game world based on a provided level data structure.
    """
    
    def process_data(self, data, tile_list, item_images, mob_animations) -> None:
        """
        Takes raw level data and processes it to populate the dungeon with tiles, items, and characters.
        """
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile] # Retrieve the image for the current tile
                image_rect = image.get_rect() 
                image_x = x * const.TILE_SIZE 
                image_y = y * const.TILE_SIZE 
                image_rect.center = (image_x, image_y) # Position the center of the tile
                tile_data = [image, image_rect, image_x, image_y] # Bundle the tile data together
                self.setup_tiles(tile, tile_data, tile_list, item_images, mob_animations)
                
    def setup_tiles(self, tile, tile_data, tile_list, item_images, mob_animations) -> None:
        """
        Sets up the tiles in the dungeon environment based on the type of tile.
        """
        # Colliding tiles
        if tile == 7 or tile == 8: 
            self.handle_colliding_tile(tile, tile_data) 
        # Items
        elif tile == 9 or tile == 10: 
            self.handle_items(tile, tile_data, item_images, tile_list)
        # Player            
        elif tile == 11:
            self.handle_player(tile_data, mob_animations, tile_list)
        # Enemies
        elif tile >= 12 and tile <= 16:
            self.handle_enemies(tile, tile_data, mob_animations, tile_list)
        # Extra characters
        elif tile >= 18 and tile <= 20: 
            self.handle_extra_characters(tile, tile_data, mob_animations, tile_list)
        # Place any tile 
        if tile >= 0:
            self.map_tiles.append(tile_data)

    def handle_extra_characters(self, tile, tile_data, mob_animations, tile_list) -> None:
        """
        Handles the creation of extra mobs (not sprites) in the garden level.
        For ease of implementation, these mobs will enter into the character list.
        """
        character = Enemy(tile_data[2], tile_data[3], mob_animations, tile - 11, 1, Stats(10))
        self.character_list.append(character)
        tile_data[0] = tile_list[0]
