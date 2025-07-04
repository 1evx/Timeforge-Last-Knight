import pygame

class Platform(pygame.sprite.Sprite):
  def __init__(self, x, y, image_path):
    super().__init__()
    self.image = pygame.image.load(image_path).convert_alpha()
    self.rect = self.image.get_rect(topleft=(x, y))