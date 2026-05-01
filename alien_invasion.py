import sys
import random

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from aliens import aliens


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    bg_color = settings.bg_color
    ship = Ship(screen)
    bullets = pygame.sprite.Group()
    alien_fleet = aliens(screen)
    clock = pygame.time.Clock()

    def _check_events(ship, bullets):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    if len(bullets) < 3:
                        new_bullet = Bullet(screen, ship)
                        bullets.add(new_bullet)
                elif event.key == pygame.K_m:
                    ship.color_changing = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    ship.moving_left = False
                elif event.key == pygame.K_m:
                    ship.color_changing = False
        return True

    def _update_bullets(bullets):
        """Update position of bullets and get rid of old bullets."""
        bullets.update()

    def _update_screen(settings, screen, ship, bullets, alien_fleet, bg_color):
        """Update images on the screen and flip to the new screen."""
        screen.fill(bg_color)
        ship.blitme()
        alien_fleet.draw()
        for bullet in bullets:
            bullet.draw_bullet()
        pygame.display.flip()

    running = True
    while running:
        running = _check_events(ship, bullets)
        if running:
            ship.update()
            _update_bullets(bullets)
            alien_fleet.update()
            pygame.sprite.groupcollide(bullets, alien_fleet.aliens, True, True)
            if not alien_fleet.aliens:
                alien_fleet._reset_fleet()
            _update_screen(settings, screen, ship, bullets, alien_fleet, bg_color)
            clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()
