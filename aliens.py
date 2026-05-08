import pygame
import time
import random


class aliens:
    """A class to manage a fleet of aliens."""

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.aliens = pygame.sprite.Group()
        self.direction = 1
        self.base_speed = 2.5
        self.speed = self.base_speed
        self.speed_boost = 0.5
        self.drop_speed = 50
        self._create_fleet()

    def _create_fleet(self):
        """Create three rows of aliens in a checkered pattern."""
        alien_width = 70
        alien_height = 45
        spacing = 30
        x_start = 40
        y_start = 35
        rows = 3
        cols = 6

        for row in range(rows):
            y = y_start + row * (alien_height + spacing)
            row_offset = (alien_width + spacing) // 2 if row % 2 else 0
            for col in range(cols):
                x = x_start + row_offset + col * (alien_width + spacing)
                self.aliens.add(self._Alien(self.screen, x, y, alien_width, alien_height))

    def _reset_fleet(self):
        """Reset the fleet to its original top row and starting direction."""
        self.direction = 1
        self.speed = self.base_speed
        self.aliens.empty()
        self._create_fleet()

    def update(self, respawn_allowed=True, alien_bullets=None, round_number=1):
        """Move the fleet right, then down, then left, then down."""
        if not self.aliens:
            if respawn_allowed:
                self._reset_fleet()
            return
        self.aliens.update(self.direction, self.speed, alien_bullets, round_number)
        self._check_edges()

    def _check_edges(self):
        """Check if any alien has reached a screen edge."""
        for alien in self.aliens.sprites():
            if alien.rect.right >= self.screen_rect.right or alien.rect.left <= 0:
                self._change_direction()
                break

    def _change_direction(self):
        """Drop the fleet and reverse direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.drop_speed
        self.direction *= -1
        self.speed += self.speed_boost

    def draw(self):
        """Draw all aliens to the screen."""
        for alien in self.aliens.sprites():
            alien.draw()

    class _Alien(pygame.sprite.Sprite):
        """A single alien in the fleet."""

        def __init__(self, screen, x, y, width, height):
            super().__init__()
            self.screen = screen
            self.width = width
            self.height = height
            self.rect = pygame.Rect(x, y, width, height)
            
            # Create animated frames
            self.frames = self._create_frames(width, height)
            self.current_frame = 0
            self.animation_start_time = time.time()
            self.frame_duration = 0.5  # 0.5 seconds per frame (4 frames = 2 seconds total)
            
            # Set initial image
            self.image = self.frames[0]

        def _create_frames(self, width, height):
            """Create 4 animated frames for the alien bug."""
            frames = []
            
            body_rect = pygame.Rect(width // 2 - 18, height // 2 - 10, 36, 20)
            eye_base_y = height // 2 - 6
            eye_base_x = width // 2
            antenna_base_y = height // 2 - 12
            antenna_length = 14

            for i in range(4):
                frame = pygame.Surface((width, height), pygame.SRCALPHA)
                frame.fill((0, 0, 0, 0))  # Transparent background

                # Main body remains the same size every frame
                pygame.draw.ellipse(frame, (0, 200, 50), body_rect)

                # Eyes blink and shift slightly for animation
                blink = 1 if i % 2 == 0 else 0
                eye_offset = 8
                left_eye_center = (eye_base_x - eye_offset, eye_base_y)
                right_eye_center = (eye_base_x + eye_offset, eye_base_y)
                left_eye_radius = 2 if blink else 1
                right_eye_radius = 2 if blink else 1
                pygame.draw.circle(frame, (255, 200, 0), left_eye_center, left_eye_radius)
                pygame.draw.circle(frame, (0, 0, 0), left_eye_center, 1)
                pygame.draw.circle(frame, (0, 200, 255), right_eye_center, right_eye_radius)
                pygame.draw.circle(frame, (0, 0, 0), right_eye_center, 1)

                # Antennae bend and wiggle
                antenna_curve = (-1) ** i * (i * 2)
                pygame.draw.line(frame, (100, 150, 100), (eye_base_x - 5, antenna_base_y), (eye_base_x - 8 + antenna_curve, antenna_base_y - antenna_length), 2)
                pygame.draw.line(frame, (100, 150, 100), (eye_base_x + 5, antenna_base_y), (eye_base_x + 8 + antenna_curve, antenna_base_y - antenna_length), 2)
                pygame.draw.circle(frame, (200, 220, 255), (eye_base_x - 8 + antenna_curve, antenna_base_y - antenna_length), 2)
                pygame.draw.circle(frame, (200, 220, 255), (eye_base_x + 8 + antenna_curve, antenna_base_y - antenna_length), 2)

                frames.append(frame)
            
            return frames

        def update(self, direction, speed, alien_bullets, round_number):
            """Update alien position and animation."""
            self.rect.x += direction * speed
            
            # Randomly shoot bullets (chance increases with round)
            shoot_chance = 0.001 + round_number * 0.001
            if random.random() < shoot_chance:
                self.shoot(alien_bullets)
            
            # Update animation frame every 0.5 seconds (cycles every 2 seconds total)
            elapsed = time.time() - self.animation_start_time
            frame_index = int(elapsed / self.frame_duration) % len(self.frames)
            self.current_frame = frame_index
            self.image = self.frames[self.current_frame]

        def shoot(self, alien_bullets):
            """Shoot a bullet downward."""
            from bullet import AlienBullet
            new_bullet = AlienBullet(self.screen, self)
            alien_bullets.add(new_bullet)

        def draw(self):
            self.screen.blit(self.image, self.rect)
