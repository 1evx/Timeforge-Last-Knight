import pygame
from scripts import Settings
from scripts.GoldEffect import GoldEffect
from scripts.Settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scripts.UI import GameOverPopup
from scripts.Valk import Valk
from scripts.Background import ParallaxBackground
from scripts.utils import load_tileset, slice_tileset, fade
from scripts.camera import Camera
from scripts.Skeleton import Skeleton
from scripts.Slime import Slime
from scripts.Nightborne import Nightborne
from scripts.Fireborne import Fireborne
from scripts.Necromancer import Necromancer
from scripts.Deathborne import Deathborne
from scripts.Goblin import Goblin
from scripts.Mushroom import Mushroom
from scripts.ShieldSkeleton import ShieldSkeleton
from scripts.Shop import Shop
from scripts.PracticeTarget import PracticeTarget
from scripts.Platform import Platform
from scripts.combat_manager import CombatManager
from scripts.tutorials import Tutorial
from assets.decorations.deco import DECOR_DEFINITIONS
from scripts.Gem import Gem

class Level:
    def __init__(self, screen, level_data, money, health, speed, max_health, power):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.tile_size = 48
        self.level_width = level_data["level_width"]
        self.tiles_per_row = level_data["tiles_per_row"]
        self.level_data = level_data
        self.has_finished = False
        self.state = "playing"
        self.death_timer = 0
        self.death_delay = 2000  # 2 seconds for death animation
        self.game_over_sound_played = False
        self.money = money

        # Camera and background
        self.camera = Camera(SCREEN_WIDTH, self.level_width)
        self.background = ParallaxBackground(level_data["backgrounds"], SCREEN_WIDTH, SCREEN_HEIGHT)

        # Load tiles
        tileset_image = pygame.image.load(level_data["tileset"]).convert_alpha()
        self.tileset_tiles = load_tileset(tileset_image, 24, 24, scale=2)
        self.platforms = pygame.sprite.Group()
        for tile_data in self.level_data["tiles"]:
            x, y = tile_data["pos"]
            index = tile_data["tile_index"]
            tile_image = self.tileset_tiles[index]
            tile = Platform(x, y, tile_image)
            self.platforms.add(tile)
        self.ground_tile = slice_tileset(self.level_data["tileset"], self.tile_size, self.tile_size, scale=2)

        # Decorations
        self.decor_group = pygame.sprite.Group()
        self.shop_group = pygame.sprite.Group()

        for obj in self.level_data["decor"]:
            decor_type = obj["type"]
            pos = obj["pos"]
            if decor_type == "Shop":
                shop = Shop(*pos)
                self.shop_group.add(shop)
            else:
                sprite = self.create_decor_sprite(decor_type, pos)
                self.decor_group.add(sprite)

        # Sound Effects
        self.background_music = level_data["background_music"]

        # Player
        self.player = Valk(100, SCREEN_HEIGHT - 200, money, health, speed, max_health, power)
        self.camera.follow(self.player)
        self.current_health = health
        self.current_speed = speed
        self.current_max_health = max_health
        self.current_money = money
        self.current_power = power

        # Tutorial system (only for oak forest level)
        self.tutorial = None
        # Check if this is the oak forest level by checking the level data structure
        if (self.level_data.get('level_width') == 8000 and 
            self.level_data.get('tiles_per_row') == 100 and
            'hall-of-king.mp3' in self.level_data.get('background_music', '')):
            self.tutorial = Tutorial(self.screen)

        # Enemies, projectiles, and coins, gems
        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()

        self.gem_group = pygame.sprite.Group()

        self.coin_effect = pygame.sprite.Group()

        self._initialize_enemies()
        self._initialize_gems()

        self.combat_manager = CombatManager(self.player, self.enemy_group)
        self.game_over_popup = GameOverPopup(self.screen, Settings)
        self.play_music()

    def play_music(self, loop=-1):
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=loop)

    def _initialize_enemies(self):
        """Initialize or reinitialize enemies based on level data."""
        for enemy_info in self.level_data["enemies"]:
            enemy_type = enemy_info["type"]
            x, y = enemy_info["pos"]
            if enemy_type == "Skeleton":
                enemy = Skeleton(x, y, self.player, self.coin_group)
            elif enemy_type == "Slime":
                enemy = Slime(x, y, self.player, self.coin_group)
            elif enemy_type == "Nightborne":
                enemy = Nightborne(x, y, self.player, self.coin_group)
            elif enemy_type == "Fireborne":
                enemy = Fireborne(x, y, self.player, self.coin_group)
            elif enemy_type == "Necromancer":
                enemy = Necromancer(x, y, self.player, self.projectile_group, self.coin_group)
            elif enemy_type == "PracticeTarget":
                enemy = PracticeTarget(x, y)
            elif enemy_type == "Goblin":
                enemy = Goblin(x, y, self.player, self.coin_group)
            elif enemy_type == "Mushroom":
                enemy = Mushroom(x, y, self.player, self.coin_group)
            elif enemy_type == "ShieldSkeleton":
                enemy = ShieldSkeleton(x, y, self.player, self.coin_group)
            elif enemy_type == "Deathborne":
                enemy = Deathborne(x, y, self.player, self.coin_group)
            else:
                continue
            if enemy is not None:
                self.enemy_group.add(enemy)

    def _initialize_gems(self):
        """Initialize gems based on level data."""
        if "gems" in self.level_data:
            for gem_info in self.level_data["gems"]:
                gem_type = gem_info.get("type", "ruby")
                x, y = gem_info["pos"]
                gem = Gem(x, y, gem_type)
                self.gem_group.add(gem)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif self.state == "game_over":
                    action = self.game_over_popup.handle_event(event)
                    if action == "restart":
                        self.reset_level()
                    elif action == "quit":
                        self.running = False
                        self.has_finished = False

                elif self.state == "playing":
                    shop_ui_active = any(shop.show_ui for shop in self.shop_group)

                    # If a shop UI is active, forward events to it and block other inputs
                    if shop_ui_active:
                        for shop in self.shop_group:
                            if shop.show_ui:
                                shop.handle_input(event, self.player)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                                    shop.show_ui = False  # Close shop with E
                        continue  # Skip player controls if shop UI is active

                    # Player presses E to open shop
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                        for shop in self.shop_group:
                            if shop.show_prompt:
                                shop.show_ui = True
                                break  # Only open one shop

                    # Handle tutorial completion input
                    if self.tutorial and self.tutorial.handle_completion_input(event):
                        self.tutorial = None  # Remove tutorial after completion
                        continue

                    # Only allow combat input if no UI is active    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.player.attack()
                        elif event.button == 3:
                            self.player.dash_attack()

            if self.state == "playing":
                # Update tutorial if active
                if self.tutorial and not self.tutorial.is_tutorial_complete():
                    mouse_buttons = pygame.mouse.get_pressed()
                    self.tutorial.update(keys, mouse_buttons, self.player)
                
                self.combat_manager.check_collisions()
                self.player.update(keys, self.platforms)
                self.decor_group.update()
                self.shop_group.update(self.player)
                for shop in self.shop_group: shop.check_interaction(self.player)
                self.enemy_group.update()
                self.gem_group.update()
                self.projectile_group.update()
                self.camera.update()
                self.background.update(self.camera.get_offset())
                self.coin_group.update()
                self.coin_effect.update()

                self.check_coin_collection()
                self.check_gem_collection()

                if not self.player.alive and self.state != "death_wait":
                    self.state = "death_wait"
                    self.death_timer = pygame.time.get_ticks()

            elif self.state == "death_wait":
                self.player.update(keys, self.platforms)  # For death animation
                current_time = pygame.time.get_ticks()
                if current_time - self.death_timer >= self.death_delay:
                    self.state = "game_over"
                    self.game_over_popup.active = True

            # Draw
            self.background.draw(self.screen)

            for gem in self.gem_group:
                screen_rect = self.camera.apply(gem.rect)
                if screen_rect:
                    self.screen.blit(gem.image, screen_rect)

            for deco in self.decor_group:
                self.screen.blit(deco.image, self.camera.apply(deco.rect))

            for shop in self.shop_group:
                self.screen.blit(shop.image, self.camera.apply(shop.rect))

            for shop in self.shop_group:
                shop.draw_prompt(self.screen, self.camera)
                shop.draw_ui(self.screen, self.player)

            # Projectile
            for projectile in self.projectile_group:
                screen_rect = self.camera.apply(projectile.rect)
                self.screen.blit(projectile.image, screen_rect)

            for i, x in enumerate(range(0, self.level_width, self.tile_size * 2)):
                screen_x = x - self.camera.get_offset()
                if -self.tile_size * 2 <= screen_x <= SCREEN_WIDTH:
                    tile = self.ground_tile[3]
                    self.screen.blit(tile, (screen_x, SCREEN_HEIGHT - 50))

            for tile in self.platforms:
                self.screen.blit(tile.image, self.camera.apply(tile.rect))

            for enemy in self.enemy_group:
                screen_rect = self.camera.apply(enemy.rect)
                self.screen.blit(enemy.image, screen_rect)
                enemy.draw_health_bar(self.screen, screen_rect)

            for coin in self.coin_group:
                self.screen.blit(coin.image, self.camera.apply(coin.rect))

            for effect in self.coin_effect:
                self.screen.blit(effect.image, self.camera.apply(effect.rect))

            self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
            self.player.draw_health_bar(self.screen, self.camera.apply(self.player.rect))
            self.player.draw_hud_status_bars(self.screen)
            self.player.draw_hud_gold(self.screen)
            self.player.draw_hud_gems(self.screen)  # Add this line

            
            # Draw tutorial UI
            if self.tutorial:
                if self.tutorial.is_tutorial_complete():
                    self.tutorial.draw_completion_screen()
                else:
                    self.tutorial.draw()


            if self.state == "game_over":
                pygame.mixer.music.stop()
                if not self.game_over_sound_played:
                    gameOver_sound = pygame.mixer.Sound("assets/sound effect/game-over.mp3")
                    gameOver_sound.play()
                    self.game_over_sound_played = True
                self.game_over_popup.draw()

            # Check level completion (for oak forest, require tutorial completion)
            if self.tutorial and not self.tutorial.is_tutorial_complete():
                # Don't complete level until tutorial is done
                pass
            elif self.check_level_complete():
                self.has_finished = True
                self.running = False
            if self.has_finished:
                pygame.mixer.music.stop()
                levelComplete_sound = pygame.mixer.Sound("assets/sound effect/levelWin.mp3")
                levelComplete_sound.play()

            pygame.display.flip()

    def reset_level(self):
        self.player = Valk(100, SCREEN_HEIGHT - 200, self.current_money, self.current_health, self.current_speed, self.current_max_health, self.current_power)
        self.camera.follow(self.player)
        self.combat_manager.player = self.player
        self.enemy_group.empty()
        self.projectile_group.empty()
        self.coin_group.empty()
        self.gem_group.empty()  # Add this line

        self._initialize_enemies()  # Reuse enemy initialization
        self._initialize_gems()

        self.state = "playing"
        self.game_over_popup.active = False

        self.game_over_sound_played = False
        self.play_music()

        fade(self.screen, fade_in=True)

    def stop(self):
        self.running = False

    def check_level_complete(self):
        return self.player.rect.right >= self.level_width + 130

    def create_decor_sprite(self, decor_type, pos):
        image = pygame.image.load(DECOR_DEFINITIONS[decor_type]["path"]).convert_alpha()
        scale = DECOR_DEFINITIONS[decor_type]["scale"]
        image = pygame.transform.scale_by(image, scale)

        rotation = DECOR_DEFINITIONS[decor_type].get("rotation", 0)
        if rotation:
            image = pygame.transform.rotate(image, rotation)

        direction = DECOR_DEFINITIONS[decor_type].get("direction", 1)
        if direction == -1:
            image = pygame.transform.flip(image, True, False)

        sprite = pygame.sprite.Sprite()
        sprite.image = image
        sprite.rect = sprite.image.get_rect(topleft=pos)
        return sprite

    def check_coin_collection(self):
        player_center = self.player.rect.center
        for coin in self.coin_group.copy():
            if coin.can_be_collected() and coin.rect.collidepoint(player_center):
                self.player.money += 1
                coin.kill()
                coin_sound = pygame.mixer.Sound("assets/sound effect/collect-coin.mp3")
                coin_sound.play()
                
                 effect = GoldEffect(coin.rect.centerx, coin.rect.centery)
                self.coin_effect.add(effect)

    def check_gem_collection(self):
        for gem in self.gem_group.copy():
            if gem.can_be_collected(self.player.rect):
                gem.collect()
                self.player.gems_collected += 1  # Add this line
                # Restore full health when gem is collected
                self.player.health = 10  # Restore to max health
                try:
                    gem_sound = pygame.mixer.Sound("assets/sound effect/collect-coin.mp3")
                    gem_sound.play()
                except:
                    pass

