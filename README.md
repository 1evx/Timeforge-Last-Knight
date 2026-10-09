# Timeforge: The Last Knight

**Timeforge: The Last Knight** is a 2D side-scrolling action platformer built with Python and Pygame. Fight through four environments, collect gold and hidden gems, upgrade your knight, and defeat the creatures standing between you and the Dark Castle.

## Features

- Four playable stages: Oak Forest, Haze Forest, Crystal Cave, and Dark Castle
- Animated combat with basic, combo, dash, and aerial attacks
- A guided tutorial covering movement and combat
- Multiple enemy types, including slimes, skeletons, goblins, demons, and a necromancer
- Coins and gems to collect across the campaign
- Shops offering health, speed, maximum-health, and sword upgrades
- Parallax backgrounds, animated sprites, sound effects, and music
- Player health, gold, gems, and upgrades carried between levels

## Requirements

- Python 3.10 or newer
- Pygame 2.0 or newer

## Getting Started

Clone the repository and move into the project directory:

```bash
git clone https://github.com/1evx/Timeforge-Last-Knight.git
cd Timeforge-Last-Knight
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependency and start the game from the repository root:

```bash
python -m pip install -r requirements.txt
python main.py
```

> The game loads assets using paths relative to the repository root, so run `main.py` from that directory.

## Controls

| Action | Input |
| --- | --- |
| Move | `A` / `D` |
| Jump | `W` or `Space` |
| Crouch | `S` |
| Slide | `S` + `A` / `D` |
| Basic attack | Left mouse button |
| Combo attack | Left mouse button twice quickly |
| Dash attack | Right mouse button |
| Aerial attack | Jump, then right mouse button |
| Open or close a shop | `E` |
| Navigate menus and shops | Arrow keys |
| Confirm a selection | `Enter` |
| Close a shop / leave the main menu | `Esc` |

Menu and shop options can also be selected with the mouse.

## How to Play

Travel to the right through each stage while defeating enemies and avoiding damage. Fallen enemies can reward gold, which can be spent at shops on restorative items and permanent upgrades. Each level also contains a gem; collect all four gems and complete every stage to earn the full completion ending.

The Oak Forest introduces the controls through an in-game tutorial. Complete each tutorial prompt before reaching the end of the stage.

## Project Structure

```text
.
├── main.py             # Game entry point and level progression
├── requirements.txt    # Python dependency list
├── assets/             # Sprites, backgrounds, tiles, audio, and decorations
├── levels/             # Data and layouts for the four stages
└── scripts/            # Player, enemies, UI, combat, camera, shop, and utilities
```
