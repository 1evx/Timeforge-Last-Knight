# scripts/level.py

import pygame
from scripts.Settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scripts.Valk import Valk
from scripts.Background import ParallaxBackground
from scripts.load_and_slice import slice_tileset
from scripts.camera import Camera
from scripts.Skeleton import Skeleton
from scripts.Slime import Slime
from scripts.Nightborne import Nightborne
from scripts.Fireborne import Fireborne
from scripts.SkeletonArcher import SkeletonArcher
from scripts.Necromancer import Necromancer
from scripts.Shop import Shop
from scripts.Projectile import Projectile
from scripts.combat_manager import CombatManager


class Level:
  def __init__(self, screen, level_data):
    self.screen = screen
    self.clock = pygame.time.Clock()
    self.running = True

    # Load level data
    self.tile_size = 48
    self.level_width = level_data["level_width"]
    self.tiles_per_row = level_data["tiles_per_row"]

    # Camera
    self.camera = Camera(SCREEN_WIDTH, self.level_width)

    # Background
    self.background = ParallaxBackground(level_data["backgrounds"], SCREEN_WIDTH, SCREEN_HEIGHT)

    # Ground tiles
    self.ground_tile = slice_tileset(level_data["tileset"], self.tile_size, self.tile_size, scale=2)

    # Deco
    self.decor_group = pygame.sprite.Group()

    for obj in level_data["decor"]:
      x, y = obj["pos"]
      if obj["type"] == "Shop":
        shop = Shop(x, y)
        self.decor_group.add(shop)
      # elif obj["type"] == "Bush":
      #   bush = Bush(obj["x"], obj["y"])
      #   self.decor_group.add(bush)

    # Player
    self.player = Valk(100, SCREEN_HEIGHT - 200)
    self.camera.follow(self.player)

    # Enemies
    self.enemy_group = pygame.sprite.Group()
    self.projectile_group = pygame.sprite.Group()

    for enemy_info in level_data["enemies"]:
      enemy_type = enemy_info["type"]
      x, y = enemy_info["pos"]

      if enemy_type == "Skeleton":
        enemy = Skeleton(x, y, self.player)
      elif enemy_type == "Slime":
        enemy = Slime(x, y, self.player)
      elif enemy_type == "Nightborne":
        enemy = Nightborne(x, y, self.player)
      elif enemy_type == "Fireborne":
        enemy = Fireborne(x, y, self.player)
      elif enemy_type == "SkeletonArcher":
        enemy = SkeletonArcher(x, y, self.player, self.projectile_group)
      elif enemy_type == "Necromancer":
        enemy = Necromancer(x, y, self.player, self.projectile_group)
      else:
        continue

      self.enemy_group.add(enemy)

    self.combat_manager = CombatManager(self.player, self.enemy_group)

  def run(self):
    while self.running:
      self.clock.tick(FPS)
      keys = pygame.key.get_pressed()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            self.player.attack()
          elif event.button == 3:
            self.player.dash_attack()

      # Combat checks
      self.combat_manager.check_collisions()

      # Update
      self.player.update(keys)
      self.enemy_group.update()
      self.decor_group.update()
      self.projectile_group.update()
      self.camera.update()
      self.background.update(self.camera.get_offset())

      # Draw
      self.background.draw(self.screen)
      self.projectile_group.draw(self.screen)

      # Draw camera debug
      for i, x in enumerate(range(0, self.level_width, self.tile_size * 2)):
        screen_x = x - self.camera.get_offset()
        if -self.tile_size * 2 <= screen_x <= SCREEN_WIDTH:
          tile = self.ground_tile[3]
          self.screen.blit(tile, (screen_x, SCREEN_HEIGHT - 50))

      for decor in self.decor_group:
        self.screen.blit(decor.image, self.camera.apply(decor.rect))

      for enemy in self.enemy_group:
        self.screen.blit(enemy.image, self.camera.apply(enemy.rect))

      self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

      pygame.display.flip()

  def stop(self):
    self.running = False
