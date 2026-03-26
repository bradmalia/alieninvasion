import sys
import pygame
import random
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()
        # Sounds
        self.laser_sound = pygame.mixer.Sound("sounds/laser.wav")
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion_medium.wav")
        self.ship_explosion = pygame.mixer.Sound("sounds/explosion_gameover_short.wav")
        self.game_over = pygame.mixer.Sound("sounds/explosion_gameover_long.wav")
        self.victory_tune = pygame.mixer.Sound("sounds/victory_tune.wav")

        self.alien_taunts = [
            pygame.mixer.Sound("sounds/alien_voice_1.wav"),
            pygame.mixer.Sound("sounds/alien_voice_2.wav"),
            pygame.mixer.Sound("sounds/alien_voice_3.wav"),
        ]

        # Schedule the first random taunt
        now = pygame.time.get_ticks()
        self._next_taunt_at = now + random.randint(3000, 7000)  # 3–7 sec

        pygame.mixer.music.load("sounds/dark_space_battle.ogg")
        pygame.mixer.music.play(-1)  # loops forever

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_width = self.screen.get_rect().height
        # self.settings.ship_speed = self.settings.screen_width * 0.0100
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics
        self.stats = GameStats(self)

        self.stars = pygame.sprite.Group()


        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _init_stars(self):
        """
        Pre-populate the screen with stars at random positions.
        Each star is represented as (x, y).
        """
        for _ in range(25):
            x = random.randint(0, self.settings.screen_width - 1)
            y = random.randint(0, self.settings.screen_height - 1)
            new_star = Star(self, x, y)
            self.stars.add(new_star)


    def _create_stars(self):
        if len(self.stars) < self.settings.stars_allowed:
            # 1 in 10 chance of adding a star
            if random.randint(0, 100) % 100 == 0:
                new_star = Star(self, 0, 0)
                self.stars.add(new_star)

    def _create_fleet(self):
        """Create te fleet of aliens."""
        #Make an alien
        alien = Alien(self)
        alien_width, alien_heigth = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_heigth) - ship_height)
        number_rows = available_space_y // (2 * alien_heigth)

        # Create the fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # def _create_star(self):
    #     star = Star(self)
    #     alien.rect.x = star.x
    #     self.stars.add(star)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.laser_sound.play()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship the the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _check_events(self):

        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
              self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _change_sound(self):
        """varies the ship blowing up sound"""
        num = random.randint(1,3)
        if num == 1:
            self.explosion_sound = pygame.mixer.Sound("sounds/explosion_small.wav")
        elif num == 2:
            self.explosion_sound = pygame.mixer.Sound("sounds/explosion_medium.wav")
        else:
            self.explosion_sound = pygame.mixer.Sound("sounds/explosion_big.wav")

    def _maybe_play_alien_taunt(self):
        if not self.stats.game_active:
            return
        now = pygame.time.get_ticks()
        if now >= self._next_taunt_at:
            # Pick a random taunt
            taunt = random.choice(self.alien_taunts)
            taunt.play()

            # Schedule the next one
            self._next_taunt_at = now + random.randint(3000, 7000)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        # Decrement ships left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.ship_explosion.play()
        else:
            pygame.mixer.music.stop()
            self.game_over.play()
            self.stats.game_active = False
        # Get rid of any remaining alients and bullets
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet
        self._create_fleet()
        self.ship.center_ship()


        #pause
        sleep(0.5)

    def _update_aliens(self):
        """Check if the fleet is at an edge then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Check for any bullets that have hit aliens
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.explosion_sound.play()
            self._change_sound()
            #speed up aliens slightly
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.victory_tune.play()
            self.bullets.empty()
            self._create_fleet()
            # speed up the aliens for the next level
            self.settings.alien_speed += .2
          #  print(len(self.bullets))

    def _update_stars(self):
        """Update position of stars and get rid of old stars."""
        self.stars.update()

        # Get rid of stars that have disappeared
        for star in self.stars.copy():
            if star.rect.bottom > self.settings.screen_height:
                self.stars.remove(star)
            #print(len(self.stars))

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)

        self._create_stars()
        for star in self.stars.sprites():
            star.draw_star()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()

    def run_game(self):
        """Start the main loop for the game."""
        stars = self._init_stars()
        while True:
            # Watch the keyboard and mouse events
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_stars()
                self._maybe_play_alien_taunt()
                # Make the most recently drawn screen visible.
                pygame.display.flip()
            # Redraw the screen during each pass though the loop
            self._update_screen()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()