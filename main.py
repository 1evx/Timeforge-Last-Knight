import pygame
from scripts import Settings
from scripts.Level import Level
from levels.haze_forest import haze_forest_data

def main():
  pygame.init()
  screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
  pygame.display.set_caption("Timeforge: The Last Knight")

  level = Level(screen, haze_forest_data)
  level.run()

  pygame.quit()

if __name__ == "__main__":
  main()