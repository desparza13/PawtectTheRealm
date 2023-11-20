from config.constants import SPEED
import pygame

left = False
right = False
up = False
down = False
pause = False

def is_game_closed(event) -> bool:
    """
    Checks if the game is closed.
    """
    if event.type == pygame.QUIT:
        return False
    return True

def calculate_player_movement(left, right, down, up) -> tuple:
    """
    Calculates the player's movement.
    """
    dx = 0
    dy = 0
    if left:
        dx -= SPEED
    if right:
        dx += SPEED
    if down:
        dy += SPEED
    if up:
        dy -= SPEED
    return dx, dy

def check_keyboard(event) -> tuple:
    """
    Checks if the keyboard is pressed or not to update the player's movement.
    """
    global left, right, up, down, pause
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            left = True
        if event.key == pygame.K_d:
            right = True
        if event.key == pygame.K_w:
             up = True
        if event.key == pygame.K_s:
            down = True
        if event.key == pygame.K_ESCAPE:
            pause = True
    
            #Keyboard released
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            left = False
        if event.key == pygame.K_d:
            right = False
        if event.key == pygame.K_w:
            up = False
        if event.key == pygame.K_s:
            down = False

    return left, right, up, down, pause
