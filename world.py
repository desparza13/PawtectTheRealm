import constants as const 
from items import Item
from character import Character

class World():
    def __init__(self) -> None:
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.character_list = [] #enemy list

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

                # CLASSIFYING TILES BASED ON THEIR VALUES
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
                    player = Character(image_x, image_y, 100, mob_animations, 0, False, 1)
                    self.player = player
                    tile_data[0] = tile_list[0]
                elif tile >= 12 and tile <= 17:
                    enemy = Character(image_x, image_y, 100, mob_animations, tile - 11, False, 1)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 17:
                    enemy = Character(image_x, image_y, 100, mob_animations, 6, True, 2)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]

                if tile >= 0: # blank spaces in map are represented with -1
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])