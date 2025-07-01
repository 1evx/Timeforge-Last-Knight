import pygame

class CombatManager:
  def __init__(self, player, enemies):
    self.player = player
    self.enemies = enemies
    self.already_hit = set()


  def check_collisions(self):
    current_time = pygame.time.get_ticks()
    windup = self.player.attack_windup_map.get(self.player.attack_stage, 0)

    # Enemies attacking player:
    for enemy in self.enemies:
      if hasattr(enemy, "get_attack_hitbox"):
        if enemy.state == "attack":
          now = pygame.time.get_ticks()
          if now - enemy.attack_timer >= enemy.attack_windup:
            current_frame = enemy.get_current_attack_frame()
            windup_passed = pygame.time.get_ticks() - enemy.attack_timer >= enemy.attack_windup
            if windup_passed:
              if enemy.attack_active_frames[0] <= current_frame <= enemy.attack_active_frames[1]:
                if not hasattr(enemy, "last_hit") or now - enemy.last_hit >= 500:
                  enemy.last_hit = now

    # Player attacking enemies:
    if (self.player.is_attacking and (current_time - self.player.attack_timer >= windup)):
      if self.player.state in ["attack1", "attack2", "dash_attack"]:
        player_hitbox = self.player.get_attack_hitbox()
        for enemy in self.enemies:
          if (player_hitbox.colliderect(enemy.hitbox) and enemy not in self.already_hit and enemy.alive):
            enemy.take_damage(self.player.attack_damage)
            self.already_hit.add(enemy)
    else:
      self.already_hit.clear()