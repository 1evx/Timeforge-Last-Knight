import pygame
from scripts.utils import load_and_resize_frames
from scripts.Settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Shop(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    
    # Load animated shop frames
    self.animations = load_and_resize_frames(
      pygame.image.load("assets/decorations/shop_anim.png").convert_alpha(),
      0, 6, 118, 128, scale=2.8
    )
    self.frame_index = 0
    self.animation_speed = 0.1

    # Set sprite
    self.image = self.animations[0]
    self.rect = self.image.get_rect(topleft=(x, y))

    # Fonts
    self.font = pygame.font.Font(None, 24)
    self.ui_font = pygame.font.Font(None, 36)
    
    # UI / Logic
    self.show_prompt = False
    self.show_ui = False
    self.selected_index = 0
    self.interaction_radius = 100

    self.items = [
      {"name": "Health Potion", "price": 5, "effect": self.give_health , "repeatable": True},
      {"name": "Speed Boost", "price": 5, "effect": self.upgrade_speed},
      {"name": "Max Health", "price": 15, "effect": self.increase_max_health},
      {"name": "Sword Upgrade", "price": 25, "effect": self.upgrade_sword},
    ]
    
    self.item_rects = []  # for mouse clicks

  def update(self, player):
    self.frame_index += self.animation_speed
    if self.frame_index >= len(self.animations):
      self.frame_index = 0
    self.image = self.animations[int(self.frame_index)]
    self.show_prompt = self.check_interaction(player)

  def check_interaction(self, player):
    # Simple AABB collision
    if self.rect.colliderect(player.rect):
      self.show_prompt = True
      return True
    else:
      self.show_prompt = False
      return False

  def draw_prompt(self, surface, camera):
    if self.show_prompt and not self.show_ui:
      screen_pos = camera.apply(self.rect)
      text = self.font.render("Press E to open shop", True, (255, 255, 255))
      text_rect = text.get_rect(center=(screen_pos.centerx, screen_pos.top - 10))
      surface.blit(text, text_rect)

  def draw_ui(self, surface, player):
    if not self.show_ui:
      return

    panel_width, panel_height = 600, 500
    panel_x = SCREEN_WIDTH // 2 - panel_width // 2
    panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    # Draw panel
    pygame.draw.rect(surface, (30, 30, 30), panel_rect)
    pygame.draw.rect(surface, (200, 200, 200), panel_rect, 2)

    title = self.ui_font.render("Shop", True, (255, 255, 255))
    surface.blit(title, (panel_x + 240, panel_y + 10))

    # Item list
    self.item_rects.clear()
    mouse_pos = pygame.mouse.get_pos()

    for i, item in enumerate(self.items):
      purchased = item['name'] in player.purchased_upgrades
      item_text = f"{item['name']} - {item['price']}G"
      text_surf = self.font.render(item_text, True, (255, 255, 255))
      item_rect = text_surf.get_rect(topleft=(panel_x + 40, panel_y + 60 + i * 40))

      is_hovered = item_rect.collidepoint(mouse_pos)

      # Color logic
      if purchased:
        color = (150, 150, 150)  # grey for disabled
      elif i == self.selected_index or is_hovered:
        color = (255, 255, 0)
      else:
        color = (255, 255, 255)

      # Highlight if hovered and not purchased
      if is_hovered and not purchased:
        pygame.draw.rect(surface, (50, 50, 100), item_rect.inflate(10, 10))

      text_surf = self.font.render(item_text, True, color)
      surface.blit(text_surf, item_rect)
      self.item_rects.append((item_rect, i))

    # Player Gold
    gold_text = self.font.render(f"Gold: {player.money}", True, (255, 255, 255))
    surface.blit(gold_text, (panel_x + 40, panel_y + panel_height - 60))

    # Close prompt
    close_text = self.font.render("Press E to close", True, (180, 180, 180))
    close_rect = close_text.get_rect(bottomright=(panel_x + panel_width - 20, panel_y + panel_height - 20))
    surface.blit(close_text, close_rect)

  def handle_input(self, event, player):
    if not self.show_ui:
      return

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        self.selected_index = (self.selected_index - 1) % len(self.items)
      elif event.key == pygame.K_DOWN:
        self.selected_index = (self.selected_index + 1) % len(self.items)
      elif event.key == pygame.K_RETURN:
        self.buy(player)
      elif event.key == pygame.K_ESCAPE:
        self.show_ui = False

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = event.pos
      for rect, index in self.item_rects:
        if rect.collidepoint(mouse_pos):
          self.selected_index = index
          self.buy(player)

  def buy(self, player):
    item = self.items[self.selected_index]
    item_name = item["name"]
    repeatable = item.get("repeatable", False)

    if not repeatable and item_name in player.purchased_upgrades:
      print(f"{item_name} already purchased!")
      return

    if player.money >= item["price"]:
      player.money -= item["price"]
      item["effect"](player)

      if not repeatable:
        player.purchased_upgrades.add(item_name)

      print(f"{item_name} purchased!")
    else:
      print("Not enough gold!")

  def give_health(self, player):
    if player.health < player.max_health:
      player.health = player.max_health

  def upgrade_sword(self, player):
    player.attack_power += 1
    player.purchased_upgrades.add("Upgrade Sword")

  def upgrade_speed(self, player):
    if hasattr(player, "speed"):
      player.speed = min(player.speed + 1, 7)
      player.purchased_upgrades.add("Speed Boost")

  def increase_max_health(self, player):
    player.max_health += 15
    player.health = player.max_health
    player.purchased_upgrades.add("Max Health")