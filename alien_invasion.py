import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button


def run_game():
    """
    Main function to be executed.
    """
    # Initialize game and create a screen object.
    pygame.init()
    # Initialize settings and screen object.
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")

    # create the Ship.
    ship = Ship(ai_settings, screen)
    # Make a group to store the bullets.
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    stats = GameStats(ai_settings)
    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship)
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button)


def main():
    print("Running the game")
    run_game()


if __name__ == "__main__":
    main()

