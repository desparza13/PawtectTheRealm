import csv
import pygame
from pygame import mixer
from garden import Garden
from dungeon import Dungeon
import config.constants as const
from screenfade import ScreenFade

# -- PYGAME INITIALIZATIONS --
def init_config() -> None:
    """
    Initializes the pygame modules and mixer.
    """
    mixer.init()
    pygame.init()

# -- LOAD MUSIC AND SOUNDS --
def load_audio_assets() -> dict:
    """
    Loads all music and sound assets.
    """
    load_music()
    return load_sounds()

def load_sounds() -> dict:
    """
    Loads all sound assets individually.
    """
    sounds = {
            "shot_sound": pygame.mixer.Sound(const.PROJECTILE_SHOT_SOUND),
            "hit_sound": pygame.mixer.Sound(const.PROJECTILE_HIT_SOUND),
            "bone_sound": pygame.mixer.Sound(const.BONE_SOUND),
            "heal_sound": pygame.mixer.Sound(const.HEAL_SOUND),
            "game_over_sound": pygame.mixer.Sound(const.GAME_OVER_SOUND),
            "level_up_sound": pygame.mixer.Sound(const.LEVEL_UP_SOUND),
            "pause_sound": pygame.mixer.Sound(const.PAUSE_SOUND)
        }
    for sound in sounds.values():
        sound.set_volume(0.5)
    return sounds

def load_music() -> None:
    """
    Loads the background music.
    """
    pygame.mixer.music.load(const.MUSIC_PATH)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1,0.0,5000)

# -- CREATE GAME WINDOW AND ITS INFORMATION --
def window_config() -> pygame.Surface:
    """
    Creates the game window.
    """
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Pawtect the Realm")
    return screen

def draw_info_top_bar(screen, player, heart, level, font) -> None:
    """
    Draws the top bar of the game window; adds text, level, and lives.
    """
    #Draw the rect of the panel
    pygame.draw.rect(screen, const.PANEL_INFO, (0,0,const.SCREEN_WIDTH,50))
    pygame.draw.line(screen,const.WHITE,(0,50), (const.SCREEN_WIDTH,50)) #separate the panel info and the screen game
    #draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.animation.stats.health >= ((i+1)*20): #One full heart = 20 health
            screen.blit(heart["heart_full"], (10 + i * 50,0)) 
        elif(player.animation.stats.health %20 > 0) and half_heart_drawn == False:
            screen.blit(heart["heart_half"], (10 + i * 50,0))
            half_heart_drawn = True
        else:
            screen.blit(heart["heart_empty"], (10 + i * 50,0))

    #level
    if level == 7: 
        draw_text(screen, "The end!", font, const.WHITE, const.SCREEN_WIDTH/2, 17)
    else: 
        draw_text(screen, f"LEVEL: {level}", font, const.WHITE, const.SCREEN_WIDTH/2, 15)
    draw_text(screen, f" x {player.score}",font, const.WHITE, const.SCREEN_WIDTH - 100, 15)
    


# -- DEFINE FONT AND DRAW TEXT --
def define_font() -> pygame.font.Font:
    """
    Defines the font used in the game.
    """
    return pygame.font.Font(const.LETTER_FONT, 20)

def draw_text(screen, text, font, text_color, x, y) -> None:
    """
    Draws text onto the top bar of the screen.
    """
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y))

# -- GAME AND LEVEL FLOW --
def reset_groups(damage_text_group, projectile_group, item_group, ballattack_group) -> list:
    """
    Resets the game level.
    """
    damage_text_group.empty()
    projectile_group.empty()
    item_group.empty()
    ballattack_group.empty()

    return [damage_text_group, projectile_group, item_group, ballattack_group]

def restate_world(level) -> tuple:
    """
    Creates an empty world data list.
    """
    w_data = []
    world = Dungeon()
    for row in range(const.ROWS):
        r = [-1] * const.COLS
        w_data.append(r)

    load_in_level_data(level, w_data)
    if level <= 3 or level == 7:
        world = Garden()

    return w_data, world

def load_in_level_data(level, world_data) -> list:
    """
    Loads the level data from a csv file according to a specific level number.
    """
    level_path = const.LEVELS_PATH + str(level) + "_data.csv"
    print(level_path)
    with open(level_path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    return world_data

def next_level(level, world, world_data) -> None:
    """
    Advances the player to the next level.
    """
    level += 1
    world_data, world = restate_world(level)
    return level, world_data, world

def create_screen_fades(screen) -> tuple:
    """
    Creates a list of screen fade images.
    """
    intro_fade = ScreenFade(screen, 1, const.BLACK, 4)
    death_fade = ScreenFade(screen, 2, const.DARK_RED, 6)
    return intro_fade, death_fade

