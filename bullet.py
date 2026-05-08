import pygame
import random
import time


class Particle(pygame.sprite.Sprite):
    """A particle effect for bullet fire."""
    
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)  # Random x velocity
        self.vy = random.uniform(-4, -1)  # Random y velocity (upward)
        self.lifetime = 0.3  # Seconds
        self.creation_time = time.time()
        self.size = random.randint(2, 5)
        self.color = random.choice([(255, 200, 0), (255, 100, 0), (255, 150, 50)])
    
    def update(self):
        """Move the particle and remove if lifetime expired."""
        self.x += self.vx
        self.y += self.vy
        
        elapsed = time.time() - self.creation_time
        if elapsed > self.lifetime:
            self.kill()
    
    def draw(self, screen):
        """Draw the particle."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


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
        self.speed = -18

    def update(self):
        """Move the bullet up the screen."""
        self.rect.y += self.speed
        # Remove the bullet if it goes off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)