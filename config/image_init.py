import pygame
import config.constants as const

# -- SCALE IMAGES -- 
def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))

# -- LOAD BUTTON IMAGES --
def load_button_images():
    # TODO return dictionary with button images
    pass