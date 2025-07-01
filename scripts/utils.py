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