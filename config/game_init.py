import pygame
from pygame import mixer
import config.constants as const

# -- PYGAME INITIALIZATIONS --
def init_config():
    mixer.init()
    pygame.init()

# -- LOAD MUSIC AND SOUNDS --
def load_audio_assets() -> dict:
    load_music()
    return load_sounds()

def load_sounds() -> dict:
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

def load_music():
    pygame.mixer.music.load(const.MUSIC_PATH)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1,0.0,5000)

# -- CREATE GAME WINDOW --
def window_config():
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Pawtect the Realm")
    return screen

# -- DEFINE FONT --
def define_font():
    return pygame.font.Font(const.LETTER_FONT, 20)
