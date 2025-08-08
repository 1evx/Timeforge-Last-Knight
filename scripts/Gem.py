import pygame
import math


class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y, gem_type="diamond"):
        super().__init__()

        # Create a single diamond gem sprite
        self.image = self.create_diamond_gem(gem_type)
        self.rect = self.image.get_rect(center=(x, y))

        # Collection parameters
        self.collected = False
        self.collection_radius = 50  # Distance player needs to be to collect

        # Floating animation
        self.float_offset = 0
        self.float_speed = 0.05
        self.original_y = y

    def create_diamond_gem(self, gem_type):
        """Create a single diamond gem sprite"""
        surface = pygame.Surface((48, 48), pygame.SRCALPHA)

        # Different colors for different gem types
        colors = {
            "ruby": (255, 50, 50),  # Red
            "emerald": (50, 255, 50),  # Green
            "sapphire": (50, 50, 255),  # Blue
            "diamond": (200, 200, 255),  # Light blue/white
        }

        gem_color = colors.get(gem_type, (200, 200, 255))

        # Create a diamond shape
        points = [
            (24, 4),  # Top point
            (36, 20),  # Right point
            (24, 36),  # Bottom point
            (12, 20),  # Left point
        ]

        # Draw the main diamond shape
        pygame.draw.polygon(surface, gem_color, points)

        # Add a white border
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)

        # Add some sparkle/reflection
        pygame.draw.circle(surface, (255, 255, 255), (20, 16), 2)
        pygame.draw.circle(surface, (255, 255, 255), (28, 24), 1)

        # Add a highlight
        pygame.draw.circle(surface, (255, 255, 255), (18, 14), 1)

        return surface

    def update(self):
        # Only floating animation, no spinning
        self.float_offset += self.float_speed
        self.rect.y = self.original_y + int(5 * math.sin(self.float_offset))

    def can_be_collected(self, player_rect):
        """Check if player is close enough to collect the gem"""
        distance = math.sqrt((self.rect.centerx - player_rect.centerx) ** 2 +
                             (self.rect.centery - player_rect.centery) ** 2)
        return distance <= self.collection_radius and not self.collected

    def collect(self):
        """Mark the gem as collected"""
        self.collected = True
        self.kill()