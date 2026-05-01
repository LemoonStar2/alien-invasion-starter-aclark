import pygame

class Bullet(pygame.sprite.Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, screen, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.color = (255, 255, 255)
        self.speed = -25

    def update(self):
        """Move the bullet up the screen."""
        self.rect.y += self.speed
        # Remove the bullet if it goes off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)