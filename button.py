import pygame

class Button():
    """
    A simple button class that can detect mouseover and click events.

    Attributes:
        image (pygame.Surface): The image of the button to be displayed.
        rect (pygame.Rect): The rectangle defining the button's position and size.
    """
    def __init__(self,x, y, image) -> None:
        """
        Initializes the button with an image and position.
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self, surface):
        """
        Draws the button on the specified surface and returns True if the button is clicked.
        """
        action = False
        
        # Get the current position of the mouse.
        pos = pygame.mouse.get_pos()
        
        # Check if the mouse is over the button and if it is clicked.
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]: # [0] corresponds to the left mouse button.
                action = True
                
        # Blit the button image at the specified position on the given surface.
        surface.blit(self.image, self.rect)
        
        return action # If the button was clicked, return True.