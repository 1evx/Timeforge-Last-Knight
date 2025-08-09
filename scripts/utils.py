import pygame, os
import math

def load_sprite_folder(path, scale=3):
  frames = []
  for filename in sorted(os.listdir(path)):
    if filename.endswith(".png"):
      img = pygame.image.load(os.path.join(path, filename)).convert_alpha()

      # Resize the image
      width = int(img.get_width() * scale)
      height = int(img.get_height() * scale)
      img = pygame.transform.scale(img, (width, height))

      frames.append(img)
  return frames


def load_and_resize_frames(sheet, row, num_frames, frame_width, frame_height, scale=1):
  frames = []
  for i in range(num_frames):
    rect = pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height)
    frame = sheet.subsurface(rect)

    if scale != 1:
      new_width = int(frame_width * scale)
      new_height = int(frame_height * scale)
      frame = pygame.transform.scale(frame, (new_width, new_height))

    frames.append(frame)
  return frames


def load_and_resize_frames(sheet, row, num_frames, frame_width, frame_height, scale=1):
  frames = []
  for i in range(num_frames):
    rect = pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height)
    frame = sheet.subsurface(rect)

    if scale != 1:
      new_width = int(frame_width * scale)
      new_height = int(frame_height * scale)
      frame = pygame.transform.scale(frame, (new_width, new_height))

    frames.append(frame)
  return frames


def load_and_resize_frames(sheet, row, count, width, height, scale=1, target_size=None):
  frames = []
  for i in range(count):
    rect = pygame.Rect(i * width, row * height, width, height)
    frame = sheet.subsurface(rect)
    frame = pygame.transform.scale_by(frame, scale)

    if target_size:
      padded = pygame.Surface(target_size, pygame.SRCALPHA)
      padded.blit(frame, frame.get_rect(center=padded.get_rect().center))
      frame = padded

    frames.append(frame)
  return frames


def load_tileset(tileset_image, tile_width, tile_height, scale=1):
  """Slice a tileset image into individual tile Surfaces.

  Args:
    tileset_image (Surface): The loaded big tileset image.
    tile_width (int): Width of each tile in pixels.
    tile_height (int): Height of each tile in pixels.
    scale (float): Scale factor for each tile.

  Returns:
    list[Surface]: List of tile Surfaces.
  """
  tiles = []
  sheet_width, sheet_height = tileset_image.get_size()

  for y in range(0, sheet_height, tile_height):
    for x in range(0, sheet_width, tile_width):
      tile = tileset_image.subsurface(pygame.Rect(x, y, tile_width, tile_height)).copy()
      if scale != 1:
        new_width = int(tile_width * scale)
        new_height = int(tile_height * scale)
        tile = pygame.transform.scale(tile, (new_width, new_height))
      tiles.append(tile)

  return tiles


