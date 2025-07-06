import pygame
from scripts import Settings
from scripts.Level import Level
from levels.oak_forest import oak_forest_data
from levels.crystal_cave import crystal_cave_data  # Example second level

def main():
  pygame.init()
  screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
  pygame.display.set_caption("Timeforge: The Last Knight")

  levels = [oak_forest_data, crystal_cave_data]  # Add more as you make them

  for level_data in levels:
    level = Level(screen, level_data)
    level.run()
    if not level.has_finished:
      break  # If player quit early

  pygame.quit()

if __name__ == "__main__":
  main()