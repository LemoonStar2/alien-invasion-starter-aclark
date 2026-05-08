import pygame.font


class GameOver:
    """A class to manage the game over screen."""

    def __init__(self, screen):
        """Initialize the game over screen."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Font settings
        self.font = pygame.font.SysFont(None, 100)
        self.text_color = (255, 255, 255)
        
        # Create the game over text
        self.game_over_image = self.font.render("GAME OVER", True, self.text_color)
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = self.screen_rect.center

    def draw_game_over(self):
        """Draw the game over overlay to the screen."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw the game over text
        self.screen.blit(self.game_over_image, self.game_over_rect)
