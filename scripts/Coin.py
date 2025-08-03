import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load sprite sheet
        self.sprite_sheet = pygame.image.load("assets/decorations/coins.png").convert_alpha()

        # Frame slicing setup
        self.frames = []
        FRAME_COLS = 8
        FRAME_ROWS = 1
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        frame_width = sheet_width // FRAME_COLS
        frame_height = sheet_height // FRAME_ROWS

        # Extract all frames
        for row in range(FRAME_ROWS):
            for col in range(FRAME_COLS):
                frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                frame_image = self.sprite_sheet.subsurface(frame_rect)
                frame_image = pygame.transform.scale(frame_image, (64, 64))
                self.frames.append(frame_image)

        # Animation parameters
        self.current_frame = 0
        self.animation_speed = 0.2

        # Image and Rect
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect(center=(x, y))

        # Lifetime tracking
        self.lifetime = 5000  # milliseconds
        self.spawn_time = pygame.time.get_ticks()
        self.invulnerable_time = 500

    def update(self):
        # Animate
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # Lifetime handling
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def can_be_collected(self):
        return pygame.time.get_ticks() - self.spawn_time > self.invulnerable_time
