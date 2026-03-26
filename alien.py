import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alient in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        original = pygame.image.load("images/alien.bmp")
        original.set_colorkey((0, 0, 0))

        scale_factor = 0.05  # 10% of original size
        width = int(original.get_width() * scale_factor)
        height = int(original.get_height() * scale_factor)
        self.image = pygame.transform.smoothscale(original, (width, height))
        self.rect = self.image.get_rect()

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

