import pygame
import config.constants as const
from button import Button
from items import Item

# -- SCALE IMAGES -- 
def scale_img(image, scale):
    """
    Returns a scaled image.
    """
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))

# -- LOAD BUTTON IMAGES --
def load_button_images() -> dict:
   """
    Returns a list of button images.
   """
   # Returns button images
   button_images = {
       "restart": scale_img(pygame.image.load(const.RESTART_BUTTON).convert_alpha(),const.BUTTON_SCALE),
       "exit": scale_img(pygame.image.load(const.EXIT_BUTTON).convert_alpha(),const.BUTTON_SCALE),
       "start": scale_img(pygame.image.load(const.START_BUTTON).convert_alpha(),const.BUTTON_SCALE),
       "resume": scale_img(pygame.image.load(const.RESUME_BUTTON).convert_alpha(),const.BUTTON_SCALE)
   }
   return button_images

def create_buttons() -> dict:
    """
    Returns a dictionary of Button objects.
    """
    # Returns Button objects
    button_images = load_button_images()
    button_objects = {
        "restart_button": Button(const.MIDDLE_WIDTH-190, const.MIDDLE_HEIGHT-60, button_images["restart"]),
        "exit_button": Button(const.MIDDLE_WIDTH-105, const.MIDDLE_HEIGHT+40, button_images["exit"]),
        "start_button": Button(const.MIDDLE_WIDTH-150, const.MIDDLE_HEIGHT-90, button_images["start"]),
        "resume_button": Button(const.MIDDLE_WIDTH-175, const.MIDDLE_HEIGHT-120, button_images["resume"])
    }
    return button_objects

def load_heart_images() -> dict:
    """
    Returns a list of heart images.
    """
    # Returns heart images
    heart_images = {
        "heart_full": scale_img(pygame.image.load(const.HEART_FULL).convert_alpha(),const.ITEM_SCALE),
        "heart_half": scale_img(pygame.image.load(const.HEART_HALF).convert_alpha(),const.ITEM_SCALE),
        "heart_empty": scale_img(pygame.image.load(const.HEART_EMPTY).convert_alpha(),const.ITEM_SCALE)
    }
    return heart_images

def load_single_image(asset:str) -> pygame.Surface:
    """
    Returns a single image that represents the asset.
    """
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
    elif asset == "game_over":
        asset_image = pygame.image.load(const.GAME_OVER).convert_alpha()
        asset_image = pygame.transform.scale(asset_image, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    return asset_image

def load_four_frame_animation(asset:str) -> dict:
    """
    Returns a list of images that represent the animation of the asset.
    """
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
    """
    Returns a list of tile images depending on the level.
    """
    # Returns tile images depending on the level
    tile_images = []
    tile_path = const.DUNGEON_TILE_PATH
    number_of_tiles = const.DUNGEON_TILE_TYPES
    if level <= 3 or level == 7:
        tile_path = const.GARDEN_TILE_PATH
        number_of_tiles = const.GARDEN_TILE_TYPES
    
    for i in range(number_of_tiles):
        img = pygame.image.load(tile_path + str(i) + ".png").convert_alpha()
        img = pygame.transform.scale(img, (const.TILE_SIZE, const.TILE_SIZE))
        tile_images.append(img)

    return tile_images

def load_mob_animations() -> list:
    """
    Returns a list of lists of lists of images that represent the animations of
    the mobs.
    """
    mob_animations = []

    for mob in const.MOB_TYPES:
        #load character images
        animation_list = []
        for animation in const.ANIMATION_TYPES:
            #reset temporary list of images
            temp_list = []
            for i in range(4):
                image = pygame.image.load(f"{const.CHARACTERS_PATH}{mob}/{animation}/{i}.png").convert_alpha()
                image = scale_img(image, const.SCALE)
                temp_list.append(image)
            animation_list.append(temp_list)
        mob_animations.append(animation_list)

    return mob_animations

def create_score_bone(bone_images) -> pygame.Surface:
    """
    Returns score bone image.
    """
    # Returns score bone image
    return Item(const.SCREEN_WIDTH - 115, 26, 0, bone_images, True)