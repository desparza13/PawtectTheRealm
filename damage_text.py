import pygame

class DamageText(pygame.sprite.Sprite):
    """
    A sprite for displaying damage text that floats up and fades out.

    Attributes:
        image (pygame.Surface): The rendered text surface.
        rect (pygame.Rect): The rectangle defining the position and boundary for the text.
        counter (int): A counter to track the lifetime of the text before it fades.
    """
    
    def __init__(self, x, y, damage, color, font) -> None:
        """
        Initialize the DamageText object with position, text, color, and font.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0 
        
    def update(self, screen_scroll) -> None:
        """
        Update the position of the text, moving it up and fading it out over time.
        """
        # Adjust the position based on the screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Move the damage text up to create a floating effect
        self.rect.y -= 1
        
        # Increment the counter and delete the text after a certain duration
        self.counter += 1
        if self.counter > 30: # If the counter exceeds the duration threshold
            self.kill() # Remove the sprite from all sprite groups