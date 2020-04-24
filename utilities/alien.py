import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """
    A class describing a single alien.
    """

    def __init__(self, ai_game):
        """
        Initialize the alien and set its starting position.
        """

        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.image_path = self.settings.alien_image_path

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()

        # Initial position: top left corner.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien's exact position.
        self.x = float(self.rect.x)

    def update(self):
        """
        Move the alien right or left.
        """
        self.x += self.settings.alien_speed_factor*self.settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """
        Draw the alien at the current location.
        """
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """
        Return True if alien is at the edge of the screen.
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        else:
            return False
