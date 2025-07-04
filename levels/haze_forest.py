from scripts.Settings import SCREEN_HEIGHT

haze_forest_data = {
  "level_width": 5000,
  "tiles_per_row": 100,
  "tileset": "assets/tiles/oak_woods_tileset.png",
  "backgrounds": [
    ("assets/backgrounds/background_layer_1.png", 0.2),
    ("assets/backgrounds/background_layer_2.png", 0.5),
    ("assets/backgrounds/background_layer_3.png", 0.8)
  ],
  "decor": [
    {"type": "Shop", "pos": [1000, SCREEN_HEIGHT - 405]}
  ],
  "enemies": [
    # {"type": "Skeleton", "pos": [1900, SCREEN_HEIGHT - 185]},
    {"type": "Slime", "pos": [3000, SCREEN_HEIGHT - 120]},
    # {"type": "Nightborne", "pos": [3900, SCREEN_HEIGHT - 300]},
    # {"type": "Fireborne", "pos": [2000, SCREEN_HEIGHT - 370]},
    # {"type": "SkeletonArcher", "pos": [1900, SCREEN_HEIGHT - 305]},
    # {"type": "Necromancer", "pos": [1000, SCREEN_HEIGHT - 230]}
  ]
}
