# scripts/level.py

import pygame
from scripts.Settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scripts.Valk import Valk
from scripts.Background import ParallaxBackground
from scripts.utils import load_tileset, slice_tileset
from scripts.camera import Camera
from scripts.Skeleton import Skeleton
from scripts.Slime import Slime
from scripts.Nightborne import Nightborne
from scripts.Fireborne import Fireborne
from scripts.SkeletonArcher import SkeletonArcher
from scripts.Necromancer import Necromancer
from scripts.Shop import Shop
from scripts.Platform import Platform
from scripts.Projectile import Projectile
from scripts.combat_manager import CombatManager
from assets.decorations.deco import DECOR_DEFINITIONS

class Level:
  def __init__(self, screen, level_data):
    self.screen = screen
    self.clock = pygame.time.Clock()
    self.running = True

    # Load level data
    self.tile_size = 48
    self.level_width = level_data["level_width"]
    self.tiles_per_row = level_data["tiles_per_row"]
    self.level_data = level_data
    self.has_finished = False

    # Camera
    self.camera = Camera(SCREEN_WIDTH, self.level_width)

    # Background
    self.background = ParallaxBackground(level_data["backgrounds"], SCREEN_WIDTH, SCREEN_HEIGHT)

    # Ground tiles
    tileset_image = pygame.image.load(level_data["tileset"]).convert_alpha()
    self.tileset_tiles = load_tileset(tileset_image, 24, 24, scale=2)

    self.platforms = pygame.sprite.Group()
    for tile_data in level_data["tiles"]:
      x, y = tile_data["pos"]
      index = tile_data["tile_index"]
      tile_image = self.tileset_tiles[index]
      tile = Platform(x, y, tile_image)
      self.platforms.add(tile)

    self.ground_tile = slice_tileset(level_data["tileset"], self.tile_size, self.tile_size, scale=2)

    # Deco
    self.decor_group = pygame.sprite.Group()

    for obj in level_data["decor"]:
      decor_type = obj["type"]
      pos = obj["pos"]
      if decor_type == "Shop":
        shop = Shop(*pos)
        self.decor_group.add(shop)
      else:
        sprite = self.create_decor_sprite(decor_type, pos)
        self.decor_group.add(sprite)
   

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
      self.player.update(keys, self.platforms)
      self.decor_group.update()
      self.enemy_group.update()
      self.projectile_group.update()
      self.camera.update()
      self.background.update(self.camera.get_offset())

      # Draw
      self.background.draw(self.screen)
      self.projectile_group.draw(self.screen)

      # Draw camera debug
      for deco in self.decor_group:
        self.screen.blit(deco.image, self.camera.apply(deco.rect))

      for i, x in enumerate(range(0, self.level_width, self.tile_size * 2)):
        screen_x = x - self.camera.get_offset()
        if -self.tile_size * 2 <= screen_x <= SCREEN_WIDTH:
          tile = self.ground_tile[3]
          self.screen.blit(tile, (screen_x, SCREEN_HEIGHT - 50))

      for tile in self.platforms:
        self.screen.blit(tile.image, self.camera.apply(tile.rect))

      for enemy in self.enemy_group:
        self.screen.blit(enemy.image, self.camera.apply(enemy.rect))

      self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

      if self.check_level_complete():
        self.has_finished = True
        self.running = False

      pygame.display.flip()

  def stop(self):
    self.running = False

  def check_level_complete(self):
    # Replace with your own condition
    # Example: player reaches right edge of map
    if self.player.rect.right >= self.level_width:
      return True
    return False

  def create_decor_sprite(self, decor_type, pos):
    image = pygame.image.load(DECOR_DEFINITIONS[decor_type]["path"]).convert_alpha()
    # Apply scale
    scale = DECOR_DEFINITIONS[decor_type]["scale"]
    image = pygame.transform.scale_by(image, scale)

    # Apply optional rotation
    rotation = DECOR_DEFINITIONS[decor_type].get("rotation", 0)
    if rotation:
      image = pygame.transform.rotate(image, rotation)

    # Optional horizontal flip
    direction = DECOR_DEFINITIONS[decor_type].get("direction", 1)
    if direction == -1:
      image = pygame.transform.flip(image, True, False)

    # Create sprite
    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = sprite.image.get_rect(topleft=pos)
    return sprite
