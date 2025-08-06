import pygame
import math
from scripts import Settings
from scripts.MenuBoss import MenuBoss
from scripts.MenuValk import MenuValk


class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.Font(None, 150)
        self.subtitle_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.title_spacing = 40

        self.load_side_images()

        self.title = self.title_font.render("TIMEFORGE", True, (255, 215, 0))
        self.subtitle = self.subtitle_font.render("The Last Knight", True, (200, 200, 200))
        self.title_rect = self.title.get_rect(center=(Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 4 - 10))
        self.subtitle_rect = self.subtitle.get_rect(
            center=(Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 4 + 80))

        button_width = 280
        button_height = 60
        button_spacing = 45
        start_y = Settings.SCREEN_HEIGHT // 2 + 150

        self.start_button = pygame.Rect(Settings.SCREEN_WIDTH // 2 - button_width // 2, start_y, button_width,
                                        button_height)
        self.quit_button = pygame.Rect(Settings.SCREEN_WIDTH // 2 - button_width // 2, start_y + button_spacing * 2,
                                       button_width, button_height)

        self.start_text = self.button_font.render("START GAME", True, (255, 255, 255))
        self.quit_text = self.button_font.render("QUIT", True, (255, 255, 255))

        self.start_text_rect = self.start_text.get_rect(center=self.start_button.center)
        self.quit_text_rect = self.quit_text.get_rect(center=self.quit_button.center)

        self.time = 0.5
        self.selected_button = 0
        self.buttons = [self.start_button, self.quit_button]
        self.button_texts = [self.start_text, self.quit_text]
        self.button_text_rects = [self.start_text_rect, self.quit_text_rect]

        self.particles = []
        for _ in range(50):
            import random
            self.particles.append({
                'x': random.randint(0, Settings.SCREEN_WIDTH),
                'y': random.randint(0, Settings.SCREEN_HEIGHT),
                'speed': random.uniform(0.2, 0.5),
                'size': random.randint(1, 3)
            })

        self.menuSound = pygame.mixer.Sound("assets/sound effect/onGame.mp3")
        self.menuSound.play()
        self.running = True

    def load_side_images(self):
        self.left_valk = MenuValk(390, Settings.SCREEN_HEIGHT // 2 - 32)
        self.left_image = self.left_valk.image
        self.left_image_rect = self.left_valk.rect

        self.right_valk = MenuBoss(Settings.SCREEN_WIDTH - 590, Settings.SCREEN_HEIGHT // 2 - 32)
        self.right_image = self.right_valk.image
        self.right_image_rect = self.right_valk.rect

    def draw_side_images(self):
        float_offset_left = int(5 * math.sin(self.time * 0.003))
        float_offset_right = int(5 * math.sin(self.time * 0.003 + 3.14))

        fixed_glow_size = (300, 180)

        if self.left_valk:
            self.left_image = self.left_valk.image
            self.left_image_rect = self.left_valk.rect
            glow_rect = pygame.Rect(0, 0, *fixed_glow_size)
            glow_rect.center = self.left_image_rect.center
            glow_rect.y += float_offset_left

            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (100, 150, 255, 30), glow_surface.get_rect(), border_radius=20)
            self.screen.blit(glow_surface, glow_rect)

            animated_rect = self.left_image_rect.copy()
            animated_rect.y += float_offset_left
            self.screen.blit(self.left_image, animated_rect)

        if self.right_valk:
            self.right_image = self.right_valk.image
            self.right_image_rect = self.right_valk.rect
            glow_rect = pygame.Rect(0, 0, *fixed_glow_size)
            glow_rect.center = self.right_image_rect.center
            glow_rect.y += float_offset_right

            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 150, 100, 30), glow_surface.get_rect(), border_radius=20)
            self.screen.blit(glow_surface, glow_rect)

            animated_rect = self.right_image_rect.copy()
            animated_rect.y += float_offset_right
            self.screen.blit(self.right_image, animated_rect)

    def update_particles(self):
        import random
        for particle in self.particles:
            particle['y'] += particle['speed']
            if particle['y'] > Settings.SCREEN_HEIGHT:
                particle['y'] = -10
                particle['x'] = random.randint(0, Settings.SCREEN_WIDTH)

    def update_menu_animations(self, dt):
        self.update_particles()

        if self.left_valk:
            self.left_valk.update_demo(dt)
        if self.right_valk:
            self.right_valk.update_demo(dt)

    def draw_gradient_background(self):
        for y in range(Settings.SCREEN_HEIGHT):
            color_value = int(30 * (1 - y / Settings.SCREEN_HEIGHT))
            color = (color_value, color_value // 2, color_value + 10)
            pygame.draw.line(self.screen, color, (0, y), (Settings.SCREEN_WIDTH, y))

    def draw_particles(self):
        for particle in self.particles:
            alpha = int(100 + 50 * math.sin(self.time * 0.01 + particle['x'] * 0.01))
            alpha = max(0, min(255, alpha))
            color = (alpha // 2, alpha // 2, alpha)
            pygame.draw.circle(self.screen, color, (int(particle['x']), int(particle['y'])), particle['size'])

    def draw_button(self, button, text, text_rect, is_selected=False, is_hovered=False):
        shadow_rect = button.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect)

        if is_selected or is_hovered:
            glow_size = int(5 + 3 * math.sin(self.time * 0.01))
            glow_rect = button.copy()
            glow_rect.inflate_ip(glow_size * 2, glow_size * 2)
            pygame.draw.rect(self.screen, (100, 150, 255, 50), glow_rect, border_radius=10)

            button_color = (80, 120, 200)
            border_color = (150, 200, 255)
        else:
            button_color = (40, 60, 100)
            border_color = (80, 100, 150)

        pygame.draw.rect(self.screen, button_color, button, border_radius=8)
        pygame.draw.rect(self.screen, border_color, button, width=2, border_radius=8)

        if is_selected:
            offset_y = int(2 * math.sin(self.time * 0.01))
            adjusted_rect = text_rect.copy()
            adjusted_rect.y += offset_y
            self.screen.blit(text, adjusted_rect)
        else:
            self.screen.blit(text, text_rect)

    def draw_title_with_glow(self):
        for i in range(3, 0, -1):
            glow_title = self.title_font.render("TIMEFORGE", True, (255, 215, 0, 50 * i))
            glow_rect = self.title_rect.copy()
            glow_rect.x += i * 2
            glow_rect.y += i * 2
            self.screen.blit(glow_title, glow_rect)

        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.subtitle, self.subtitle_rect)

    def draw(self):
        self.draw_gradient_background()
        self.draw_particles()
        self.draw_side_images()
        self.draw_title_with_glow()

        mouse_pos = pygame.mouse.get_pos()

        for i, (button, text, text_rect) in enumerate(zip(self.buttons, self.button_texts, self.button_text_rects)):
            is_selected = (i == self.selected_button)
            is_hovered = button.collidepoint(mouse_pos)
            self.draw_button(button, text, text_rect, is_selected, is_hovered)

        pygame.display.flip()

    def handle_keyboard_navigation(self, event):
        if event.key == pygame.K_UP:
            self.selected_button = (self.selected_button - 1) % len(self.buttons)
        elif event.key == pygame.K_DOWN:
            self.selected_button = (self.selected_button + 1) % len(self.buttons)
        elif event.key == pygame.K_RETURN:
            return self.execute_selected_action()
        elif event.key == pygame.K_ESCAPE:
            return False
        return None

    def execute_selected_action(self):
        if self.selected_button == 0:
            self.running = False
            return True
        elif self.selected_button == 1:
            return False
        return None

    def run(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(60)
            self.time += dt

            self.update_menu_animations(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menuSound.stop()
                    return False

                elif event.type == pygame.KEYDOWN:
                    result = self.handle_keyboard_navigation(event)
                    self.menuSound.stop()
                    if result is not None:
                        return result

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.menuSound.stop()
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button in enumerate(self.buttons):
                        if button.collidepoint(mouse_pos):
                            self.selected_button = i
                            result = self.execute_selected_action()
                            if result is not None:
                                return result

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button in enumerate(self.buttons):
                        if button.collidepoint(mouse_pos):
                            self.selected_button = i
                            break
            self.draw()

        return True