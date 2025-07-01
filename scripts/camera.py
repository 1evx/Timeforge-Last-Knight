class Camera:
  def __init__(self, screen_width, level_width):
    self.offset_x = 0
    self.screen_width = screen_width
    self.level_width = level_width
    self.target = None

  def follow(self, target):
    """Assign the object (usually player) to follow"""
    self.target = target

  def update(self):
    if self.target:
      # Center camera on player
      center_x = self.target.rect.centerx
      self.offset_x = center_x - self.screen_width // 2

      # Clamp camera to level bounds
      self.offset_x = max(0, min(self.offset_x, self.level_width - self.screen_width))

  def apply(self, rect):
    """Return a shifted version of any object's rect"""
    return rect.move(-self.offset_x, 0)

  def get_offset(self):
    return self.offset_x
