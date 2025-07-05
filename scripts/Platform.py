import pygame

class Platform(pygame.sprite.Sprite):
  def __init__(self, x, y, image):
    super().__init__()

    if isinstance(image, str):
      self.image = pygame.image.load(image).convert_alpha()
    elif isinstance(image, pygame.Surface):
      self.image = image
    else:
      raise TypeError("Platform requires image as file path or pygame.Surface!")

    self.rect = self.image.get_rect(topleft=(x, y))