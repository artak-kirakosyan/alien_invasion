import sys
import pygame
import configparser
from time import sleep
from pygame.sprite import Group

from utilities.settings import Settings
from utilities.ship import Ship
from utilities.game_stats import GameStats
from utilities.button import Button
from utilities.scoreboard import Scoreboard
from utilities.bullet import Bullet
from utilities.alien import Alien


class AlienInvasion:
    """
    Class representing the game.
    """

    def __init__(self):
        """
       Initialize game object
        """

        # Initialize game and create a screen object.
        pygame.init()
        # Initialize settings and screen object.
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.play_button = Button(self, "Play")

        # create the Ship.
        self.ship = Ship(self.settings, self.screen)
        # Make a group to store the bullets.
        self.bullets = Group()
        self.aliens = Group()
        self.create_fleet()

        # Create a Game stats and scoreboard instance.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.game_paused = True

    def run_game(self):
        """
        Main function to be executed.
        """

        # Start the main loop for the game.
        while True:
            self.check_events()
            if self.stats.game_active and self.game_paused:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()

    def get_number_of_rows(self, ship_height, alien_height):
        """
        Determine the number of rows of aliens that fit on the screen.
        """
        available_space_y = self.settings.screen_height - 3*alien_height - ship_height
        number_of_rows = int(available_space_y / (2*alien_height))
        return number_of_rows

    def get_number_of_aliens_x(self, alien_width):
        """
        Determine the number of aliens that fit in a row.
        """
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_of_aliens_x = int(available_space_x / (2 * alien_width))
        return number_of_aliens_x

    def create_alien(self, alien_number, row_number):
        """
        Create one alien.
        """
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def create_fleet(self):
        """
        Create a full fleet of aliens.
        """
        # Create one alien to check the size and the number.
        alien = Alien(self)
        number_of_aliens_x = self.get_number_of_aliens_x(alien.rect.width)
        number_of_rows = self.get_number_of_rows(self.ship.rect.height, alien.rect.height)
        # Create the fleet of the aliens.
        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens_x):
                self.create_alien(alien_number, row_number)

    def check_key_down_events(self, event):
        """
        Respond to key presses.
        """
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_p:
            self.start_game()

    def check_key_up_events(self, event):
        """
        Respond to key releases.
        """
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_ESCAPE:
            self.game_paused = not self.game_paused

    def check_events(self):
        """
        Respond to key presses and mouse events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self.check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self.check_key_up_events(event)

    def check_play_button(self, mouse_pos):
        """
        Start the new game if play was clicked.
        """
        mouse_x, mouse_y = mouse_pos
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked:
            self.start_game()

    def start_game(self):
        """
        Start a new game.
        """
        if not self.stats.game_active:

            self.stats.game_active = True
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            # Empty the list of aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            self.sb.prep_all()
            # Create a new fleet and center the ship.
            self.create_fleet()
            self.ship.center_ship()

    def update_bullets(self):
        """
        Update position of bullets and get rid of old ones.
        """
        # Update bullets position.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        """
        Respond to bullet-alien collisions.
        """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_reward * len(aliens)
            self.sb.prep_score()
            self.check_high_score()

        if len(self.aliens) == 0:
            # Destroy all bullets and create a new fleet.
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            self.create_fleet()

    def fire_bullet(self):
        """
        Fire a bullet if the limit is not yet reached.
        """
        if len(self.bullets) < self.settings.bullets_allowed and self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_screen(self):
        """
        Update images on the screen and flip to the new screen.
        """

        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.sb.show_score()
        if self.stats.game_active:
            # Redraw all bullets behind ship and aliens.
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.ship.blitme()
            self.aliens.draw(self.screen)

        else:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def check_fleet_edges(self):
        """
        Respond properly if any alien reached an edge.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """
        Drop the entire fleet and change the fleet's direction.
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def update_aliens(self):
        """
        Check if the fleet is at an edge, and then update the positions.
        """
        self.check_fleet_edges()
        self.aliens.update()

        # Now check for alien ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.lose_a_life()
        # Check if aliens hit the bottom.
        self.check_aliens_bottom()

    def lose_a_life(self):
        """
        Respond to ship being hit by alien.
        """
        if self.stats.ships_left > 0:
            # Decrement the number of ships left.
            self.stats.ships_left -= 1
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        # Empty the list of aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        self.sb.prep_ships()

        # Create a new fleet and center the ship.
        self.create_fleet()
        self.ship.center_ship()

        sleep(0.5)

    def check_aliens_bottom(self):
        """
        Check if aliens hit the bottom.
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this a loosing a life.
                self.lose_a_life()
                break

    def check_high_score(self):
        """
        Check to see if there is a new high score.
        """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()
