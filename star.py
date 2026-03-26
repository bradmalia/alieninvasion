import pygame
import random
from pygame.sprite import Sprite
from settings import Settings

class Star(Sprite):
    """A class to represent a single alient in the fleet."""

    def __init__(self, ai_game, x, y):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        original = pygame.image.load("images/star.png")
        original.set_colorkey((0, 0, 0))

        scale_factor = 0.005  # 10% of original size
        width = int(original.get_width() * scale_factor)
        height = int(original.get_height() * scale_factor)
        self.image = pygame.transform.smoothscale(original, (width, height))
        self.rect = self.image.get_rect()
        if x == 0 and y == 0:
            self.rect.x = random.uniform(0,self.settings.screen_width)
        else:
            self.rect.x  = x
            self.rect.y = y

        # Store the stars exact horizontal position
        self.x = self.rect.x
        self.y = self.rect.y
        #print(self.x)

    def update(self):
        """Move the star down the screen."""
        self.y += self.settings.star_speed
        #update the rect position
        self.rect.y = self.y

    def draw_star(self):
        """Draw the bullet to the screen."""
        #pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)