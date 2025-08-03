import random
import pygame
import math
from scripts.Coin import Coin
from scripts.utils import load_and_resize_frames
from scripts.Projectile import Projectile

class Necromancer(pygame.sprite.Sprite):
  def __init__(self, x, y, player, projectile_group,coin_group):
    super().__init__()

    # Sprite sheet config
    self.coin_group = coin_group
    self.animations = {
      "attack": load_and_resize_frames(pygame.image.load("assets/sprites/necromancer/attack/spr_NecromancerAttackWithoutEffect_strip47.png").convert_alpha(), 0, 47, 128, 128, scale=2.8, target_size=(128*2.8, 128*2.8)),
      "death":  load_and_resize_frames(pygame.image.load("assets/sprites/necromancer/death/spr_NecromancerDeath_strip52.png").convert_alpha(), 0, 52, 96, 96, scale=2.8, target_size=(128*2.8, 128*2.8)),
      "walk":   load_and_resize_frames(pygame.image.load("assets/sprites/necromancer/walk/spr_NecromancerWalk_strip10.png").convert_alpha(), 0, 8, 96, 96, scale=2.8, target_size=(128*2.8, 128*2.8)),
      "idle":   load_and_resize_frames(pygame.image.load("assets/sprites/necromancer/idle/spr_NecromancerIdle_strip50.png").convert_alpha(), 0, 50, 96, 96, scale=2.8, target_size=(128*2.8, 128*2.8)),
      "hit":    load_and_resize_frames(pygame.image.load("assets/sprites/necromancer/hurt/spr_NecromancerGetHit_strip9.png").convert_alpha(), 0, 9, 96, 96, scale=2.8, target_size=(128*2.8, 128*2.8)),
    }

    # Core stats
    self.health = 4
    self.alive = True
    self.state = "idle"
    self.frame_index = 0
    self.animation_speed = 0.15
    self.image = self.animations[self.state][0]
    self.rect = self.image.get_rect(topleft=(x, y))
    self.hitbox = self.rect.inflate(-250, -200)

    self.direction = 1
    self.speed = 2

    # Player
    self.player = player
    self.aggro_range = 500
    self.shoot_range = 1200
    self.retreat_range = 200

    # Ranged Attack
    self.projectile_group = projectile_group
    self.shoot_cooldown = 3000
    self.last_shot = 0
    self.shoot_damage = 2
    self.attacking = False
    self.current_projectile = None
    self.shot_delay = 3000
    self.shot_start_time = 0
    self.projectile_spawned = False

    # Hit
    self.hit_anim_playing = False
    self.knockback_velocity = 20
    self.knockback_timer = 20
    self.stun_start_time = 0
    self.stun_duration = 600

    # Preload projectile animations with conditional flip
    sprite_sheet = pygame.image.load("assets/sprites/necromancer/attack/spr_NecromancerAttackEffect_strip47.png").convert_alpha()
    if self.direction == -1:  # Flip if shooting left
      sprite_sheet = pygame.transform.flip(sprite_sheet, True, False)
    full_animation = load_and_resize_frames(sprite_sheet, 0, 47, 128, 128, scale=2.8, target_size=(128*2.8, 128*2.8))
    self.reloading_animation = full_animation[0:23]
    self.shooting_animation = full_animation[23:30]

  def update(self):
    if not self.alive:
      self.animate()
      return

    if self.hit_anim_playing:
      if self.knockback_timer > 0:
        self.rect.x += self.knockback_velocity
        self.knockback_timer -= 1
      now = pygame.time.get_ticks()
      if now - self.stun_start_time >= self.stun_duration:
        self.hit_anim_playing = False
        self.state = "idle"  # Reset to idle after stun
        self.frame_index = 0
      self.animate()
      return

    if not self.player.alive:
      self.state = "idle"
      self.animate()
      return

    player_dx = self.player.rect.centerx - self.rect.centerx
    distance = abs(player_dx)
    now = pygame.time.get_ticks()

    self.direction = 1 if player_dx > 0 else -1

    # Retreat if player is too close
    if distance <= self.retreat_range and not self.attacking:
      self.state = "walk"
      self.rect.x -= self.speed * self.direction
    # Shoot if in range, off cooldown, and no projectile spawned
    elif distance <= self.shoot_range and now - self.last_shot >= self.shoot_cooldown and not self.projectile_spawned:
      self.state = "attack"
      self.frame_index = 0
      self.attacking = True
      self.shoot()
      self.last_shot = now
    # Idle if not attacking and out of aggro range
    elif not self.attacking:
      self.state = "idle"

    self.animate()
    self.hitbox.center = self.rect.center
    self.hitbox.centery -= 25

  def shoot(self):
    # Calculate direction vector based on current positions
    dx = self.player.rect.centerx - self.rect.centerx
    dy = self.player.rect.centery - self.rect.centery
    angle = math.atan2(dy, dx)
    speed = 8

    # Prepare animation frames, flipping if facing left
    reloading_frames = [pygame.transform.flip(frame, True, False) if self.direction == -1 else frame for frame in self.reloading_animation]
    shooting_frames = [pygame.transform.flip(frame, True, False) if self.direction == -1 else frame for frame in self.shooting_animation]

    # Spawn projectile with synchronized animation
    self.current_projectile = Projectile(self.rect.centerx, self.rect.centery, angle, speed, reloading_frames, self.player, self.shoot_damage, animation_speed=0.2, hitbox_size=(30, 30), x_offset=-30, y_offset=-30, hitbox_anchor="topmid")
    self.current_projectile.frame_index = self.frame_index
    self.projectile_group.add(self.current_projectile)
    self.shot_start_time = pygame.time.get_ticks()
    self.projectile_spawned = True

  def animate(self):
    frames = self.animations.get(self.state, self.animations["idle"])
    if self.state == "death":
      if self.frame_index < len(frames) - 1:
        self.frame_index += self.animation_speed
      else:
        self.frame_index = len(frames) - 1
    elif self.state == "attack":
      self.frame_index += self.animation_speed
      if self.current_projectile and self.current_projectile.alive():  # Sync projectile animation
        self.current_projectile.frame_index = self.frame_index
        self.current_projectile.rect.center = self.rect.center  # Keep projectile at Necromancer's position
      now = pygame.time.get_ticks()
      if self.projectile_spawned and now - self.shot_start_time >= self.shot_delay:
        if self.current_projectile:
          self.current_projectile.switch_animation(self.shooting_animation)  # Switch to shooting animation
          self.current_projectile.frame_index = 0  # Reset frame index for shooting
          self.current_projectile.active = True  # Launch projectile
          self.current_projectile = None  # Clear reference after launch
          self.projectile_spawned = False
      if self.frame_index >= len(frames) and not self.projectile_spawned:
        self.frame_index = 0  # Restart animation for continuous attacks
        self.attacking = False  # Allow new attack cycle
    elif self.state == "hit":
      self.frame_index += self.animation_speed
      if self.frame_index >= len(frames):
        self.frame_index = 0  # Reset frame index
        now = pygame.time.get_ticks()
        if now - self.stun_start_time >= self.stun_duration:
          self.hit_anim_playing = False
          self.state = "idle"  # Reset to idle after hit animation
    else:
      self.frame_index += self.animation_speed
      if self.frame_index >= len(frames):
        self.frame_index = 0

    frame = frames[int(self.frame_index)]
    if self.direction == -1:
      frame = pygame.transform.flip(frame, True, False)
    self.image = frame

  def take_damage(self, amount):
    now = pygame.time.get_ticks()
    self.health -= amount

    if self.health <= 0:
      self.die()
      return

    self.stun_start_time = now
    self.state = "hit"
    self.hit_anim_playing = True
    self.frame_index = 0
    self.knockback_velocity = -self.direction * 5

    if self.current_projectile:
      self.current_projectile.kill()
      self.current_projectile = None

    # Reset attack state on hit
    self.attacking = False
    self.projectile_spawned = False
    self.current_projectile = None

  def die(self):
    self.alive = False
    self.state = "death"
    self.frame_index = 0

    # Clean up projectile
    if self.current_projectile:
      self.current_projectile.kill()
      self.current_projectile = None

    num_coins = 3
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
      bar_y = screen_rect.top + 70  # above the image

      ratio = max(self.health / 4, 0)

      bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
      pygame.draw.rect(surface, (60, 60, 60), bg_rect)

      hp_rect = pygame.Rect(bar_x, bar_y, int(bar_width * ratio), bar_height)
      pygame.draw.rect(surface, (255, 0, 0), hp_rect)

      pygame.draw.rect(surface, (0, 0, 0), bg_rect, 1)