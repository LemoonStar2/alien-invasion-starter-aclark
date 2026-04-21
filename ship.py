import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen

        # Create a surface for the ship
        self.image = pygame.Surface((60, 40))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent
        # Draw the ship as a triangle
        pygame.draw.polygon(self.image, (255, 255, 255), [(30, 0), (0, 40), (60, 40)])

        # Get the rect of the ship image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)