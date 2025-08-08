from scripts.Settings import SCREEN_HEIGHT
from scripts.utils import generate_tile_row

oak_forest_data = {
  "level_width": 8000,
  "tiles_per_row": 100,
  "tileset": "assets/tiles/oak_woods_tileset.png",
  "background_music": "assets/audio/music/hall-of-king.mp3",
  "backgrounds": [
    ("assets/backgrounds/of_layer_1.png", 0.2),
    ("assets/backgrounds/of_layer_2.png", 0.5),
    ("assets/backgrounds/of_layer_3.png", 0.8)
  ],
  "decor": [
    {"type": "Fence1", "pos": [650, SCREEN_HEIGHT - 100]},
    {"type": "Fence2", "pos": [850, SCREEN_HEIGHT - 100]},
    {"type": "Lamp", "pos": [1200, SCREEN_HEIGHT - 192]},
    {"type": "FallenWhiteVanguard", "pos": [1350, SCREEN_HEIGHT - 175]},
    {"type": "Cart", "pos": [1500, SCREEN_HEIGHT - 160]},
    {"type": "Barricade", "pos": [1700, SCREEN_HEIGHT - 119]},
    {"type": "Vase_1", "pos": [1750, SCREEN_HEIGHT - 109]},
    {"type": "Vase_2", "pos": [1800, SCREEN_HEIGHT - 90]},
    {"type": "FallenSkeleton1", "pos": [1850, SCREEN_HEIGHT - 175]}, 
    {"type": "Lamp", "pos": [2000, SCREEN_HEIGHT - 192]},
    {"type": "Sign", "pos": [2300, SCREEN_HEIGHT - 120]},
    {"type": "Grass_1", "pos": [2400, SCREEN_HEIGHT - 55]},
    {"type": "Rock_1", "pos": [2500, SCREEN_HEIGHT - 70]}, 
    {"type": "Grass_3", "pos": [2600, SCREEN_HEIGHT - 55]},
    {"type": "Grass_2", "pos": [2700, SCREEN_HEIGHT - 60]},
    {"type": "Rock_2", "pos": [2800, SCREEN_HEIGHT - 70]}, 
    {"type": "Wall", "pos": [3000, SCREEN_HEIGHT - 160]},
    {"type": "Latern_1", "pos": [3200, SCREEN_HEIGHT - 100]},
    {"type": "Vase_1", "pos": [3300, SCREEN_HEIGHT - 109]},
    {"type": "Vase_2", "pos": [3320, SCREEN_HEIGHT - 90]},
    {"type": "Booth_1", "pos": [3400, SCREEN_HEIGHT - 260]},
    {"type": "Tableset_1", "pos": [3700, SCREEN_HEIGHT - 130]},
    {"type": "Grass_2", "pos": [4000, SCREEN_HEIGHT - 60]}, 
    {"type": "Grass_1", "pos": [4200, SCREEN_HEIGHT - 55]},
    {"type": "Rock_1", "pos": [4300, SCREEN_HEIGHT - 70]}, 
    {"type": "Fireplace", "pos": [4350, SCREEN_HEIGHT - 80]},
    {"type": "Grass_3", "pos": [4700, SCREEN_HEIGHT - 55]},
    {"type": "Grass_1", "pos": [5000, SCREEN_HEIGHT - 55]},
    {"type": "Grass_2", "pos": [5300, SCREEN_HEIGHT - 60]}, 
    {"type": "Fence1", "pos": [5400, SCREEN_HEIGHT - 100]},
    {"type": "Fence2", "pos": [5600, SCREEN_HEIGHT - 100]},
    {"type": "Grass_3", "pos": [5600, SCREEN_HEIGHT - 55]},
    {"type": "Shop", "pos": [6500, SCREEN_HEIGHT - 405]}, # A Funtional Class
    {"type": "Sign", "pos": [7600, SCREEN_HEIGHT - 120]},
  ],
  "tiles": [
    {"pos": [2300, 670], "tile_index": 2},
    {"pos": [4000, 670], "tile_index": 2},
  ],
  "enemies": [
    {"type": "PracticeTarget", "pos": [2600, SCREEN_HEIGHT - 160]}, 
    {"type": "Slime", "pos": [3500, SCREEN_HEIGHT - 120]},
    {"type": "Slime", "pos": [4000, SCREEN_HEIGHT - 120]},
    {"type": "Slime", "pos": [5800, SCREEN_HEIGHT - 120]},
    {"type": "Slime", "pos": [6300, SCREEN_HEIGHT - 120]},
  ],
  "gems": [
    {"type": "sapphire", "pos": [7500, SCREEN_HEIGHT - 250]},
  ]
}

# Add a strip of alternating ground tiles:
row = generate_tile_row(
  start_x=2300,
  y=670,
  tile_indices=[2, 1],   # pattern
  tile_width=40,
  count=15               # tiles
)
oak_forest_data["tiles"].extend(row)
row2 = generate_tile_row(
  start_x=4000,
  y=670,
  tile_indices=[2, 1],
  tile_width=40,
  count=60
)
oak_forest_data["tiles"].extend(row2)