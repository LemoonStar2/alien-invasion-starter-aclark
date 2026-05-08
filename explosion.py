import pygame
import time


class Explosion:
    """A class to manage explosion animation."""

    def __init__(self, screen, x, y):
        """Initialize the explosion at the given position."""
        self.screen = screen
        self.x = x
        self.y = y
        self.start_time = time.time()
        self.duration = 0.8  # Explosion lasts 0.8 seconds
        self.is_active = True
        
        # Create explosion frames
        self.frames = self._create_frames()
        self.num_frames = len(self.frames)

    def _create_frames(self):
        """Create 8 frames of explosion animation."""
        frames = []
        
        for frame_num in range(8):
            frame = pygame.Surface((120, 120), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0))
            
            # Calculate expansion and fade
            progress = frame_num / 8.0
            max_radius = 60
            radius = int(max_radius * progress)
            alpha = int(255 * (1 - progress * 0.5))  # Reduced fade rate for less transparency
            
            # Outer orange/red ring
            if radius > 0:
                color_outer = (255, int(100 - progress * 100), 0, alpha)
                pygame.draw.circle(frame, color_outer, (60, 60), radius, 3)
            
            # Inner yellow/orange rings
            inner_radius = int(radius * 0.7)
            if inner_radius > 0:
                color_inner = (255, 200, 50, int(alpha * 0.95))
                pygame.draw.circle(frame, color_inner, (60, 60), inner_radius)
            
            # Bright center
            center_radius = int(radius * 0.3)
            if center_radius > 0:
                color_center = (255, 255, 100, int(alpha * 0.9))
                pygame.draw.circle(frame, color_center, (60, 60), center_radius)
            
            frames.append(frame)
        
        return frames

    def update(self):
        """Update the explosion animation."""
        elapsed = time.time() - self.start_time
        
        if elapsed >= self.duration:
            self.is_active = False

    def draw(self):
        """Draw the current explosion frame."""
        if not self.is_active:
            return
        
        elapsed = time.time() - self.start_time
        frame_index = min(int((elapsed / self.duration) * self.num_frames), self.num_frames - 1)
        
        frame = self.frames[frame_index]
        self.screen.blit(frame, (self.x - 60, self.y - 60))
