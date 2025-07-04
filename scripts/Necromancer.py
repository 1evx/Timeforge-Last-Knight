import pygame
import math
from scripts.utils import load_frames
from scripts.Projectile import Projectile

class Necromancer(pygame.sprite.Sprite):
  def __init__(self, x, y, player, projectile_group):
    super().__init__()

    # Sprite sheet config
    self.animations = {
      "attack": load_frames(pygame.image.load("assets/sprites/necromancer/attack/spr_NecromancerAttackWithEffect_strip47.png").convert_alpha(), 0, 47, 128, 128, scale=2.8),
      "death":  load_frames(pygame.image.load("assets/sprites/necromancer/death/spr_NecromancerDeath_strip52.png").convert_alpha(), 0, 52, 96, 96, scale=2.8),
      "walk":   load_frames(pygame.image.load("assets/sprites/necromancer/walk/spr_NecromancerWalk_strip10.png").convert_alpha(), 0, 8, 96, 96, scale=2.8),
      "idle":   load_frames(pygame.image.load("assets/sprites/necromancer/idle/spr_NecromancerIdle_strip50.png").convert_alpha(), 0, 50,  96, 96, scale=2.8),
      "hit":    load_frames(pygame.image.load("assets/sprites/necromancer/hurt/spr_NecromancerGetHit_strip9.png").convert_alpha(), 0, 9,  96, 96, scale=2.8),
    }

    # Core stats
    self.health = 2
    self.alive = True
    self.state = "idle"
    self.frame_index = 0
    self.animation_speed = 0.15
    self.image = self.animations[self.state][0]
    self.rect = self.image.get_rect(topleft=(x, y))
    self.hitbox = self.rect.inflate(-130, -130)

    self.direction = 1
    self.speed = 2

    # Player
    self.player = player
    self.aggro_range = 500
    self.attack_range = 200

    # Melee Attack
    self.attacking = False
    self.attack_damage = 3
    self.attack_timer = 2000
    self.attack_windup = 2000
    self.attack_cooldown = 1000
    self.last_attack_time = 0
    self.attack_active_frames = (3, 6)
    self.attack_has_hit = False

    # Ranged Attack
    self.projectile_group = projectile_group
    self.shoot_range = 1000
    self.shoot_cooldown = 2000  # ms
    self.last_shot = 0

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

    # Shoot if in range
    if distance <= self.shoot_range and now - self.last_shot >= self.shoot_cooldown:
      self.shoot()
      self.last_shot = now

    # Melee attack
    if self.attacking:
      self.direction = -1 if player_dx > 0 else 1
      self.animate()
      current_frame = self.get_current_attack_frame()
      if self.attack_active_frames[0] <= current_frame <= self.attack_active_frames[1]:
        if (not self.attack_has_hit and self.get_attack_hitbox().colliderect(self.player.hitbox)):
          self.player.take_damage(self.attack_damage)
          self.attack_has_hit = True
      return

    if distance <= self.attack_range and now - self.last_attack_time >= self.attack_cooldown:
      self.attacking = True
      self.attack_has_hit = False
      self.state = "attack"
      self.frame_index = 0
      self.last_attack_time = now
    elif distance <= self.aggro_range:
      self.state = "walk"
      self.direction = -1 if player_dx > 0 else 1
      self.rect.x += self.speed * self.direction
    else:
      self.state = "idle"

    self.animate()
    self.hitbox.center = self.rect.center
    self.hitbox.centery += 70


  def shoot(self):
    # Calculate direction vector
    dx = self.player.rect.centerx - self.rect.centerx
    dy = self.player.rect.centery - self.rect.centery
    angle = math.atan2(dy, dx)
    speed = 8

    bullet = Projectile(self.rect.centerx, self.rect.centery, angle, speed)
    self.projectile_group.add(bullet)


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
