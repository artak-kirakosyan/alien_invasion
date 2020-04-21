import sys
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
    # Create one alien to check the size and the number
    alien = Alien(ai_settings, screen)
    number_of_aliens_x = get_number_of_aliens_x(ai_settings, alien.rect.width)
    number_of_rows = get_number_of_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the fleet of the aliens.
    for row_number in range(number_of_rows):
        for alien_number in range(number_of_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_key_down_events(event, ai_settings, screen, ship, bullets):
    """
    Respond to key presses.
    """
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


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


def check_events(ai_settings, screen, ship, bullets):
    """
    Respond to key presses and mouse events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)


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
    """Respond to bullet-alien collisions"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy all bullets and create a new fleet.
        # bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """
    Fire a bullet if the limit is not yet reached.
    """
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, ship, bullets, aliens):
    """
    Update images on the screen and flip to the new screen.
    """
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
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


def update_aliens(ai_settings, aliens):
    """
    Check if the fleet is at an edge, and then update the positions
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
