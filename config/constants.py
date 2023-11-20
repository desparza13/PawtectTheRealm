
#Time
FPS = 60

#Screen sizes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MIDDLE_WIDTH = SCREEN_WIDTH // 2
MIDDLE_HEIGHT = SCREEN_HEIGHT // 2

#Colors
RED = (255,0,0)
DARK_BLUE = (58, 53, 151)
BG = (40, 25,25)
MENU_BG = (65,41,93)
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
DUNGEON_TILE_TYPES = 18
GARDEN_TILE_TYPES = 30
DUNGEON_TILE_PATH = 'assets/tiles/dungeon/'
GARDEN_TILE_PATH = 'assets/tiles/garden/'

#Level mapsize
ROWS = 150
COLS = 150

# Camera settings
SCROLL_THRESH = 200

# ------ EXISTING MOBS ------
ANIMATION_TYPES = ["idle", "run"]
MOB_TYPES = ["kebo","black_cat", "brown_cat","orange_cat", "budgie", "budgie2", "big_demon", "sol", "nia", "milo"]


# ------ LEVEL INFORMATION ------
LEVELS_PATH = 'levels/level'

# ------ ASSETS PATHS ------
# Music and sounds
AUDIO_PATH = 'assets/audio/'
MUSIC_PATH = AUDIO_PATH + 'music.wav'
BOSS_MUSIC = AUDIO_PATH + 'boss_music.mp3'
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

# Items
ITEMS_PATH = 'assets/items/'
HEART_FULL = ITEMS_PATH + 'heart_full.png'
HEART_HALF = ITEMS_PATH + 'heart_half.png'
HEART_EMPTY = ITEMS_PATH + 'heart_empty.png'
BONE_PATH = ITEMS_PATH + 'bone_'
POTION_PATH = ITEMS_PATH + 'potion_red.png'

# Characters
CHARACTERS_PATH = 'assets/characters/'
BIG_DEMON_IDLE = CHARACTERS_PATH + 'big_demon/idle/'
BIG_DEMON_RUN = CHARACTERS_PATH + 'big_demon/run/'
BLACK_CAT_IDLE = CHARACTERS_PATH + 'black_cat/idle/'
BLACK_CAT_RUN = CHARACTERS_PATH + 'black_cat/run/'
BROWN_CAT_IDLE = CHARACTERS_PATH + 'brown_cat/idle/'
BROWN_CAT_RUN = CHARACTERS_PATH + 'brown_cat/run/'
ORANGE_CAT_IDLE = CHARACTERS_PATH + 'orange_cat/idle/'
ORANGE_CAT_RUN = CHARACTERS_PATH + 'orange_cat/run/'
BUDGIE_IDLE = CHARACTERS_PATH + 'budgie/idle/'
BUDGIE_RUN = CHARACTERS_PATH + 'budgie/run/'
BUDGIE2_IDLE = CHARACTERS_PATH + 'budgie2/idle/'
BUDGIE2_RUN = CHARACTERS_PATH + 'budgie2/run/'
KEBO_IDLE = CHARACTERS_PATH + 'kebo/idle/'
KEBO_RUN = CHARACTERS_PATH + 'kebo/run/'

# Weapons (paths for decorator)
WEAPONS_PATH = 'assets/weapons/'
BALLATTACK_O = 'ballattack_o.png'
BALLATTACK_B = 'ballattack_b.png'
BALLATTACK_Y = 'ballattack_y.png'
PROJECTILE = WEAPONS_PATH + 'projectile.png'
WEAPON = WEAPONS_PATH + 'weapon1.png'

# Backgrounds
BACKGROUND_PATH = 'assets/backgrounds/'
COVER = BACKGROUND_PATH + 'cover.png'