import pygame.font


class Button:
    """
    Class representing a button.
    """

    def __init__(self, ai_game, message):
        """
        Initialize button attributes.
        """
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Set the size and properties of the button.
        self.width, self.height = self.settings.button_size
        self.button_color = self.settings.button_color

        self.text_color = self.settings.button_text_color
        self.font = pygame.font.SysFont(None, self.settings.button_font_size)

        # Build buttons rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.message_image = None
        self.message_image_rect = None

        # Prep the button's message(needs to be done only once).
        self.prep_message(message)

    def prep_message(self, message):
        """
        Turn msg into a rendered image and center the text on the button.
        """
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        """
        Draw blank button and then draw the message.
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
