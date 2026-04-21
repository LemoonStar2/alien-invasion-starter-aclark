import pygame
import random

class Ship:
    """A class to manage the ship."""

    def __init__(self, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen

        # Ship color
        self.color = (255, 255, 255)

        # Create a surface for the ship
        self.image = pygame.Surface((60, 40))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent
        # Draw the ship as a triangle
        pygame.draw.polygon(self.image, self.color, [(30, 0), (0, 40), (60, 40)])

        # Get the rect of the ship image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Movement flags
        self.moving_right = False
        self.moving_left = False

        # Ship speed
        self.speed = 2

        # Color changing flag
        self.color_changing = False

        # Color change timer
        self.color_timer = 0

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.speed

        # Handle color changing
        if self.color_changing:
            self.color_timer += 1
            if self.color_timer >= 10:
                self.change_color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                self.color_timer = 0

    def change_color(self, color):
        """Change the ship's color and redraw the image."""
        self.color = color
        self.image.fill((0, 0, 0))
        pygame.draw.polygon(self.image, self.color, [(30, 0), (0, 40), (60, 40)])