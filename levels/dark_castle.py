from scripts.Settings import SCREEN_HEIGHT

dark_castle_data = {
  "level_width": 8000,
  "tiles_per_row": 100,
  "tileset": "assets/tiles/oak_woods_tileset.png",
  "background_music": "assets/audio/music/lost-city.mp3",
  "backgrounds": [
    ("assets/backgrounds/dc_layer_1.png", 0.2),
    ("assets/backgrounds/dc_layer_2.png", 0.5),
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
    {"type": "Rock_2", "pos": [2800, SCREEN_HEIGHT - 70]}, 
    {"type": "FallenSkeleton2", "pos": [2900, SCREEN_HEIGHT - 175]}, 
  ],
  "tiles": [ 
  ],
  "enemies": [
    {"type": "Nightborne", "pos": [900, SCREEN_HEIGHT - 300]},

    {"type": "Nightborne", "pos": [1800, SCREEN_HEIGHT - 300]},
    {"type": "Necromancer", "pos": [1900, SCREEN_HEIGHT - 272]},

    {"type": "Nightborne", "pos": [4600, SCREEN_HEIGHT - 300]},
    {"type": "Nightborne", "pos": [4800, SCREEN_HEIGHT - 300]},
    {"type": "Necromancer", "pos": [5000, SCREEN_HEIGHT - 272]},

    {"type": "Skeleton", "pos": [6000, SCREEN_HEIGHT - 185]},
    {"type": "Skeleton", "pos": [6000, SCREEN_HEIGHT - 185]},

    {"type": "Deathborne", "pos": [6700, SCREEN_HEIGHT - 325]},
    {"type": "Necromancer", "pos": [6800, SCREEN_HEIGHT - 272]},
  ],
  "gems": [
    {"type": "amethyst", "pos": [7500, SCREEN_HEIGHT - 250]},  # Purple gem
  ]
}