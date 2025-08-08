import pygame
import math
import random

class GemParticle:
    def __init__(self, x, y, color, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = 60  # frames
        self.age = 0
        self.size = random.randint(3, 8)
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.2  # gravity
        self.age += 1
        
    def draw(self, surface, camera_offset):
        if self.age < self.lifetime:
            alpha = 255 * (1 - self.age / self.lifetime)
            color_with_alpha = (*self.color, int(alpha))
            
            # Create a surface for the particle
            particle_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, (self.size//2, self.size//2), self.size//2)
            
            screen_x = self.x - camera_offset
            screen_y = self.y
            surface.blit(particle_surface, (screen_x, screen_y))

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
        
        # Particle effect
        self.particles = []
        self.creating_particles = False

    def create_diamond_gem(self, gem_type):
        """Create a single diamond gem sprite"""
        surface = pygame.Surface((48, 48), pygame.SRCALPHA)
        
        # Different colors for different gem types
        colors = {
            "ruby": (255, 50, 50),      # Red
            "emerald": (50, 255, 50),    # Green
            "sapphire": (50, 50, 255),   # Blue
            "diamond": (200, 200, 255),  # Light blue/white
            "amethyst": (150, 50, 255),  # Purple
        }
        
        gem_color = colors.get(gem_type, (200, 200, 255))
        self.gem_color = gem_color  # Store for particle effect
        
        # Create a diamond shape
        points = [
            (24, 4),   # Top point
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

    def create_particle_burst(self):
        """Create a burst of particles when gem is collected"""
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # Create multiple particles in a burst pattern
        for _ in range(20):  # 20 particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            particle = GemParticle(center_x, center_y, self.gem_color, velocity_x, velocity_y)
            self.particles.append(particle)
        
        self.creating_particles = True

    def update(self):
        # Only floating animation, no spinning
        self.float_offset += self.float_speed
        self.rect.y = self.original_y + int(5 * math.sin(self.float_offset))
        
        # Update particles
        if self.creating_particles:
            for particle in self.particles[:]:
                particle.update()
                if particle.age >= particle.lifetime:
                    self.particles.remove(particle)

    def draw_particles(self, surface, camera_offset):
        """Draw the particle effect"""
        for particle in self.particles:
            particle.draw(surface, camera_offset)

    def can_be_collected(self, player_rect):
        """Check if player is close enough to collect the gem"""
        distance = math.sqrt((self.rect.centerx - player_rect.centerx)**2 +
                           (self.rect.centery - player_rect.centery)**2)
        return distance <= self.collection_radius and not self.collected

    def collect(self):
        """Mark the gem as collected and create particle effect"""
        self.collected = True
        self.create_particle_burst()
        self.kill()