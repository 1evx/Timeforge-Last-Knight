import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load coin image (replace with your coin sprite path)
        self.image = pygame.image.load("assets/decorations/coins.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))  # Adjust size as needed
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 5000  # Coin exists for 5 seconds (in milliseconds)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Remove coin after its lifetime expires
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()