class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)#(25, 25, 112)
        self.ship_speed = 2
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 100

        # Star Settings
        self.star_speed = .5
        self.stars_allowed = 25

        # Alien Settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
