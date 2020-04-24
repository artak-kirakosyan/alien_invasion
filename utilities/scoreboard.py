import pygame.font
from pygame.sprite import Group
from utilities.ship import Ship


class Scoreboard:
    """
    A class to report the score.
    """

    def __init__(self, ai_game):
        """
        Initialize score-keeping attributes.
        """
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats

        # Font settings.
        self.text_color = self.settings.scoreboard_text_color
        self.font = pygame.font.SysFont(None, self.settings.scoreboard_font_size)

        self.score_image = None
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.level_image = None
        self.level_rect = None
        self.ships = None

        # render all images to be displayed
        self.prep_all()

    def prep_all(self):
        """
        Prepare all rendered images
        """
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """
        Turn the score into a rendered image.
        """
        rounded_score = int(round(self.stats.score, -1))
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """
        Turn the high score into a rendered image.
        """
        rounded_score = int(round(self.stats.high_score, -1))
        high_score_str = "Highest Score: {:,}".format(rounded_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top center of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def prep_level(self):
        """
        Turn the level into a rendered image.
        """
        level_str = "Level: {:,}".format(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.top + 30

    def prep_ships(self):
        """
        Show how many ships are left.
        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number*ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """
        Draw the score.
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
