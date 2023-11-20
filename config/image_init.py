import pygame
import config.constants as const
from button import Button

# -- SCALE IMAGES -- 
def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))

# -- LOAD BUTTON IMAGES --
def load_button_images() -> dict:
   # Returns button images
   button_images = {
       "restart": scale_img(pygame.image.load(const.RESTART_BUTTON).convert_alpha(),const.BUTTON_SCALE),
       "exit": scale_img(pygame.image.load(const.EXIT_BUTTON).convert_alpha(),const.BUTTON_SCALE),
       "start": scale_img(pygame.image.load(const.START_BUTTON).convert_alpha(),const.BUTTON_SCALE),
       "resume": scale_img(pygame.image.load(const.RESUME_BUTTON).convert_alpha(),const.BUTTON_SCALE)
   }
   return button_images

def create_buttons() -> dict:
    # Returns Button objects
    button_images = load_button_images()
    button_objects = {
        "restart_button": Button(const.MIDDLE_WIDTH-175, const.MIDDLE_HEIGHT-60, button_images["restart"]),
        "exit_button": Button(const.MIDDLE_WIDTH-105, const.MIDDLE_HEIGHT+40, button_images["exit"]),
        "start_button": Button(const.MIDDLE_WIDTH-150, const.MIDDLE_HEIGHT-90, button_images["start"]),
        "resume_button": Button(const.MIDDLE_WIDTH-175, const.MIDDLE_HEIGHT-120, button_images["resume"])
    }
    return button_objects

def load_heart_images() -> dict:
    # Returns heart images
    heart_images = {
        "heart_full": scale_img(pygame.image.load(const.HEART_FULL).convert_alpha(),const.ITEM_SCALE),
        "heart_half": scale_img(pygame.image.load(const.HEART_HALF).convert_alpha(),const.ITEM_SCALE),
        "heart_empty": scale_img(pygame.image.load(const.HEART_EMPTY).convert_alpha(),const.ITEM_SCALE)
    }
    return heart_images

def load_single_image(asset:str) -> pygame.Surface:
    # Returns image
    asset_image = None
    if asset == "potion_red":
        asset_image = scale_img(pygame.image.load(const.POTION_PATH).convert_alpha(),const.POTION_SCALE)
    elif asset == "weapon" :
        asset_image = scale_img(pygame.image.load(const.WEAPON).convert_alpha(),const.WEAPON_SCALE)
    elif asset == "projectile":
        asset_image = scale_img(pygame.image.load(const.PROJECTILE).convert_alpha(),const.WEAPON_SCALE)
    elif asset == "ballattack":
        asset_image = scale_img(pygame.image.load(const.BALLATTACK_O).convert_alpha(),const.BALLATTACK_SCALE)
    elif asset == "cover":
        asset_image = pygame.image.load(const.COVER).convert_alpha()
        asset_image = pygame.transform.scale(asset_image, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    return asset_image

def load_four_frame_animation(asset:str) -> dict:
    asset_animation = []
    # Determine which asset to load (every image ends with '#.png')
    if asset == "bone":
        asset_path = const.BONE_PATH
        scale = const.ITEM_SCALE
    else:
        asset_path = const.BONE_PATH
        scale = const.ITEM_SCALE

    for i in range(4):
        img = pygame.image.load(asset_path + str(i) + ".png").convert_alpha() 
        img = scale_img(img, scale)
        asset_animation.append(img)
    
    return asset_animation

def load_tile_images(level:int) -> dict:
    # Returns tile images depending on the level
    tile_images = []
    tile_path = const.DUNGEON_TILE_PATH
    number_of_tiles = const.DUNGEON_TILE_TYPES
    if level <= 3:
        tile_path = const.GARDEN_TILE_PATH
        number_of_tiles = const.GARDEN_TILE_TYPES
    
    for i in range(number_of_tiles):
        img = pygame.image.load(tile_path + str(i) + ".png").convert_alpha()
        img = pygame.transform.scale(img, (const.TILE_SIZE, const.TILE_SIZE))
        tile_images.append(img)

    print('TILE IMAGES', tile_images)
    return tile_images
