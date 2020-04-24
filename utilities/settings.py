import random


class Settings:
    """
    A class to store all settings for Alien Invasion.
    """
    def __init__(self):
        """
        Initialize the game's settings.
        """
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 2
        self.alien_image_path = "images/alien.bmp"
        self.ship_image_path = "images/ship.bmp"
        self.high_score = 0

        # Scoreboard settings.
        self.scoreboard_text_color = (30, 30, 30)
        self.scoreboard_font_size = 48

        # Bullet settings.
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 30
        # Play button settings.
        self.button_size = (200, 50)
        self.button_color = (0, 255, 0)
        self.button_text_color = (255, 255, 255)
        self.button_font_size = 48

        # alien_settings.
        self.fleet_drop_speed = 10

        # Game settings.
        self.speedup_scale = 1.1

        self.score_scale = 1.5

        # fleet direction of 1 represents right, -1 represents left.
        self.fleet_direction = random.choice((-1, 1))
        # Reward of killing one alien.
        self.alien_reward = 50

        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

    def reset_dynamic_settings(self):
        """
        Reset dynamic settings.
        """
        # Reward of killing one alien.
        self.alien_reward = 50

        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet direction of 1 represents right, -1 represents left.
        self.fleet_direction = random.choice((-1, 1))
        
    def increase_speed(self):
        """
        Increase speed settings.
        """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_reward = int(self.alien_reward * self.score_scale)
