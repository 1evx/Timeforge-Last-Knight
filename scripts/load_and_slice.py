import pygame

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
