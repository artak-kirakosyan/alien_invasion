import random
import configparser


class Settings:
    """
    A class to store all settings for Alien Invasion.
    """
    def __init__(self):
        """
        Initialize the game's settings.
        """
        self.config_path = "utilities/config.ini"

        self.configs = configparser.ConfigParser()
        self.configs.read(self.config_path)

        # Screen settings.
        self.screen_width = int(self.configs["DEFAULT"]["screen_width"])
        self.screen_height = int(self.configs["DEFAULT"]["screen_height"])
        self.bg_color = [int(i) for i in self.configs["DEFAULT"]["bg_color"].split(", ")]
        self.ship_limit = int(self.configs["DEFAULT"]["ship_limit"])
        self.alien_image_path = self.configs["DEFAULT"]["alien_image_path"]
        self.ship_image_path = self.configs["DEFAULT"]["ship_image_path"]
        self.high_score = int(self.configs["DEFAULT"]["high_score"])
        # Reward of killing one alien.
        self.alien_reward = int(self.configs["DEFAULT"]["alien_reward"])
        self.score_scale = float(self.configs["DEFAULT"]["score_scale"])
        self.fleet_drop_speed = int(self.configs["DEFAULT"]["fleet_drop_speed"])

        # Bullet settings.
        self.bullet_width = int(self.configs["bullet"]["bullet_width"])
        self.bullet_height = int(self.configs["bullet"]["bullet_height"])
        self.bullet_color = [int(i) for i in self.configs["bullet"]["bullet_color"].split(", ")]
        self.bullets_allowed = int(self.configs["bullet"]["bullets_allowed"])

        # Speed settings.
        self.ship_speed_factor = float(self.configs["speed"]["ship_speed_factor"])
        self.alien_speed_factor = float(self.configs["speed"]["alien_speed_factor"])
        self.bullet_speed_factor = float(self.configs["speed"]["bullet_speed_factor"])
        self.speedup_scale = float(self.configs["speed"]["speedup_scale"])

        # Play button settings.
        self.button_size = [int(i) for i in self.configs["button"]["button_size"].split(", ")]
        self.button_color = [int(i) for i in self.configs["button"]["button_color"].split(", ")]
        self.button_text_color = [int(i) for i in self.configs["button"]["button_text_color"].split(", ")]
        self.button_font_size = int(self.configs["button"]["button_font_size"])

        # Scoreboard settings.
        self.scoreboard_text_color = [int(i) for i in self.configs["scoreboard"]["scoreboard_text_color"].split(", ")]
        self.scoreboard_font_size = int(self.configs["scoreboard"]["scoreboard_font_size"])

        # fleet direction of 1 represents right, -1 represents left.
        self.fleet_direction = random.choice((-1, 1))

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

    def update_high_score(self, ai_game):
        """
        Update the config file with new high score.
        """
        if ai_game.stats.high_score > self.high_score:
            self.configs["DEFAULT"]["high_score"] = str(ai_game.stats.high_score)
            with open(self.config_path, 'w') as configfile:
                self.configs.write(configfile)
