import pygame
from scripts.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
import math
import random

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


class GameCompleteScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.body_font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 48)
        self.active = False
        
        # Calculate button size based on text
        self.button_text = self.button_font.render("Close Game", True, (255, 255, 255))
        text_width = self.button_text.get_width()
        text_height = self.button_text.get_height()
        padding_x, padding_y = 40, 20
        
        button_width = text_width + padding_x
        button_height = text_height + padding_y
        center_x = self.settings.SCREEN_WIDTH // 2
        center_y = self.settings.SCREEN_HEIGHT // 2 + 150
        
        self.button = pygame.Rect(center_x - button_width // 2, center_y, button_width, button_height)
        
        # Animation variables
        self.animation_time = 0
        self.gem_positions = []
        self.create_gem_positions()
        
        # Particle effects
        self.particles = []
        self.create_celebration_particles()
        
        # Sound effects
        self.sound_played = False
        try:
            self.completion_sound = pygame.mixer.Sound("assets/sound effect/levelWin.mp3")
        except:
            self.completion_sound = None
    
    def create_gem_positions(self):
        """Create positions for the 4 gems to display"""
        center_x = self.settings.SCREEN_WIDTH // 2
        center_y = self.settings.SCREEN_HEIGHT // 2 - 50
        spacing = 80
        
        self.gem_positions = [
            (center_x - spacing * 1.5, center_y),  # Left gem
            (center_x - spacing * 0.5, center_y),  # Center-left gem
            (center_x + spacing * 0.5, center_y),  # Center-right gem
            (center_x + spacing * 1.5, center_y),  # Right gem
        ]
    
    def create_gem_icon(self, gem_type, size=32):
        """Create a gem icon for display"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Different colors for different gem types
        colors = {
            "sapphire": (50, 50, 255),    # Blue
            "emerald": (50, 255, 50),     # Green
            "ruby": (255, 50, 50),        # Red
            "amethyst": (150, 50, 255),   # Purple
        }
        
        gem_color = colors.get(gem_type, (200, 200, 255))
        
        # Create a diamond shape
        points = [
            (size//2, size//8),           # Top
            (size*3//4, size//2),         # Right
            (size//2, size*7//8),         # Bottom
            (size//4, size//2),           # Left
        ]
        
        # Draw the gem
        pygame.draw.polygon(surface, gem_color, points)
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)
        
        # Add sparkle
        pygame.draw.circle(surface, (255, 255, 255), (size//3, size//3), 2)
        
        return surface
    
    def create_celebration_particles(self):
        """Create celebration particles"""
        for _ in range(50):
            x = random.randint(0, self.settings.SCREEN_WIDTH)
            y = random.randint(0, self.settings.SCREEN_HEIGHT)
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            color = random.choice([(255, 255, 255), (200, 200, 255), (255, 200, 200), (200, 255, 200)])
            self.particles.append({
                'x': x, 'y': y, 'vx': vx, 'vy': vy, 'color': color,
                'life': random.randint(100, 200), 'max_life': 200
            })
    
    def draw(self):
        if not self.active:
            return
        
        # Play completion sound once
        if not self.sound_played and self.completion_sound:
            self.completion_sound.play()
            self.sound_played = True
        
        # Animate time
        self.animation_time += 1
        
        # Draw background with gradient effect
        for y in range(self.settings.SCREEN_HEIGHT):
            # Create a gradient from dark blue to purple
            ratio = y / self.settings.SCREEN_HEIGHT
            r = int(20 + ratio * 30)
            g = int(20 + ratio * 20)
            b = int(40 + ratio * 60)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.settings.SCREEN_WIDTH, y))
        
        # Draw animated stars in background
        for i in range(20):
            x = (i * 200 + self.animation_time // 2) % self.settings.SCREEN_WIDTH
            y = (i * 150 + 100) % self.settings.SCREEN_HEIGHT
            alpha = 100 + int(50 * (math.sin(self.animation_time / 1000 + i) + 1))
            color = (255, 255, 255, alpha)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 1)
        
        # Draw celebration particles
        for particle in self.particles[:]:
            # Update particle
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Draw particle with fade effect
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (*particle['color'], alpha)
            
            # Create particle surface
            particle_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (2, 2), 2)
            self.screen.blit(particle_surf, (int(particle['x']), int(particle['y'])))
        
        # Draw title with glow effect and animation
        title_alpha = int(200 + 55 * math.sin(self.animation_time / 50))
        title_color = (255, 255, 255)
        title_text = self.title_font.render("GAME COMPLETE!", True, title_color)
        title_rect = title_text.get_rect(center=(self.settings.SCREEN_WIDTH // 2, 150))
        
        # Add glow effect
        glow_surf = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
        glow_surf.fill((255, 255, 255, 50))
        self.screen.blit(glow_surf, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render("You have collected all the gems!", True, (200, 200, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.settings.SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw gem collection display
        gem_types = ["sapphire", "emerald", "ruby", "amethyst"]
        gem_names = ["Sapphire", "Emerald", "Ruby", "Amethyst"]
        
        for i, (pos, gem_type, gem_name) in enumerate(zip(self.gem_positions, gem_types, gem_names)):
            # Animate gem floating
            float_offset = math.sin(self.animation_time / 30 + i) * 5
            gem_y = pos[1] + float_offset
            
            # Add sparkle effect around gems
            sparkle_alpha = int(100 + 50 * math.sin(self.animation_time / 20 + i * 2))
            sparkle_color = (255, 255, 255, sparkle_alpha)
            pygame.draw.circle(self.screen, sparkle_color, (int(pos[0]), int(gem_y)), 35, 2)
            
            # Draw gem icon
            gem_icon = self.create_gem_icon(gem_type, 48)
            gem_rect = gem_icon.get_rect(center=(pos[0], gem_y))
            self.screen.blit(gem_icon, gem_rect)
            
            # Draw gem name
            name_text = self.body_font.render(gem_name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(pos[0], gem_y + 40))
            self.screen.blit(name_text, name_rect)
        
        # Draw completion message with fade effect
        message_alpha = int(200 + 55 * math.sin(self.animation_time / 40))
        message_text = self.body_font.render("You can now forge your way back to the past!", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(message_text, message_rect)
        
        # Draw button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_color = (120, 120, 120) if self.button.collidepoint(mouse_pos) else (80, 80, 80)
        
        pygame.draw.rect(self.screen, button_color, self.button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.button, 2)
        
        # Center and draw button text
        btn_text_rect = self.button_text.get_rect(center=self.button.center)
        self.screen.blit(self.button_text, btn_text_rect)
    
    def handle_event(self, event):
        if not self.active:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button.collidepoint(event.pos):
                return "quit"
        return None