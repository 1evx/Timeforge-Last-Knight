import pygame
from scripts.utils import load_sprite_folder

class Fireborne(pygame.sprite.Sprite):
  def __init__(self, x, y, player):
    super().__init__()

    self.animations = {
      "attack": load_sprite_folder("assets/sprites/fireborne/attack", 2),
      "death":  load_sprite_folder("assets/sprites/fireborne/death", 2),
      "walk":   load_sprite_folder("assets/sprites/fireborne/walk", 2),
      "idle":   load_sprite_folder("assets/sprites/fireborne/idle", 2),
      "hit":    load_sprite_folder("assets/sprites/fireborne/hurt", 2),
    }

    # Core stats
    self.health = 6
    self.alive = True
    self.state = "idle"
    self.frame_index = 0
    self.animation_speed = 0.15
    self.image = self.animations[self.state][0]
    self.rect = self.image.get_rect(topleft=(x, y))
    self.hitbox = self.rect.inflate(-400, -130)

    self.direction = 1
    self.speed = 2

    # Player
    self.player = player
    self.aggro_range = 500
    self.attack_range = 200

    # Attack
    self.attacking = False
    self.attack_damage = 3
    self.attack_timer = 2000  # ms
    self.attack_windup = 2000   # ms
    self.attack_cooldown = 1000  # ms
    self.last_attack_time = 0
    self.attack_active_frames = (3, 6)
    self.attack_has_hit = False

    # Hit
    self.hit_anim_playing = False
    self.knockback_velocity = 20
    self.knockback_timer = 20
    self.stun_start_time = 0
    self.stun_duration = 600


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
      self.state = "idle"

    self.animate()
    self.hitbox.center = self.rect.center
    self.hitbox.centery += 70   # Adjust postion y of the enemy hitbox


  def animate(self):
    frames = self.animations.get(self.state, self.animations["idle"])
    
    if self.state == "death":
      if self.frame_index < 10:
        self.frame_index += self.animation_speed
      else:
        self.frame_index = len(frames) - 1  # freeze at last frame
        self.kill()

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
    width = 200
    height = self.rect.height - 140
    new_top = self.rect.top + 140

    if self.direction == 1:
      return pygame.Rect(self.rect.right - 300, new_top, width, height)
    else:
      return pygame.Rect(self.rect.left - width + 300, new_top, width, height)


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


  def draw_health_bar(self, surface, screen_rect):
    if self.alive:
      bar_width = 40
      bar_height = 5
      bar_x = screen_rect.centerx - bar_width // 2
      bar_y = screen_rect.top + 120  # above the image

      ratio = max(self.health / 6, 0)

      bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
      pygame.draw.rect(surface, (60, 60, 60), bg_rect)

      hp_rect = pygame.Rect(bar_x, bar_y, int(bar_width * ratio), bar_height)
      pygame.draw.rect(surface, (255, 0, 0), hp_rect)

      pygame.draw.rect(surface, (0, 0, 0), bg_rect, 1)