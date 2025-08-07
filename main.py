import pygame
from scripts import Settings
from scripts.Level import Level
from levels.oak_forest import oak_forest_data
from levels.haze_forest import haze_forest_data
from levels.crystal_cave import crystal_cave_data
from levels.dark_castle import dark_castle_data
from scripts.Menu import Menu
from scripts.utils import fade
from scripts.UI import DemoEndScreen 

def main():
  while True:
    money = 0
    player_health = 10
    player_speed = 5
    player_max_health = 10
    player_power = 1
    
    pygame.init()
    screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Timeforge: The Last Knight")
    
    levels = [oak_forest_data, haze_forest_data, crystal_cave_data, dark_castle_data]
    menu = Menu(screen)
    if not menu.run():
      pygame.quit()
      return

    # Main game level loop
    for i, level_data in enumerate(levels):
      fade(screen, fade_in=True, speed=5)
      level = Level(screen, level_data, money, player_health, player_speed, player_max_health, player_power)
      level.run()
      money = level.player.money
      player_health = level.player.health
      player_speed = level.player.speed
      player_max_health = level.player.max_health
      player_power = level.player.attack_power
  
      if not level.has_finished:
        pygame.quit()
        return

      if i < len(levels) - 1:
        fade(screen, fade_in=False, speed=5)

    # After last level, show Demo Complete screen
    demo_screen = DemoEndScreen(screen, Settings)
    demo_screen.active = True
    showing_demo_screen = True

    while showing_demo_screen:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return
        result = demo_screen.handle_event(event)
        if result == "menu":
          showing_demo_screen = False  # Go back to menu (loop restarts)
      
      demo_screen.draw()
      pygame.display.flip()

if __name__ == "__main__":
  main()