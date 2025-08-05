import pygame
from scripts.Settings import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverPopup:
  def __init__(self, screen, settings):
    self.screen = screen
    self.settings = settings
    self.font = pygame.font.Font(None, 74)  # Large font for "Game Over"
    self.button_font = pygame.font.Font(None, 48)  # Smaller font for buttons
    self.active = False
    self.buttons = []
    self.create_buttons()

  def create_buttons(self):
    button_width, button_height = 200, 50
    screen_center_x = SCREEN_WIDTH // 2
    screen_center_y = SCREEN_HEIGHT // 2.5
    restart_rect = pygame.Rect(screen_center_x - button_width // 2, screen_center_y + 50, button_width, button_height)
    self.buttons.append({"text": "Restart", "rect": restart_rect, "action": "restart"})
    quit_rect = pygame.Rect(screen_center_x - button_width // 2, screen_center_y + 120, button_width, button_height)
    self.buttons.append({"text": "Quit", "rect": quit_rect, "action": "quit"})

  def draw(self):
    if not self.active:
      return
    overlay = pygame.Surface((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(200)
    self.screen.blit(overlay, (0, 0))
    popup_width, popup_height = 400, 300
    popup_rect = pygame.Rect(
      self.settings.SCREEN_WIDTH // 2 - popup_width // 2,
      self.settings.SCREEN_HEIGHT // 2 - popup_height // 2,
      popup_width,
      popup_height
    )
    pygame.draw.rect(self.screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 2)
    game_over_text = self.font.render("Game Over", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2 - 100))
    self.screen.blit(game_over_text, text_rect)
    for button in self.buttons:
      pygame.draw.rect(self.screen, (100, 100, 100), button["rect"])
      pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2)
      button_text = self.button_font.render(button["text"], True, (255, 255, 255))
      text_rect = button_text.get_rect(center=button["rect"].center)
      self.screen.blit(button_text, text_rect)

  def handle_event(self, event):
    if not self.active:
      return None
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = event.pos
      for button in self.buttons:
        if button["rect"].collidepoint(mouse_pos):
          return button["action"]
    return None
  
class DemoEndScreen:
  def __init__(self, screen, settings):
    self.screen = screen
    self.settings = settings
    self.font = pygame.font.Font(None, 72)
    self.button_font = pygame.font.Font(None, 48)
    self.active = False

    # Calculate button size based on text
    self.button_text = self.button_font.render("Back to Menu", True, (255, 255, 255))
    text_width = self.button_text.get_width()
    text_height = self.button_text.get_height()
    padding_x, padding_y = 40, 20  # Padding around text

    button_width = text_width + padding_x
    button_height = text_height + padding_y
    center_x = self.settings.SCREEN_WIDTH // 2
    center_y = self.settings.SCREEN_HEIGHT // 2 + 50

    self.button = pygame.Rect(center_x - button_width // 2, center_y, button_width, button_height)

  def draw(self):
    if not self.active:
      return
    self.screen.fill((0, 0, 0))

    # Draw "Demo Complete!" text
    text = self.font.render("Demo Complete!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2 - 50))
    self.screen.blit(text, text_rect)

    # Draw button
    pygame.draw.rect(self.screen, (80, 80, 80), self.button)
    pygame.draw.rect(self.screen, (255, 255, 255), self.button, 2)

    # Center and draw button text
    btn_text_rect = self.button_text.get_rect(center=self.button.center)
    self.screen.blit(self.button_text, btn_text_rect)

  def handle_event(self, event):
    if not self.active:
      return None
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self.button.collidepoint(event.pos):
        return "menu"
    return None