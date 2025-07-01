import pygame
from scripts.utils import load_frames

class Nightborne(pygame.sprite.Sprite):
  def __init__(self, x, y, player):
    super().__init__()

    # Sprite sheet config
    sprite_sheet = pygame.image.load("assets/sprites/nightborne/NightBorne.png").convert_alpha()

    self.animations = {
      "idle": load_frames(sprite_sheet, 0, 9, 80, 80, scale=4),
      "walk":  load_frames(sprite_sheet, 1, 6, 80, 80, scale=4),
      "attack":   load_frames(sprite_sheet, 2, 12, 80, 80, scale=4),
      "hit":   load_frames(sprite_sheet, 3, 5,  80, 80, scale=4),
      "death":    load_frames(sprite_sheet, 4, 23,  80, 80, scale=4),
    }

    # Core stats
    self.health = 6
    self.alive = True
    self.state = "idle"
    self.frame_index = 0
    self.animation_speed = 0.15
    self.image = self.animations[self.state][0]
    self.rect = self.image.get_rect(topleft=(x, y))
    self.hitbox = self.rect.inflate(-200, -150)

    self.direction = 1
    self.speed = 5

    # Player
    self.player = player
    self.aggro_range = 500
    self.attack_range = 140

    # Attack
    self.attacking = False
    self.attack_damage = 2
    self.attack_timer = 1500  # ms
    self.attack_windup = 1000   # ms
    self.attack_cooldown = 1000  # ms
    self.last_attack_time = 0
    self.attack_active_frames = (8, 12)
    self.attack_has_hit = False

    # Hit
    self.hit_anim_playing = False
    self.knockback_velocity = 20
    self.knockback_timer = 20
    self.stun_start_time = 0
    self.stun_duration = 600

    self.death_timer = 0


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


  def animate(self):
    frames = self.animations.get(self.state, self.animations["idle"])

    if self.state == "death":
      if self.frame_index < len(frames) - 1:
        self.frame_index += self.animation_speed
      else:
        self.frame_index = len(frames) - 1
        if not hasattr(self, 'death_timer'):
          self.death_timer = 0
        self.death_timer += 1
        if self.death_timer >= 5:  # Adjust this number to control how long to hold
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
    if self.direction == -1:
      frame = pygame.transform.flip(frame, True, False)
    self.image = frame


  def get_current_attack_frame(self):
    return int(self.frame_index) if self.state == "attack" else -1


  def get_attack_hitbox(self):
    width = 120
    height = self.rect.height - 150
    new_top = self.rect.top + 80

    if self.direction == 1:
      return pygame.Rect(self.rect.right - 150, new_top, width, height)
    else:
      return pygame.Rect(self.rect.left - width + 150, new_top, width, height)


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
