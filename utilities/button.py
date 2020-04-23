import pygame.font


class Button:
    """
    Class representing a button.
    """

    def __init__(self, settings, screen, message):
        """
        Initialize button attributes.
        """
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the size and properties of the button.
        self.width, self.height = (200, 50)
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build buttons rect object and center it.

        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

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
