import pygame
import random
import math


class GoldEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.alpha = 255
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0

        self.particles = []
        for _ in range(8):  # Number of sparkle particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            particle = {
                'x': 0,
                'y': 0,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': 15,
                'life': 8000,
                'max_life': 8000
            }
            self.particles.append(particle)

    def update(self):
        self.radius += 2
        self.alpha -= 10
        self.timer += 1

        if self.radius > self.max_radius or self.alpha <= 0:
            self.kill()
            return

        self.image.fill((0, 0, 0, 0))

        circle_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            circle_surface,
            (255, 215, 0),
            (self.radius, self.radius),
            self.radius
        )
        circle_surface.set_alpha(self.alpha)

        center_x = self.image.get_width() // 2 - self.radius
        center_y = self.image.get_height() // 2 - self.radius
        self.image.blit(circle_surface, (center_x, center_y))

        surface_center_x = self.image.get_width() // 2
        surface_center_y = self.image.get_height() // 2

        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1

            particle['vy'] += 0.1

            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue

            particle_alpha = int((particle['life'] / particle['max_life']) * 255)

            twinkle = 1 + 0.5 * math.sin(self.timer * 0.5 + particle['x'])
            actual_size = max(1, int(particle['size'] * twinkle))

            colors = [
                (255, 215, 0),  # Gold
                (255, 255, 100),  # Bright yellow
                (255, 200, 50),  # Orange-gold
                (255, 255, 200)  # Light yellow
            ]
            color = random.choice(colors)

            particle_x = int(surface_center_x + particle['x'])
            particle_y = int(surface_center_y + particle['y'])

            if (0 <= particle_x < self.image.get_width() and
                    0 <= particle_y < self.image.get_height()):

                # Create small surface for the particle
                particle_surface = pygame.Surface((actual_size * 2, actual_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    particle_surface,
                    color,
                    (actual_size, actual_size),
                    actual_size
                )
                particle_surface.set_alpha(particle_alpha)

                self.image.blit(particle_surface,
                                (particle_x - actual_size, particle_y - actual_size))

                if actual_size > 1:
                    center_surface = pygame.Surface((2, 2), pygame.SRCALPHA)
                    pygame.draw.circle(center_surface, (255, 255, 255), (1, 1), 1)
                    center_surface.set_alpha(min(255, particle_alpha + 50))
                    self.image.blit(center_surface, (particle_x - 1, particle_y - 1))