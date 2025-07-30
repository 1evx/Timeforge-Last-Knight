import pygame
import math
from scripts.Settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Projectile(pygame.sprite.Sprite):
  def __init__(self, x, y, angle, speed, frames, player, damage, animation_speed=0.2, hitbox_size=(50, 50), x_offset=0, y_offset=0, hitbox_anchor="center"):
    super().__init__()

    # Use original frame sizes without rescaling
    self.frames = frames
    self.frame_index = 0
    self.animation_speed = animation_speed
    self.image = self.frames[int(self.frame_index)]
    self.rect = self.image.get_rect(center=(x, y))

    # Calculate velocity based on angle and speed
    self.vx = math.cos(angle) * speed
    self.vy = math.sin(angle) * speed
    self.player = player
    self.damage = damage
    self.initial_pos = pygame.math.Vector2(x, y)  # Starting position without offset
    self.distance_traveled = 0  # Track distance
    self.range = 1000  # Increased to 1000 pixels for longer range
    self.active = False  # Track if projectile is launched
    self.x_offset = x_offset  # Store x_offset for horizontal positioning
    self.y_offset = y_offset  # Store y_offset for vertical positioning
    self.hitbox_anchor = hitbox_anchor  # Store hitbox anchor point

    # Custom hitbox size, initially disabled
    self.hitbox = pygame.Rect(0, 0, hitbox_size[0], hitbox_size[1])
    self.update_hitbox_position()  # Set initial hitbox position based on anchor
    self.hitbox_enabled = False  # Flag to control hitbox activation

    self.spawn_time = pygame.time.get_ticks()
    self.timeout_duration = 5000

  def update_hitbox_position(self):
    """Update hitbox position based on the anchor point and offsets."""
    if self.hitbox_anchor == "topleft":
      self.hitbox.topleft = (self.rect.left + self.x_offset, self.rect.top + self.y_offset)
    else:  # Default to center
      self.hitbox.center = (self.rect.centerx + self.x_offset, self.rect.centery + self.y_offset)

  def switch_animation(self, new_frames):
    # Switch to new animation frames and reset index
    self.frames = new_frames
    self.frame_index = 0
    self.image = self.frames[int(self.frame_index)]
    current_center = list(self.rect.center)
    current_center[1] -= self.y_offset  # Move up by y_offset
    self.rect = self.image.get_rect(center=tuple(current_center))
    self.update_hitbox_position()  # Update hitbox position to match new anchor
    self.initial_pos = pygame.math.Vector2(*self.rect.center)  # Update initial_pos to new launch position
    self.active = True
    self.hitbox_enabled = True  # Enable hitbox when switching to shooting animation

  def move(self):
    if self.active:
      # Update position and track distance
      current_pos = pygame.math.Vector2(self.rect.center)
      self.distance_traveled = current_pos.distance_to(self.initial_pos)
      self.rect.x += self.vx
      self.rect.y += self.vy
      self.update_hitbox_position()  # Update hitbox position after moving

  def update(self):
    self.move()

    if not self.active:
      now = pygame.time.get_ticks()
      if now - self.spawn_time > self.timeout_duration:
        self.kill()

    self.frame_index += self.animation_speed
    if self.frame_index >= len(self.frames):
      self.frame_index = 0
    self.image = self.frames[int(self.frame_index)]

    # Check collision with player using custom hitbox, only if enabled
    if self.player.alive and self.hitbox_enabled and self.hitbox.colliderect(self.player.hitbox):
      self.player.take_damage(self.damage)
      self.kill()

    # Remove projectile if it exceeds range
    if self.distance_traveled >= self.range:
      self.kill()