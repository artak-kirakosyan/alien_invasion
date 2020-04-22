import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def get_number_of_rows(ai_settings, ship_height, alien_height):
    """
    Determine the number of rows of aliens that fit on the screen.
    """
    available_space_y = ai_settings.screen_height - 3*alien_height - ship_height
    number_of_rows = int(available_space_y / (2*alien_height))
    return number_of_rows


def get_number_of_aliens_x(ai_settings, alien_width):
    """
    Determine the number of aliens that fit in a row.
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    Create one alien.
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """
    Create a full fleet of aliens.
    """
    # Create one alien to check the size and the number.
    alien = Alien(ai_settings, screen)
    number_of_aliens_x = get_number_of_aliens_x(ai_settings, alien.rect.width)
    number_of_rows = get_number_of_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the fleet of the aliens.
    for row_number in range(number_of_rows):
        for alien_number in range(number_of_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_key_down_events(event, ai_settings, screen, ship, bullets, stats, aliens):
    """
    Respond to key presses.
    """
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, stats)
    elif event.key == pygame.K_p:
        start_game(stats, aliens, bullets, ai_settings, screen, ship)


def check_key_up_events(event, ship):
    """
    Respond to key releases.
    """
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens):
    """
    Respond to key presses and mouse events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets)
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ai_settings, screen, ship, bullets, stats, aliens)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets):
    """
    Start the new game if play was clicked.
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(stats, aliens, bullets, ai_settings, screen, ship)


def start_game(stats, aliens, bullets, ai_settings, screen, ship):
    """
    Start a new game.
    """
    if not stats.game_active:

        stats.game_active = True
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bullets(bullets, aliens, ai_settings, screen, ship, ):
    """
    Update position of bullets and get rid of old ones.
    """
    # Update bullets position.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """
    Respond to bullet-alien collisions.
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy all bullets and create a new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets, stats):
    """
    Fire a bullet if the limit is not yet reached.
    """
    if len(bullets) < ai_settings.bullets_allowed and stats.game_active:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button):
    """
    Update images on the screen and flip to the new screen.
    """

    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    if stats.game_active:
        # Redraw all bullets behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        ship.blitme()
        aliens.draw(screen)

    else:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def check_fleet_edges(ai_settings, aliens):
    """
    Respond properly if any alien reached an edge.
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """
    Drop the entire fleet and change the fleet's direction.
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens, ship, stats, screen, bullets):
    """
    Check if the fleet is at an edge, and then update the positions.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Now check for alien ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        lose_a_life(ai_settings, stats, screen, ship, aliens, bullets)
    # Check if aliens hit the bottom.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def lose_a_life(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Respond to ship being hit by alien.
    """
    if stats.ships_left > 0:
        # Decrement the number of ships left.
        stats.ships_left -= 1
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    sleep(0.5)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Check if aliens hit the bottom.
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this a loosing a life.
            lose_a_life(ai_settings, stats, screen, ship, aliens, bullets)
            break