def slice_tileset(image_path, tile_width, tile_height, scale=1):
  """Slices a tileset PNG into individual tile surfaces.

  Args:
    image_path (str): Path to the tileset image.
    tile_width (int): Width of a single tile in pixels.
    tile_height (int): Height of a single tile in pixels.
    scale (int): Optional scale multiplier.

  Returns:
    list[Surface]: List of sliced and optionally scaled tile surfaces.
  """
  tile_list = []
  tileset = pygame.image.load(image_path).convert_alpha()
  image_width, image_height = tileset.get_size()

  for row in range(image_height // tile_height):
    for col in range(image_width // tile_width):
      rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
      tile_image = tileset.subsurface(rect)
      if scale != 1:
        tile_image = pygame.transform.scale(tile_image, (tile_width * scale, tile_height * scale))
      tile_list.append(tile_image)

  return tile_list


def generate_tile_row(start_x, y, tile_indices, tile_width, count):
  """
  Auto-generate a repeating row of tiles.

  start_x: where to start the row (in px)
  y: vertical position
  tile_indices: [index1, index2, ...] pattern to repeat
  tile_width: how wide each tile is (in px)
  count: how many tiles to place
  """
  tiles = []
  for i in range(count):
    index = tile_indices[i % len(tile_indices)]
    x = start_x + i * tile_width
    tiles.append({"pos": [x, y], "tile_index": index})
  return tiles


def fade(screen, fade_in=True, speed=5):
  fade_surface = pygame.Surface(screen.get_size()).convert_alpha()
  fade_surface.fill((0, 0, 0))

  clock = pygame.time.Clock()
  alpha = 255 if fade_in else 0
  done = False

  while not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    if fade_in:
      alpha -= speed
      if alpha <= 0:
        done = True
        alpha = 0
    else:
      alpha += speed
      if alpha >= 255:
        done = True
        alpha = 255

    fade_surface.set_alpha(alpha)
    screen.fill((0, 0, 0))  # Or draw current frame behind fade
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)


def loading_screen(screen, level_name="Next Level"):
    """Display a loading screen with progress bar during level transitions."""
    clock = pygame.time.Clock()
    progress = 0
    loading_done = False
    
    # Colors
    background_color = (20, 20, 40)
    bar_bg_color = (60, 60, 80)
    bar_fill_color = (100, 150, 255)
    text_color = (255, 255, 255)
    title_color = (200, 200, 255)
    
    # Fonts
    title_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)
    
    # Bar dimensions
    bar_width = 400
    bar_height = 20
    bar_x = (screen.get_width() - bar_width) // 2
    bar_y = screen.get_height() // 2 + 50
    
    # Loading messages
    loading_messages = [
        "Loading level assets...",
        "Preparing enemies...",
        "Setting up environment...",
        "Almost ready...",
        "Level complete!"
    ]
    
    current_message = 0
    message_timer = 0
    start_time = pygame.time.get_ticks()
    
    while not loading_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        # Update progress (simulate loading with easing)
        if progress < 100:
            # Use easing for smoother progress
            progress += 1.5  # Slower, more realistic progress
            if progress > 100:
                progress = 100
        
        # Update loading message based on progress
        if progress < 20:
            current_message = 0
        elif progress < 40:
            current_message = 1
        elif progress < 70:
            current_message = 2
        elif progress < 90:
            current_message = 3
        else:
            current_message = 4
        
        # Check if loading is complete
        if progress >= 100 and elapsed_time > 2000:  # Minimum 2 seconds
            loading_done = True
        
        # Draw background with gradient effect
        screen.fill(background_color)
        
        # Draw animated background stars
        for i in range(8):
            x = (i * 200 + elapsed_time // 3) % screen.get_width()
            y = (i * 150 + 100) % (screen.get_height() // 2)
            alpha = 100 + int(50 * (math.sin(elapsed_time / 1000 + i) + 1))
            color = (255, 255, 255, alpha)
            pygame.draw.circle(screen, color, (int(x), int(y)), 1)
        
        # Draw title with glow effect
        title_text = title_font.render(f"Loading {level_name}", True, title_color)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
        
        # Add a subtle glow effect
        glow_surf = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
        glow_surf.fill((200, 200, 255, 50))
        screen.blit(glow_surf, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)
        
        # Draw progress bar background with rounded corners effect
        bar_bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, bar_bg_color, bar_bg_rect)
        pygame.draw.rect(screen, (100, 100, 120), bar_bg_rect, 2)
        
        # Draw progress bar fill with animation
        fill_width = int((progress / 100) * bar_width)
        if fill_width > 0:
            bar_fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            # Create gradient effect for the fill
            for i in range(fill_width):
                gradient_ratio = i / fill_width
                r = int(100 + gradient_ratio * 50)
                g = int(150 + gradient_ratio * 50)
                b = int(255 - gradient_ratio * 50)
                pygame.draw.line(screen, (r, g, b), 
                               (bar_x + i, bar_y), 
                               (bar_x + i, bar_y + bar_height))
            
            # Add a subtle pulse effect at the end of the progress bar
            pulse_alpha = int(100 + 50 * math.sin(elapsed_time / 200))
            pulse_color = (255, 255, 255, pulse_alpha)
            pygame.draw.line(screen, pulse_color, 
                           (bar_x + fill_width - 1, bar_y), 
                           (bar_x + fill_width - 1, bar_y + bar_height))
        
        # Draw progress percentage with animation
        progress_text = text_font.render(f"{int(progress)}%", True, text_color)
        progress_rect = progress_text.get_rect(center=(screen.get_width() // 2, bar_y + bar_height + 30))
        screen.blit(progress_text, progress_rect)
        
        # Draw loading message with fade effect
        message_text = small_font.render(loading_messages[current_message], True, text_color)
        message_rect = message_text.get_rect(center=(screen.get_width() // 2, bar_y - 30))
        screen.blit(message_text, message_rect)
        
        # Draw decorative loading dots
        dots_x = screen.get_width() // 2 - 30
        dots_y = bar_y + bar_height + 60
        for i in range(3):
            dot_alpha = 255 if (elapsed_time // 200 + i) % 3 == 0 else 100
            dot_color = (255, 255, 255, dot_alpha)
            pygame.draw.circle(screen, dot_color, (dots_x + i * 20, dots_y), 3)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Brief pause at the end
    pygame.time.wait(500)
