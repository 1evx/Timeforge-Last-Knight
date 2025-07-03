import pygame
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scripts.Valk import Valk
from scripts.background import ParallaxBackground
from scripts.load_and_slice import slice_tileset
from scripts.camera import Camera
from scripts.Skeleton import Skeleton
from scripts.Slime import Slime
from scripts.Nightborne import Nightborne
from scripts.Fireborne import Fireborne
from scripts.SkeletonArcher import SkeletonArcher
from scripts.Necromancer import Necromancer
from scripts.Projectile import Projectile
from scripts.combat_manager import CombatManager

tile_size = 24
level_width = 5000  # or based on tile count
tiles_per_row = 100
tile_size = 48
level_width = tiles_per_row * tile_size
camera = Camera(SCREEN_WIDTH, level_width)

def main():
  pygame.init()
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Side Scroller: Dark Wood Level")
  clock = pygame.time.Clock()

  running = True

  # Load Materials
  background = ParallaxBackground([
    ("assets/backgrounds/background_layer_1.png", 0.2),
    ("assets/backgrounds/background_layer_2.png", 0.5),
    ("assets/backgrounds/background_layer_3.png", 0.8)
  ], SCREEN_WIDTH, SCREEN_HEIGHT)

  ground_tile = slice_tileset("assets/tiles/oak_woods_tileset.png", tile_size, tile_size, scale=2)

  # Player components
  player = Valk(100, SCREEN_HEIGHT - 200)
  camera.follow(player) # Camera

  # Enemy groups
  enemy_group = pygame.sprite.Group()
  projectile_group = pygame.sprite.Group()
  skeleton = Skeleton(1900, SCREEN_HEIGHT - 185, player)
  slime = Slime(3000, SCREEN_HEIGHT - 120, player)
  nightborne = Nightborne(3900, SCREEN_HEIGHT - 300, player)
  fireborne = Fireborne(2000, SCREEN_HEIGHT - 370, player)
  skeletonAcher = SkeletonArcher(1900, SCREEN_HEIGHT - 305, player, projectile_group)
  necromancer = Necromancer(1000, SCREEN_HEIGHT - 305, player, projectile_group)
  enemy_group.add(skeleton)
  enemy_group.add(slime)
  enemy_group.add(nightborne)
  enemy_group.add(fireborne)
  enemy_group.add(skeletonAcher)
  enemy_group.add(necromancer)
  combat_manager = CombatManager(player, enemy_group) # Combat manager

  while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          player.attack()
        elif event.button == 3:
          player.dash_attack()
    
    # player_attack_hitbox = player.get_attack_hitbox()
    # player_offset_hitbox = player_attack_hitbox.move(-camera.get_offset(), 0)
    # offset_player_hitbox = player.hitbox.move(-camera.get_offset(), 0)

    skeletonAcher_attack_hitbox = skeletonAcher.get_attack_hitbox()
    skeletonAcher_offset_hitbox = skeletonAcher_attack_hitbox.move(-camera.get_offset(), 0)
    offset_skeletonAcher_hitbox = skeletonAcher.hitbox.move(-camera.get_offset(), 0)

    necromancer_attack_hitbox = necromancer.get_attack_hitbox()
    necromancer_offset_hitbox = necromancer_attack_hitbox.move(-camera.get_offset(), 0)
    offset_necromancer_hitbox = necromancer.hitbox.move(-camera.get_offset(), 0)
 
    combat_manager.check_collisions() # Check combat

    # Update
    player.update(keys)
    enemy_group.update()
    projectile_group.update()
    camera.update()
    background.update(camera.get_offset())

    # Draw background
    background.draw(screen)
    projectile_group.draw(screen)

    # Debug
    # pygame.draw.rect(screen, (255, 0, 0), player_offset_hitbox, 2)
    # pygame.draw.rect(screen, (0, 255, 0), offset_player_hitbox, 2)
    pygame.draw.rect(screen, (255, 0, 0), skeletonAcher_offset_hitbox, 2)
    pygame.draw.rect(screen, (0, 255, 0), offset_skeletonAcher_hitbox, 2)
    pygame.draw.rect(screen, (255, 0, 0), necromancer_offset_hitbox, 2)
    pygame.draw.rect(screen, (0, 255, 0), offset_necromancer_hitbox, 2)

    # Draw camera
    for i, x in enumerate(range(0, level_width, tile_size * 2)):
      screen_x = x - camera.get_offset()
      if -tile_size * 2 <= screen_x <= SCREEN_WIDTH:
        tile = ground_tile[3] 
        screen.blit(tile, (screen_x, SCREEN_HEIGHT-50))

    # Draw player
    screen.blit(player.image, camera.apply(player.rect))

    # Draw enemies
    for enemy in enemy_group:
      screen.blit(enemy.image, camera.apply(enemy.rect))

    pygame.display.flip()

  pygame.quit()

if __name__ == "__main__":
  main()
