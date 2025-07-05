from scripts.Settings import SCREEN_HEIGHT
from scripts.utils import generate_tile_row

# -------------------------------
oak_forest_data = {
  "level_width": 8000,
  "tiles_per_row": 100,
  "tileset": "assets/tiles/oak_woods_tileset.png",
  "backgrounds": [
    ("assets/backgrounds/background_layer_1.png", 0.2),
    ("assets/backgrounds/background_layer_2.png", 0.5),
    ("assets/backgrounds/background_layer_3.png", 0.8)
  ],
  "decor": [
    {"type": "Fence1", "pos": [650, SCREEN_HEIGHT - 100]},
    {"type": "Fence2", "pos": [850, SCREEN_HEIGHT - 100]},
    {"type": "Lamp", "pos": [1200, SCREEN_HEIGHT - 192]},
    {"type": "FallenWhiteVanguard", "pos": [1300, SCREEN_HEIGHT - 175]},
    {"type": "Cart", "pos": [1500, SCREEN_HEIGHT - 160]},
    {"type": "Barricade", "pos": [1700, SCREEN_HEIGHT - 119]},
    {"type": "Vase_1", "pos": [1740, SCREEN_HEIGHT - 109]},
    {"type": "Lamp", "pos": [2000, SCREEN_HEIGHT - 192]},
    {"type": "Sign", "pos": [2300, SCREEN_HEIGHT - 120]},
    {"type": "Fireplace", "pos": [3000, SCREEN_HEIGHT - 80]},
    {"type": "Wall", "pos": [3000, SCREEN_HEIGHT - 160]},
    {"type": "Shop", "pos": [6500, SCREEN_HEIGHT - 405]},
  ],
  "tiles": [
    {"pos": [2300, 670], "tile_index": 2},
  ],
  "enemies": [
    {"type": "Slime", "pos": [6000, SCREEN_HEIGHT - 120]},
    # {"type": "Skeleton", "pos": [1900, SCREEN_HEIGHT - 185]},
    # {"type": "Nightborne", "pos": [3900, SCREEN_HEIGHT - 300]},
    # {"type": "Fireborne", "pos": [2000, SCREEN_HEIGHT - 370]},
    # {"type": "SkeletonArcher", "pos": [1900, SCREEN_HEIGHT - 305]},
    # {"type": "Necromancer", "pos": [1000, SCREEN_HEIGHT - 230]}
  ]
}

# Add a strip of alternating ground tiles:
row = generate_tile_row(
  start_x=2300,
  y=670,
  tile_indices=[2, 1],   # your pattern
  tile_width=40,
  count=15               # how many tiles
)
oak_forest_data["tiles"].extend(row)
row2 = generate_tile_row(
  start_x=3300,
  y=670,
  tile_indices=[2, 1],   # your pattern
  tile_width=40,
  count=60               # how many tiles
)
oak_forest_data["tiles"].extend(row2)