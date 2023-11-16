#Time
FPS = 60

#Screen sizes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Colors
RED = (255,0,0)
BG = (40, 25,25)
MENU_BG = (130,0,0)
PANEL_INFO = (50,50,50)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (235,65,54)

#Player size
SCALE = 3
OFFSET = 12

#Character movement
SPEED = 5 #player
ENEMY_SPEED = 3.5

# Enemy range to player
RANGE = 50 #player
ATTACK_RANGE = 60

#Weapon size
WEAPON_SCALE = 1.5

#Projectile movement
PROJECTILE_SPEED = 10

#Item size
ITEM_SCALE = 3

#Potion size
POTION_SCALE = 2

#Button size
BUTTON_SCALE = 1

# BallAttack size and speed
BALLATTACK_SCALE = 1
BALLATTACK_SPEED = 4

#Tiles
TILE_SIZE = 16 * SCALE
TILE_TYPES = 18
GARDEN_TILE_TYPES = 18

#Level mapsize
ROWS = 150
COLS = 150

# Camera settings
SCROLL_THRESH = 200

# ------ ASSETS PATHS ------
# Music and sounds
AUDIO_PATH = 'assets/audio/'
MUSIC_PATH = AUDIO_PATH + 'music.wav'
PROJECTILE_SHOT_SOUND = AUDIO_PATH + 'projectile_shot.mp3'
PROJECTILE_HIT_SOUND = AUDIO_PATH + 'projectile_hit.wav'
BONE_SOUND = AUDIO_PATH + 'bone.mp3'
HEAL_SOUND = AUDIO_PATH + 'heal.wav'
GAME_OVER_SOUND = AUDIO_PATH + 'game_over.mp3'
LEVEL_UP_SOUND = AUDIO_PATH + 'level_up.mp3'
PAUSE_SOUND = AUDIO_PATH + 'pause.mp3'

# Letter font
LETTER_FONT = 'font/Minecraftia-Regular.ttf'

# Buttons
BUTTON_PATH = 'assets/buttons/'
START_BUTTON = BUTTON_PATH + 'button_start.png'
EXIT_BUTTON = BUTTON_PATH + 'button_exit.png'
RESTART_BUTTON = BUTTON_PATH + 'button_restart.png'
RESUME_BUTTON = BUTTON_PATH + 'button_resume.png'