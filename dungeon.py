import config.constants as const 
from items import Item
from stats import Stats
from player import Player
from enemy import Enemy
from boss import Boss
from world import World

class Dungeon(World):

    def process_data(self, data, tile_list, item_images, mob_animations):
        self.level_length = len(data)
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * const.TILE_SIZE
                image_y = y * const.TILE_SIZE
                # to place the tiles in the centers of the rects
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                # CREATING ITEMS/CHARACTERS ON SPECIFIC TILES 
                if tile == 7:
                    self.obstacle_tiles.append(tile_data) #used for collision
                elif tile == 8:
                    self.exit_tile = tile_data
                elif tile == 9:
                    bone = Item(image_x, image_y, 0, item_images[0])
                    self.item_list.append(bone)
                    # replace the tile with a floor tile 
                    tile_data[0] = tile_list[0]
                elif tile == 10:
                    potion = Item(image_x, image_y, 1, [item_images[1]])
                    self.item_list.append(potion)
                    tile_data[0] = tile_list[0]
                elif tile == 11:
                    player = Player(image_x, image_y, mob_animations, 0, 1, Stats(100))
                    self.player = player
                    tile_data[0] = tile_list[0]
                elif tile >= 12 and tile <= 16:
                    enemy = Enemy(image_x, image_y, mob_animations, tile - 11, 1, Stats(100))
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 17:
                    enemy = Boss(image_x, image_y, mob_animations, 6, 2, Stats(150))
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]

                if tile >= 0: # blank spaces in map are represented with -1
                    self.map_tiles.append(tile_data)

    