import pygame
import math

class Projectile(pygame.sprite.Sprite):
  def __init__(self, x, y, angle, speed):
    super().__init__()
    self.image = pygame.Surface((10, 4))
    self.image.fill((255, 255, 0))
    self.rect = self.image.get_rect(center=(x, y))

    self.vx = math.cos(angle) * speed
    self.vy = math.sin(angle) * speed

  def update(self):
    self.rect.x += self.vx
    self.rect.y += self.vy

    if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
      self.kill()
