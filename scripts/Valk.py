import pygame
from scripts import Settings
from scripts.utils import load_sprite_folder

class Valk(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    # Valk Animation Material
    self.run_frames = load_sprite_folder("assets/sprites/valk/run")
    self.idle_frames = load_sprite_folder("assets/sprites/valk/idle")
    self.jump_frames = load_sprite_folder("assets/sprites/valk/jump")
    self.attack1_frames = load_sprite_folder("assets/sprites/valk/attack1")
    self.attack2_frames = load_sprite_folder("assets/sprites/valk/attack2")
    self.crouch_frames = load_sprite_folder("assets/sprites/valk/crouch")
    self.crouch_slide_frames = load_sprite_folder("assets/sprites/valk/crouch_slide")
    self.dash_attack_frames = load_sprite_folder("assets/sprites/valk/dash_attack")
    self.hurt = load_sprite_folder("assets/sprites/valk/hurt")
    self.death = load_sprite_folder("assets/sprites/valk/die")

    # Valk Normal Settings
    self.state = "idle"
    self.frame_index = 0
    self.animation_speed = 0.15
    self.image = self.idle_frames[0]
    self.rect = self.image.get_rect(topleft=(x, y))
    self.hitbox = self.rect.inflate(-120, 0) # Shrink for hitbox
    self.hitbox.centerx += 100 # Adjust the image

    self.alive = True
    self.health = 6
    self.invincibility_time = 4000  # ms

    self.knockback_velocity = 20
    self.knockback_timer = 200

    # Valk Physics
    self.velocity_y = 0
    self.on_ground = False
    self.direction = 0  # -1 = left, 1 = right, 0 = idle

    self.facing = 1
    self.is_crouching = False

    # Valk Attack State
    self.is_attacking = False
    self.attack_stage = 0  # 0 = no attack, 1 = attack1, 2 = attack2
    self.attack_windup_map = {
      1: 500, # stage 1: 600 ms windup
      2: 0,   # stage 2: no windup
      3: 2500  # heavy attack windup
    }
    self.attack_range_map = {
      1: 50,  # attack1 range
      2: 25,  # attack2 range
      3: 90   # heavy attack range
    }
    self.attack_timer = 0  # when attack1 started
    self.combo_window = 500  # ms to press again for attack2
    self.combo_queued = False
    self.attack_damage = 1

    # Valk Dash Attack State
    self.is_dashing = False
    self.dash_speed = 3
    self.dash_max_speed = 10
    self.dash_min_speed = 1.5
    self.dash_duration = 800  # ms
    self.dash_cooldown = 1000  # ms
    self.dash_timer = 0
    self.last_dash_time = -self.dash_cooldown

    # Valk Slide State
    self.is_sliding = False
    self.slide_distance = 200  # pixels
    self.slide_speed = 10
    self.slide_start_x = 0
    self.slide_cooldown = 1000  # milliseconds
    self.last_slide_time = 0


  def handle_input(self, keys):
    current_time = pygame.time.get_ticks()
    # -------------------------------
    # 1. Hurt Or Dead — override all
    # -------------------------------
    if not self.alive:
      return

    if not self.alive or self.state == "death":
      self.animate()
      return

    if self.state == "hurt":
      if self.knockback_timer <= 0:
        self.state = "idle"
      return

    # -------------------------------
    # 1. Dash Attack — override all
    # -------------------------------
    if self.state == "dash_attack":
      if self.is_dashing:
        elapsed = current_time - self.dash_timer
        t = min(elapsed / self.dash_duration, 1)
        speed = self.dash_max_speed * (1 - t) + self.dash_min_speed * t
        self.rect.x += speed if self.direction >= 0 else -speed

        if elapsed >= self.dash_duration:
          self.is_dashing = False
          self.is_attacking = False
          self.attack_stage = 0
          self.state = "idle"
      return

    # -------------------------------
    # 2. Normal Attack — allow tiny drift
    # -------------------------------
    if self.state.startswith("attack"):
      if keys[pygame.K_a]:
        self.rect.x -= 1
      if keys[pygame.K_d]:
        self.rect.x += 1
      return

    # -------------------------------
    # 3. Slide logic
    # -------------------------------
    if self.is_sliding:
      self.rect.x += self.slide_speed if self.direction >= 0 else -self.slide_speed
      if abs(self.rect.x - self.slide_start_x) >= self.slide_distance:
        self.is_sliding = False
        self.state = "idle"
      return

    # -------------------------------
    # 4. Movement & Crouch
    # -------------------------------
    if keys[pygame.K_s] and keys[pygame.K_d] and self.on_ground:
      if not self.is_sliding and (current_time - self.last_slide_time >= self.slide_cooldown):
        self.is_sliding = True
        self.direction = 1
        self.facing = 1
        self.state = "right_crouch_slide"
        self.slide_start_x = self.rect.x
        self.last_slide_time = current_time
        return

    if keys[pygame.K_s] and keys[pygame.K_a] and self.on_ground:
      if not self.is_sliding and (current_time - self.last_slide_time >= self.slide_cooldown):
        self.is_sliding = True
        self.direction = -1
        self.facing = -1
        self.state = "left_crouch_slide"
        self.slide_start_x = self.rect.x
        self.last_slide_time = current_time
        return

    if keys[pygame.K_s]:
      self.state = "crouch"
      return

    if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
      self.velocity_y = Settings.JUMP_VELOCITY
      self.on_ground = False
      self.state = "jump"
      return

    if keys[pygame.K_a]:
      self.rect.x -= Settings.PLAYER_SPEED
      self.direction = -1
      self.facing = -1
      self.state = "run"
      return

    if keys[pygame.K_d]:
      self.rect.x += Settings.PLAYER_SPEED
      self.direction = 1
      self.facing = 1
      self.state = "run"
      return
    
    # -------------------------------
    # 5. Default: No input
    # -------------------------------
    if self.on_ground and not self.state.startswith("attack"):
      self.state = "idle"


  def apply_gravity(self, platforms):
    self.velocity_y += Settings.GRAVITY
    self.rect.y += self.velocity_y

    self.on_ground = False

    hits = pygame.sprite.spritecollide(self, platforms, False)
    for platform in hits:
      # Only snap if falling downward
      if self.velocity_y > 0 and self.rect.bottom <= platform.rect.bottom:
        self.rect.bottom = platform.rect.top
        self.velocity_y = 0
        self.on_ground = True

    # Optional: still keep a floor limit if you want
    if self.rect.bottom >= Settings.SCREEN_HEIGHT - 45:
      self.rect.bottom = Settings.SCREEN_HEIGHT - 45
      self.velocity_y = 0
      self.on_ground = True


  def animate(self):
    # Pick frames
    if self.state == "run":
      frames = self.run_frames
    elif self.state == "jump":
      frames = self.jump_frames
    elif self.state == "attack1":
      frames = self.attack1_frames
    elif self.state == "attack2":
      frames = self.attack2_frames
    elif self.state in ("right_crouch_slide", "left_crouch_slide"):
      frames = self.crouch_slide_frames
    elif self.state == "crouch":
      frames = self.crouch_frames
    elif self.state == "dash_attack":
      frames = self.dash_attack_frames
    elif self.state == "hurt":
      frames = self.hurt
    elif self.state == "death":
      frames = self.death
    else:
      frames = self.idle_frames

    # ---- HANDLE SPECIAL CASES ----

    # Advance frame
    is_crouching = self.state in ("crouch", "right_crouch_slide", "left_crouch_slide")

    if is_crouching and self.frame_index >= len(frames) - 1:
      self.frame_index = len(frames) - 1
    else:
      self.frame_index += self.animation_speed

    # DEATH
    if self.state == "death":
      if self.frame_index >= len(frames):
        self.frame_index = len(frames) - 1  # hold on last frame

    # HURT
    if self.state == "hurt":
      if self.frame_index >= len(frames):
          self.state = "idle"
          self.frame_index = 0
          self.is_attacking = False
          self.is_dashing = False
          self.attack_stage = 0
          if self.knockback_timer > 0:
              self.rect.x += -self.facing * self.knockback_velocity
              self.knockback_timer -= 10

    # ---- HANDLE NORMAL STATE TRANSITIONS ----
    elif self.frame_index >= len(frames):
      self.frame_index = 0

      if self.state == "attack1":
        if self.combo_queued:
          self.state = "attack2"
          self.attack_stage = 2
          self.is_attacking = True
          self.combo_queued = False
        else:
          self.is_attacking = False
          self.attack_stage = 0
          self.state = "idle"

      elif self.state == "attack2":
        self.is_attacking = False
        self.attack_stage = 0
        self.state = "idle"

      elif self.state == "dash_attack":
        self.is_dashing = False
        self.is_attacking = False
        self.attack_stage = 0
        self.state = "idle"

    # Apply frame
    self.image = frames[int(self.frame_index)]
    if self.direction == -1:
      self.image = pygame.transform.flip(self.image, True, False)


  def update(self, keys, platforms):
    self.hitbox.center = self.rect.center
    self.handle_input(keys)
    self.apply_gravity(platforms)
    self.animate()


  def attack(self):
    current_time = pygame.time.get_ticks()
    self.attack_timer = pygame.time.get_ticks()
    self.attack_damage = 1

    # Cancel dash if currently dashing
    if self.is_dashing:
      self.is_dashing = False
      self.state = "attack1"
      self.attack_stage = 1
      self.frame_index = 0
      self.is_attacking = True
      self.attack_timer = current_time
      self.combo_queued = False
      return

    if self.attack_stage == 0 and not self.is_attacking:
      # Start attack1
      self.state = "attack1"
      self.attack_stage = 1
      self.frame_index = 0
      self.is_attacking = True
      self.attack_timer = current_time
      self.combo_queued = False  # reset

    elif self.attack_stage == 1 and self.is_attacking:
      # User clicked during attack1
      if self.state == "attack1":
        self.combo_queued = True  # queue attack2

    elif self.attack_stage == 2 and self.is_attacking:
      # User clicked during attack1
      if self.state == "attack2":
        self.combo_queued = True  # queue attack2


  def dash_attack(self):
    current_time = pygame.time.get_ticks()
    self.attack_damage = 2
    
    # Block if currently attacking or dashing
    if self.state.startswith("attack") or self.is_dashing:
      return

    # Dash cooldown check
    if current_time - self.last_dash_time >= self.dash_cooldown:
      self.is_dashing = True
      self.state = "dash_attack"
      self.attack_stage = 3
      self.frame_index = 0
      self.dash_timer = current_time
      self.last_dash_time = current_time
      self.is_attacking = True


  def start_slide(self):
    self.state = "slide"
    self.is_sliding = True
    self.slide_start_x = self.rect.x
    self.last_slide_time = pygame.time.get_ticks()
    self.frame_index = 0


  def get_attack_hitbox(self):
    stage = self.attack_stage
    width = self.attack_range_map.get(stage, 50)
    height = self.rect.height
    y = self.rect.top

    if self.facing == 1:
      x = self.hitbox.right
    else:
      x = self.hitbox.left - width

    return pygame.Rect(x, y, width, height)
  

  def take_damage(self, amount):
    self.health -= amount

    if self.health <= 0:
      self.die()
      return

    if not self.alive:
      return

    # Knockback AWAY from attacker
    if hasattr(self, "player"):
      attacker_direction = 1 if self.player.facing >= 0 else -1
    else:
      attacker_direction = 1

    self.knockback_velocity = attacker_direction * 5
    self.knockback_timer = 500
    self.attack_timer = 0
    self.state = "hurt"
    self.frame_index = 0


  def die(self):
    if not self.alive:
      return
    self.alive = False
    self.state = "death"
    self.frame_index = 0