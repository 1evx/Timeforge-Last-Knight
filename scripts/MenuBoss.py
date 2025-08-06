import pygame
import random
from scripts.utils import load_sprite_folder


class MenuBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.attack1_frames = load_sprite_folder("assets/sprites/deathborne/attack")

        self.current_animation = "attack1"
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.attack1_frames[0] if self.attack1_frames else self.create_placeholder_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing = 1

    def create_placeholder_sprite(self, color=(150, 100, 255)):
        surface = pygame.Surface((128, 128), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (32, 16, 64, 96))  # Body
        pygame.draw.circle(surface, (255, 220, 180), (64, 40), 16)  # Head
        pygame.draw.rect(surface, (80, 80, 80), (16, 48, 16, 48))  # Left arm
        pygame.draw.rect(surface, (80, 80, 80), (96, 48, 16, 48))  # Right arm
        return surface

    def update_demo(self, dt):
        self.animate()

    def animate(self):
        if not self.attack1_frames:
            return

        frames = self.attack1_frames
        self.frame_index += self.animation_speed

        if self.frame_index >= len(frames):
            self.frame_index = 0

        self.image = frames[int(self.frame_index)]
        self.image = pygame.transform.smoothscale(self.image, (250, 150))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        if self.facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(topleft=self.rect.topleft)