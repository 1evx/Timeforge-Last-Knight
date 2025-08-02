import pygame
from scripts import Settings
from scripts.Level import Level
from levels.oak_forest import oak_forest_data
from levels.haze_forest import haze_forest_data
from levels.crystal_cave import crystal_cave_data
from levels.dark_castle import dark_castle_data
from scripts.Menu import Menu
from scripts.utils import fade

def main():
  pygame.init()
  screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
  pygame.display.set_caption("Timeforge: The Last Knight")
  levels = [haze_forest_data, crystal_cave_data, dark_castle_data, oak_forest_data]

  menu = Menu(screen)
  if not menu.run():
    pygame.quit()
    return

  money = 0
  for i, level_data in enumerate(levels):
    fade(screen, fade_in=True, speed=5)
    level = Level(screen, level_data,money)
    level.run()

    if not level.has_finished:
      break

    if i < len(levels) - 1:
      fade(screen, fade_in=False, speed=5)

  pygame.quit()

if __name__ == "__main__":
  main()