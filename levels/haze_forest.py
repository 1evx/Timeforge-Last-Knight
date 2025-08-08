from scripts.Settings import SCREEN_HEIGHT

haze_forest_data = {
  "level_width": 8000,
  "tiles_per_row": 100,
  "tileset": "assets/tiles/oak_woods_tileset.png",
  "background_music": "assets/audio/music/dark-wood.mp3",
  "backgrounds": [
    ("assets/backgrounds/hf_layer_1.png", 0.1),
    ("assets/backgrounds/hf_layer_2.png", 0.3),
    ("assets/backgrounds/hf_layer_3.png", 0.5),
    ("assets/backgrounds/hf_layer_4.png", 0.7),
    ("assets/backgrounds/hf_layer_5.png", 0.9),
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
    {"type": "Rock_1", "pos": [2500, SCREEN_HEIGHT - 70]}, 
    {"type": "Rock_2", "pos": [2800, SCREEN_HEIGHT - 70]}, 
    {"type": "FallenSkeleton2", "pos": [2900, SCREEN_HEIGHT - 175]}, 
    {"type": "Wall", "pos": [3000, SCREEN_HEIGHT - 160]},
    {"type": "Fireplace", "pos": [3300, SCREEN_HEIGHT - 80]},
    {"type": "Shop", "pos": [6500, SCREEN_HEIGHT - 405]},
  ],
  "tiles": [
  ],
  "enemies": [
    {"type": "Mushroom", "pos": [900, SCREEN_HEIGHT - 250]},
    {"type": "ShieldSkeleton", "pos": [1000, SCREEN_HEIGHT - 250]},
    
    {"type": "Necromancer", "pos": [1800, SCREEN_HEIGHT - 272]},

    {"type": "Goblin", "pos": [2700, SCREEN_HEIGHT - 250]},
    {"type": "Goblin", "pos": [2800, SCREEN_HEIGHT - 250]},

    {"type": "ShieldSkeleton", "pos": [4500, SCREEN_HEIGHT - 250]},
    {"type": "Mushroom", "pos": [4700, SCREEN_HEIGHT - 250]},
    {"type": "Necromancer", "pos": [5000, SCREEN_HEIGHT - 272]},
    {"type": "Necromancer", "pos": [5600, SCREEN_HEIGHT - 272]},

    # {"type": "Skeleton", "pos": [600, SCREEN_HEIGHT - 185]},
    # {"type": "Skeleton", "pos": [750, SCREEN_HEIGHT - 185]},

    # {"type": "Skeleton", "pos": [1150, SCREEN_HEIGHT - 185]},
    # {"type": "Necromancer", "pos": [1300, SCREEN_HEIGHT - 272]},
    # {"type": "Skeleton", "pos": [1350, SCREEN_HEIGHT - 185]},
    # {"type": "Skeleton", "pos": [1450, SCREEN_HEIGHT - 185]},

    # {"type": "Necromancer", "pos": [1700, SCREEN_HEIGHT - 272]},
    # {"type": "Skeleton", "pos": [1850, SCREEN_HEIGHT - 185]},

    # {"type": "Necromancer", "pos": [2400, SCREEN_HEIGHT - 272]},
    # {"type": "Necromancer", "pos": [2600, SCREEN_HEIGHT - 272]},
    # {"type": "Skeleton", "pos": [2750, SCREEN_HEIGHT - 185]},
    # {"type": "Skeleton", "pos": [3200, SCREEN_HEIGHT - 185]},

    # {"type": "Skeleton", "pos": [4200, SCREEN_HEIGHT - 185]},
    # {"type": "Necromancer", "pos": [4500, SCREEN_HEIGHT - 272]},
    # {"type": "Necromancer", "pos": [4600, SCREEN_HEIGHT - 272]},
  ],
  "gems": [
    {"type": "emerald", "pos": [7500, SCREEN_HEIGHT - 250]},  # Green gem
  ]
}