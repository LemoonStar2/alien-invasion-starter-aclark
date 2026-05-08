import sys
import random

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet, Particle
from aliens import aliens
from score import Score
from gameover import GameOver
from explosion import Explosion


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Alien Invasion")
    bg_color = settings.bg_color
    ship = Ship(screen)
    bullets = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    alien_fleet = aliens(screen)
    score = Score(screen)
    game_over_screen = GameOver(screen)
    explosion = None
    game_over = False
    round_number = 1
    lives = 3
    next_round_time = None
    round_delay_ms = 1200
    round_font = pygame.font.SysFont(None, 72)
    lives_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    def _check_events(ship, bullets, particles):
        """Respond to keypresses and mouse events."""
        controls_disabled = next_round_time is not None or explosion is not None or game_over
        if controls_disabled:
            ship.moving_right = False
            ship.moving_left = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if not controls_disabled and event.key == pygame.K_SPACE:
                    if len(bullets) < 5:
                        new_bullet = Bullet(screen, ship)
                        bullets.add(new_bullet)
                        # Create spark particles at the ship's tip
                        for _ in range(8):
                            particle = Particle(screen, ship.rect.centerx, ship.rect.top)
                            particles.add(particle)
                elif not controls_disabled:
                    if event.key == pygame.K_RIGHT:
                        ship.moving_right = True
                    elif event.key == pygame.K_LEFT:
                        ship.moving_left = True
                    elif event.key == pygame.K_m:
                        ship.color_changing = True
            elif event.type == pygame.KEYUP and not controls_disabled:
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

    def _create_space_background(settings):
        """Create a space-themed background surface."""
        background = pygame.Surface((settings.screen_width, settings.screen_height))

        # Draw a subtle vertical gradient from deep blue to purple.
        for y in range(settings.screen_height):
            ratio = y / settings.screen_height
            red = int(5 + ratio * 25)
            green = int(10 + ratio * 15)
            blue = int(35 + ratio * 80)
            pygame.draw.line(background, (red, green, blue), (0, y), (settings.screen_width, y))

        # Add star clusters and nebula-like glow.
        for _ in range(120):
            star_x = random.randrange(settings.screen_width)
            star_y = random.randrange(settings.screen_height)
            star_size = random.choice((1, 1, 2))
            star_color = random.choice([(255, 255, 255), (200, 220, 255), (180, 200, 255)])
            pygame.draw.circle(background, star_color, (star_x, star_y), star_size)

        for cx, cy, radius, color in [
            (180, 120, 100, (120, 40, 150, 50)),
            (620, 90, 120, (80, 20, 170, 45)),
            (420, 380, 140, (90, 30, 140, 40)),
            (150, 420, 110, (100, 60, 180, 35)),
        ]:
            nebula = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(nebula, color, (radius, radius), radius)
            background.blit(nebula, (cx - radius, cy - radius), special_flags=pygame.BLEND_ADD)

        return background

    def _check_alien_collision_with_ship(alien_fleet, ship):
        """Check if any aliens have reached the ship level or lower."""
        for alien in alien_fleet.aliens.sprites():
            if alien.rect.bottom >= ship.rect.top:
                return True
        return False

    def _draw_round_message(screen, font, round_number):
        """Draw a round announcement in the center of the screen."""
        message = font.render(f"Round {round_number}", True, (255, 255, 255))
        msg_rect = message.get_rect()
        msg_rect.center = screen.get_rect().center
        screen.blit(message, msg_rect)

    def _draw_lives(screen, font, lives):
        """Draw the current lives count at the top left of the screen."""
        message = font.render(f"Lives: {lives}", True, (255, 255, 255))
        msg_rect = message.get_rect()
        msg_rect.topleft = (10, 50)
        screen.blit(message, msg_rect)

    def _update_screen(settings, screen, ship, bullets, particles, alien_fleet, score, game_over_screen, explosion, game_over, bg_color, background, next_round_time, round_font, round_number, lives_font, lives):
        """Update images on the screen and flip to the new screen."""
        screen.blit(background, (0, 0))
        ship.blitme()
        alien_fleet.draw()
        for bullet in bullets:
            bullet.draw_bullet()
        for particle in particles:
            particle.draw(screen)
        score.draw_score()
        _draw_lives(screen, lives_font, lives)
        
        if explosion:
            explosion.draw()
        
        if next_round_time is not None:
            _draw_round_message(screen, round_font, round_number)
        
        if game_over:
            game_over_screen.draw_game_over()
        
        pygame.display.flip()

    background = _create_space_background(settings)

    running = True
    while running:
        running = _check_events(ship, bullets, particles)
        if running and not game_over:
            if next_round_time is None:
                ship.update()
                alien_fleet.update(respawn_allowed=True)
            else:
                alien_fleet.update(respawn_allowed=False)
            _update_bullets(bullets)
            particles.update()
            
            # Check if aliens have reached the ship
            if explosion is None and _check_alien_collision_with_ship(alien_fleet, ship):
                # Create explosion at ship position
                explosion = Explosion(screen, ship.rect.centerx, ship.rect.centery)
            
            # Update explosion if active
            if explosion:
                explosion.update()
                # Handle life loss and reset instead of game over if lives remain
                if not explosion.is_active:
                    if lives > 1:
                        lives -= 1
                        score.score = max(0, score.score - 2000)
                        score._update_score_image()
                        bullets.empty()
                        particles.empty()
                        alien_fleet._reset_fleet()
                        ship.moving_right = False
                        ship.moving_left = False
                        ship.rect.centerx = ship.screen_rect.centerx
                        ship.rect.bottom = ship.screen_rect.bottom
                        explosion = None
                    else:
                        game_over = True
            
            # Check for collisions and update score (only if explosion not happening)
            if explosion is None and not game_over:
                collisions = pygame.sprite.groupcollide(bullets, alien_fleet.aliens, True, True)
                if collisions:
                    for aliens_hit in collisions.values():
                        score.add_alien_defeated()
            
            # Check if fleet is cleared and schedule the next round
            if not alien_fleet.aliens and explosion is None and next_round_time is None:
                score.add_wave_cleared()
                round_number += 1
                next_round_time = pygame.time.get_ticks() + round_delay_ms

            # Spawn the next wave after a short delay
            if next_round_time is not None and pygame.time.get_ticks() >= next_round_time:
                alien_fleet._reset_fleet()
                next_round_time = None
        
        _update_screen(settings, screen, ship, bullets, particles, alien_fleet, score, game_over_screen, explosion, game_over, bg_color, background, next_round_time, round_font, round_number, lives_font, lives)
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()
