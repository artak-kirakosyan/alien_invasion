import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """
    A class to manage bullets fired from the ship.
    """

    def __init__(self, ai_game):
        """
        Create a bullet object at the ship's current position.
        """
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.centerx = ai_game.ship.rect.centerx
        self.rect.top = ai_game.ship.rect.top

        # store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

        self.color = self.settings.bullet_color
        self.speed_factor = self.settings.bullet_speed_factor

    def update(self):
        """
        Move the bullet up the screen.
        """
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the position
        self.rect.y = self.y

    def draw_bullet(self):
        """
        Draw the bullet on the screen.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
