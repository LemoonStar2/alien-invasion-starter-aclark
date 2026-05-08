import pygame.font


class Score:
    """A class to manage the game score."""

    def __init__(self, screen):
        """Initialize the score."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Font settings
        self.font = pygame.font.SysFont(None, 36)
        self.text_color = (255, 255, 255)
        
        # Score
        self.score = 0
        self.score_image = self.font.render(f"Score: {self.score}", True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topleft = (10, 10)

    def add_alien_defeated(self):
        """Add 100 points when an alien is defeated."""
        self.score += 100
        self._update_score_image()

    def add_wave_cleared(self):
        """Add 400 points when all aliens are defeated."""
        self.score += 400
        self._update_score_image()

    def _update_score_image(self):
        """Render the current score."""
        self.score_image = self.font.render(f"Score: {self.score}", True, self.text_color)

    def draw_score(self):
        """Draw the score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
