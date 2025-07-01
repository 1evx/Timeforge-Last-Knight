import pygame

class ParallaxBackground:
  def __init__(self, layers, width, height):
    self.layers = []
    self.width = width
    self.height = height

    for image_path, speed in layers:
      image = pygame.image.load(image_path).convert_alpha()
      image = pygame.transform.scale(image, (width, height))
      self.layers.append({
        "image": image,
        "speed": speed,
        "x": 0
      })

  def update(self, camera_x):
    for layer in self.layers:
      layer["x"] = -camera_x * layer["speed"]

  def draw(self, surface):
    for layer in self.layers:
      x = int(layer["x"]) % self.width  # wrap smoothly
      surface.blit(layer["image"], (x - self.width, 0))  # previous image
      surface.blit(layer["image"], (x, 0))               # current image
