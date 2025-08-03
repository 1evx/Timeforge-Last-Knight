import random

import pygame

from scripts.Coin import Coin
from scripts.utils import load_sprite_folder

class Slime(pygame.sprite.Sprite):
  def __init__(self, x, y, player,coin_group):
    super().__init__()
    self.coin_group = coin_group

    # Sprite sheet config
    self.animations = {
      "attack": load_sprite_folder("assets/sprites/slimeL1/attack"),
      "death":  load_sprite_folder("assets/sprites/slimeL1/death"),
      "walk":   load_sprite_folder("assets/sprites/slimeL1/walk"),
      "idle":   load_sprite_folder("assets/sprites/slimeL1/idle"),
      "hit":    load_sprite_folder("assets/sprites/slimeL1/hurt"),
    }

    # Core stats
    self.health = 5
    self.alive = True
    self.state = "idle"
    self.frame_index = 0
    self.animation_speed = 0.15
    self.image = self.animations[self.state][0]
    self.rect = self.image.get_rect(topleft=(x, y))
    self.hitbox = self.rect.inflate(-10, 0)

    # Patrol
    self.direction = 1
    self.speed = 2
    self.start_x = x
    self.patrol_distance = 100
    self.patrol_left = self.start_x - self.patrol_distance
    self.patrol_right = self.start_x + self.patrol_distance

    # Player
    self.player = player
    self.aggro_range = 500
    self.attack_range = 70

    # Attack
    self.attacking = False
    self.attack_damage = 1
    self.attack_timer = 1500  # ms
    self.attack_windup = 600   # ms
    self.attack_cooldown = 2000  # ms
    self.last_attack_time = 0
    self.attack_active_frames = (2, 5)
    self.attack_has_hit = False

    # Hit
    self.hit_anim_playing = False
    self.knockback_velocity = 10
    self.knockback_timer = 20
    self.stun_start_time = 0
    self.stun_duration = 700


  def update(self):
    if not self.alive:
      self.animate()
      return

    if self.hit_anim_playing:
      if self.knockback_timer > 0:
        self.rect.x += self.knockback_velocity
        self.knockback_timer -= 1
      self.animate()
      return

    if not self.player.alive:
      self.state = "idle"
      self.animate()
      return

    player_dx = self.player.rect.centerx - self.rect.centerx
    distance = abs(player_dx)
    now = pygame.time.get_ticks()

    if self.attacking:
      self.direction = 1 if player_dx > 0 else -1
      self.animate()
      current_frame = self.get_current_attack_frame()
      if self.attack_active_frames[0] <= current_frame <= self.attack_active_frames[1]:
        if (not self.attack_has_hit and self.get_attack_hitbox().colliderect(self.player.hitbox)):
          self.player.take_damage(self.attack_damage)
          self.attack_has_hit = True

      return

    if distance <= self.attack_range and now - self.last_attack_time >= self.attack_cooldown:
      self.attacking = True
      self.attack_has_hit = False  # reset
      self.state = "attack"
      self.frame_index = 0
      self.last_attack_time = now
    elif distance <= self.aggro_range:
      self.state = "walk"
      self.direction = 1 if player_dx > 0 else -1
      self.rect.x += self.speed * self.direction
    else:
      self.patrol()

    self.animate()
    self.hitbox.center = self.rect.center


  def patrol(self):
    if self.rect.x <= self.patrol_left:
      self.direction = 1
    elif self.rect.x >= self.patrol_right:
      self.direction = -1

    self.state = "walk"
    self.rect.x += self.speed * self.direction


  def animate(self):
    frames = self.animations.get(self.state, self.animations["idle"])

    if self.state == "death":
      if self.frame_index < len(frames) - 1:
        self.frame_index += self.animation_speed
      else:
        self.frame_index = len(frames) - 1

    elif self.state == "attack":
      self.frame_index += self.animation_speed
      if self.frame_index >= len(frames):
        self.frame_index = 0
        self.attacking = False
        self.state = "idle"

    elif self.state == "hit":
      self.frame_index += self.animation_speed
      if self.frame_index >= len(frames):
        self.frame_index = len(frames) - 1
        now = pygame.time.get_ticks()
        if now - self.stun_start_time >= self.stun_duration:
          self.hit_anim_playing = False
          self.state = "idle"
          
    else:
      self.frame_index += self.animation_speed
      if self.frame_index >= len(frames):
        self.frame_index = 0

    frame = frames[int(self.frame_index)]
    if self.direction == 1:
      frame = pygame.transform.flip(frame, True, False)
    self.image = frame


  def get_current_attack_frame(self):
    return int(self.frame_index) if self.state == "attack" else -1


  def get_attack_hitbox(self):
    width = 60
    height = self.rect.height
    new_top = self.rect.top + 40

    if self.direction == 1:
      return pygame.Rect(self.rect.right, new_top, width, height)
    else:
      return pygame.Rect(self.rect.left - width, new_top, width, height)


  def take_damage(self, amount):
    now = pygame.time.get_ticks()
    self.health -= amount

    if self.health <= 0:
      self.die()
      return

    self.attacking = False
    self.stun_start_time = now
    self.state = "hit"
    self.hit_anim_playing = True
    self.frame_index = 0
    self.knockback_velocity = -self.direction * 5


  def die(self):
    self.alive = False
    self.state = "death"
    self.frame_index = 0

    num_coins = 2
    for i in range(num_coins):
      offset_x = random.randint(-200, 150)
      offset_y = random.randint(-5, 5)
      coin = Coin(self.rect.centerx + offset_x, self.rect.centery + offset_y)
      self.coin_group.add(coin)

  def draw_health_bar(self, surface, screen_rect):
    if self.alive:
      bar_width = 40
      bar_height = 5
      bar_x = screen_rect.centerx - bar_width // 2
      bar_y = screen_rect.top - 10  # above the image

      ratio = max(self.health / 5, 0)

      bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
      pygame.draw.rect(surface, (60, 60, 60), bg_rect)

      hp_rect = pygame.Rect(bar_x, bar_y, int(bar_width * ratio), bar_height)
      pygame.draw.rect(surface, (255, 0, 0), hp_rect)

      pygame.draw.rect(surface, (0, 0, 0), bg_rect, 1)

