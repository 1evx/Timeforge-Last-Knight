import pygame
from scripts.utils import load_and_resize_frames

class Shop(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()

    # Load animated frames
    self.animations = load_and_resize_frames(pygame.image.load("assets/decorations/shop_anim.png").convert_alpha(), 0, 6, 118, 128, scale=2.8)
    self.frame_index = 0
    self.animation_speed = 0.1

    # Set initial image
    self.image = self.animations[0]
    self.rect = self.image.get_rect(topleft=(x, y))

    # Define items correctly
    self.items = [
      {"name": "Health Potion", "price": 50, "effect": self.give_health},
      {"name": "Sword Upgrade", "price": 200, "effect": self.upgrade_sword}
    ]
    self.selected_index = 0

    self.interaction_radius = 100
    self.show_prompt = False
    self.prompt_font = pygame.font.SysFont(None, 28)

    self.font = pygame.font.SysFont(None, 32)

  def update(self):
    self.frame_index += self.animation_speed
    if self.frame_index >= len(self.animations):
      self.frame_index = 0
    self.image = self.animations[int(self.frame_index)]

  def check_interaction(self, player):
    distance = self.rect.centerx - player.rect.centerx
    if abs(distance) <= self.interaction_radius:
      self.show_prompt = True
      return True
    else:
      self.show_prompt = False
      return False

  def draw_prompt(self, screen):
    if self.show_prompt:
      text = self.prompt_font.render("Press E to interact", True, (255, 255, 255))
      text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 20))
      screen.blit(text, text_rect)

  def buy(self, player):
    """Try to buy the currently selected item"""
    item = self.items[self.selected_index]
    if player.gold >= item["price"]:
      player.gold -= item["price"]
      item["effect"](player)
      print(f"{item['name']} purchased!")
    else:
      print("Not enough gold!")

  def next_item(self):
    self.selected_index = (self.selected_index + 1) % len(self.items)

  def prev_item(self):
    self.selected_index = (self.selected_index - 1) % len(self.items)

  def draw_ui(self, screen):
    """Draw simple shop UI"""
    y = 100
    for i, item in enumerate(self.items):
      color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
      text = f"{item['name']} - {item['price']} gold"
      img = self.font.render(text, True, color)
      screen.blit(img, (100, y))
      y += 40

  def give_health(self, player):
    player.health += 50
    if player.health > player.max_health:
      player.health = player.max_health

  def upgrade_sword(self, player):
    player.attack_power += 10
