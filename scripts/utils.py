import pygame, os

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


def load_frames(sheet, row, num_frames, frame_width, frame_height, scale=1):
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
