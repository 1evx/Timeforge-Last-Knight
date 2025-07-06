from scripts.Settings import SCREEN_HEIGHT
from scripts.utils import generate_tile_row

crystal_cave_data = {
  "level_width": 8000,
  "tiles_per_row": 100,
  "tileset": "assets/tiles/oak_woods_tileset.png",
  "backgrounds": [
    ("assets/backgrounds/background1.png", 0.2),
    ("assets/backgrounds/background3.png", 0.5),
    ("assets/backgrounds/background4b.png", 0.8)
  ],
  "decor": [
    {"type": "Fence1", "pos": [650, SCREEN_HEIGHT - 100]},
    {"type": "Fence2", "pos": [850, SCREEN_HEIGHT - 100]},
    {"type": "Lamp", "pos": [1200, SCREEN_HEIGHT - 192]},
    {"type": "FallenWhiteVanguard", "pos": [1300, SCREEN_HEIGHT - 175]},
    {"type": "Cart", "pos": [1500, SCREEN_HEIGHT - 160]},
    {"type": "Barricade", "pos": [1700, SCREEN_HEIGHT - 119]},
    {"type": "Vase_1", "pos": [1740, SCREEN_HEIGHT - 109]},
    {"type": "FallenSkeleton1", "pos": [1800, SCREEN_HEIGHT - 175]}, 
    {"type": "Lamp", "pos": [2000, SCREEN_HEIGHT - 192]},
    {"type": "Sign", "pos": [2300, SCREEN_HEIGHT - 120]},
    {"type": "Grass_1", "pos": [2400, SCREEN_HEIGHT - 55]},
    {"type": "Rock_1", "pos": [2500, SCREEN_HEIGHT - 70]}, 
    {"type": "Grass_3", "pos": [2600, SCREEN_HEIGHT - 55]},
    {"type": "Grass_2", "pos": [2700, SCREEN_HEIGHT - 60]},
    {"type": "Rock_2", "pos": [2800, SCREEN_HEIGHT - 70]}, 
    {"type": "FallenSkeleton2", "pos": [2900, SCREEN_HEIGHT - 175]}, 
    {"type": "Wall", "pos": [3000, SCREEN_HEIGHT - 160]},
    {"type": "Fireplace", "pos": [3300, SCREEN_HEIGHT - 80]},
    {"type": "Grass_3", "pos": [3500, SCREEN_HEIGHT - 55]},
    {"type": "Grass_1", "pos": [3700, SCREEN_HEIGHT - 55]}, 
    {"type": "Grass_2", "pos": [4000, SCREEN_HEIGHT - 60]}, 
    {"type": "Shop", "pos": [6500, SCREEN_HEIGHT - 405]},
  ],
  "tiles": [
    {"pos": [2300, 670], "tile_index": 2},
    {"pos": [3400, 670], "tile_index": 2},
    # {"pos": [4000, 620], "tile_index": 2},
  ],
  "enemies": [
    # {"type": "Slime", "pos": [5800, SCREEN_HEIGHT - 120]},
    # {"type": "Skeleton", "pos": [1900, SCREEN_HEIGHT - 185]},
    {"type": "Nightborne", "pos": [3900, SCREEN_HEIGHT - 300]},
    {"type": "Fireborne", "pos": [2000, SCREEN_HEIGHT - 370]},
    # {"type": "SkeletonArcher", "pos": [1900, SCREEN_HEIGHT - 305]},
    {"type": "Necromancer", "pos": [1000, SCREEN_HEIGHT - 230]}
  ]
}