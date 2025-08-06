import pygame
import random
from scripts.utils import load_sprite_folder

class MenuValk(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.idle_frames = load_sprite_folder("assets/sprites/valk/idle")
        self.attack1_frames = load_sprite_folder("assets/sprites/valk/attack1")
        self.attack2_frames = load_sprite_folder("assets/sprites/valk/attack2")
        self.dash_attack_frames = load_sprite_folder("assets/sprites/valk/dash_attack")

        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.idle_frames[0] if self.idle_frames else self.create_placeholder_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.demo_timer = 0
        self.attack_cooldown = 1000
        self.last_attack_time = 0
        self.facing = 1

        self.attack_sequence = ["attack1", "attack2", "dash_attack"]
        self.current_attack_index = 0

    def create_placeholder_sprite(self, color=(100, 150, 255)):
        surface = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (24, 12, 48, 72))  # Body
        pygame.draw.circle(surface, (255, 220, 180), (48, 30), 12)  # Head
        pygame.draw.rect(surface, (200, 100, 50), (36, 36, 24, 4))  # Sword
        return surface

    def update_demo(self, dt):
        current_time = pygame.time.get_ticks()
        self.demo_timer += dt

        if current_time - self.last_attack_time >= self.attack_cooldown:
            attack_type = self.attack_sequence[self.current_attack_index]
            self.start_attack_demo(attack_type)

            self.current_attack_index = (self.current_attack_index + 1) % len(self.attack_sequence)
            self.last_attack_time = current_time

        self.animate()

    def start_attack_demo(self, attack_type):
        self.current_animation = attack_type
        self.frame_index = 0

        if random.choice([True, False]):
            self.facing *= -1

    def animate(self):
        # Get the appropriate frames based on current animation
        if self.current_animation == "attack1" and self.attack1_frames:
            frames = self.attack1_frames
        elif self.current_animation == "attack2" and self.attack2_frames:
            frames = self.attack2_frames
        elif self.current_animation == "dash_attack" and self.dash_attack_frames:
            frames = self.dash_attack_frames
        elif self.idle_frames:
            frames = self.idle_frames
        else:
            return  # No frames available

        self.frame_index += self.animation_speed

        if self.frame_index >= len(frames):
            if self.current_animation in ["attack1", "attack2", "dash_attack"]:
                # Attack finished, return to idle
                self.current_animation = "idle"
                self.frame_index = 0
            else:
                self.frame_index = 0

        self.image = frames[int(self.frame_index)]
        self.image = pygame.transform.smoothscale(self.image, (192, 132))

        if self.facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)