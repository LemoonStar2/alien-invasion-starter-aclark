import pygame


class aliens:
    """A class to manage a fleet of aliens."""

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.aliens = pygame.sprite.Group()
        self.direction = 1
        self.speed = 2
        self.drop_speed = 20
        self._create_fleet()

    def _create_fleet(self):
        """Create a row of 6 aliens at the top of the screen."""
        alien_width = 50
        alien_height = 30
        spacing = 20
        x_start = 50
        y_start = 40

        for alien_number in range(6):
            x = x_start + alien_number * (alien_width + spacing)
            y = y_start
            self.aliens.add(self._Alien(self.screen, x, y, alien_width, alien_height))

    def update(self):
        """Move the fleet right, then down, then left, then down."""
        self.aliens.update(self.direction)
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

    def draw(self):
        """Draw all aliens to the screen."""
        for alien in self.aliens.sprites():
            alien.draw()

    class _Alien(pygame.sprite.Sprite):
        """A single alien in the fleet."""

        def __init__(self, screen, x, y, width, height):
            super().__init__()
            self.screen = screen
            self.color = (0, 255, 0)
            self.image = pygame.Surface((width, height))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self, direction):
            self.rect.x += direction * 2

        def draw(self):
            self.screen.blit(self.image, self.rect)
