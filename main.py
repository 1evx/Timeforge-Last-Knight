import pygame
from scripts import Settings
from scripts.Level import Level
from levels.oak_forest import oak_forest_data
from levels.haze_forest import haze_forest_data
from levels.crystal_cave import crystal_cave_data
from levels.dark_castle import dark_castle_data
from scripts.utils import fade

def main():
  pygame.init()
  screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
  pygame.display.set_caption("Timeforge: The Last Knight")

  levels = [oak_forest_data, haze_forest_data, crystal_cave_data, dark_castle_data]

  for i, level_data in enumerate(levels):
    # Fade in at the start of each level
    fade(screen, fade_in=True, speed=5)

    level = Level(screen, level_data)
    level.run()

    if not level.has_finished:
      break

    if i < len(levels) - 1:
      fade(screen, fade_in=False, speed=5)

  pygame.quit()

if __name__ == "__main__":
  main()