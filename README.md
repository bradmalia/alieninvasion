# Alien Invasion

A Python-based arcade-style game where players control a ship to defend Earth from an incoming fleet of aliens. This project is inspired by the classic Space Invaders and developed using the `pygame` library.

<img width="1196" height="835" alt="image" src="https://github.com/user-attachments/assets/89895d3b-e6d7-49e7-93e5-8563177ba417" />

## Features
- Dynamic ship movement and shooting.
- Multiple alien fleet levels with increasing speed.
- Interactive sound effects and background music.
- Randomized alien taunts and visual elements like stars and planets.
- Game statistics tracking.

## Prerequisites
- Python 3.x
- `pygame` library

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bradmalia/alien_invasion.git
   ```
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## How to Play
Run the game using Python:
```bash
python3 alien_invasion.py
```
- **Arrow Keys:** Move the ship left and right.
- **Spacebar / Up Arrow:** Fire bullets.
- **Q:** Quit the game.

## Project Structure
- `alien_invasion.py`: The main game loop and manager.
- `settings.py`: Configuration for game parameters.
- `ship.py`, `alien.py`, `bullet.py`, `star.py`: Classes for game entities.
- `game_stats.py`: Logic for tracking player statistics.
- `images/`: Game graphical assets.
- `sounds/`: Game audio assets.
![Uploading image.png…]()
