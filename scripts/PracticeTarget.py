import pygame

class PracticeTarget(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()

    # Images
    idle_img = pygame.image.load("assets/decorations/practice_target_idle.png").convert_alpha()
    self.image = pygame.transform.scale_by(idle_img, 1.6)

    broken_img = pygame.image.load("assets/decorations/practice_target_hit.png").convert_alpha()
    self.broken_image = pygame.transform.scale_by(broken_img, 1.65)

    self.rect = self.image.get_rect(topleft=(x, y))
    self.hitbox = self.rect.inflate(-10, 0)

    self.health = 5
    self.is_hit = False
    self.hit_timer = 0

  def update(self):
    if self.is_hit:
      self.image = self.broken_image

      self.hit_timer += 1
      if self.hit_timer > 30:  # After hit effect, switch back to idle
        self.is_hit = False
        self.hit_timer = 0
        if self.health <= 0:
          self.health = 5
        self.image = pygame.transform.scale_by(pygame.image.load("assets/decorations/practice_target_idle.png").convert_alpha(),1.6)

    self.hitbox.center = self.rect.center

  def take_damage(self, amount):
    if not self.is_hit:
      self.health -= amount
      self.hit()

  def hit(self):
    self.is_hit = True
    self.hit_timer = 0

  def draw_health_bar(self, surface, screen_rect):
    if self.alive and self.health > 0:
      bar_width = 40
      bar_height = 5
      bar_x = screen_rect.centerx - bar_width // 2
      bar_y = screen_rect.top - 10

      ratio = max(self.health / 5, 0)

      bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
      pygame.draw.rect(surface, (60, 60, 60), bg_rect)

      hp_rect = pygame.Rect(bar_x, bar_y, int(bar_width * ratio), bar_height)
      pygame.draw.rect(surface, (255, 0, 0), hp_rect)

      pygame.draw.rect(surface, (0, 0, 0), bg_rect, 1)
