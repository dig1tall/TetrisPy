# 🎮 TetrisPy

A modern implementation of the classic **Tetris** game written in **Python** using **Pygame**.

This project was originally developed as a **coursework in C**, and later fully rewritten in Python as a **pet project**
with a focus on **object-oriented programming, clean architecture, and modular design**.

---

## Features

* Classic Tetris gameplay
* Smooth controls and animations
* Ghost piece (landing preview)
* Hold piece system
* Sound effects & background music
* 7-bag randomizer (fair piece generation)
* Local leaderboard system:

    * Personal best for each player
    * Local champion (stored in binary file)
* Clean OOP architecture

---

## Tech Stack

* Python 3.x
* Pygame

---

## Installation

```bash
git clone https://github.com/dig1tall/TetrisPy.git
cd TetrisPy
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Controls

| Key       | Action          |
|-----------|-----------------|
| A / D     | Move left/right |
| Q / E     | Rotate          |
| S / ↓     | Soft drop       |
| Space / Z | Hard drop       |
| C         | Hold piece      |
| ESC       | Exit game       |

---

## Project Structure

```
Tetris_Realse/
│── main.py
│── README.md
│── requirements.txt
│── .gitignore
│
├── game/
│   │── __init__.py
│   │── engine.py
│   │── board.py
│   │── piece.py
│   │── renderer.py
│   │── score_manager.py
│   │── config.py
│
├── assets/
│   └── sounds/
│
├── scores/
│   ├── champion.dat
│   └── scores.csv
│
├── screenshots/
│   ├── game_over.png
│   ├── gameplay.png
│   └── menu.png
```

---

## Data Storage

* `scores/scores.csv` — stores player scores
* `scores/champion.dat` — stores global best player (binary format)

---

## Architecture

The project follows a modular OOP design:

* `engine.py` — main game loop and logic
* `board.py` — grid and collision system
* `piece.py` — tetromino behavior
* `renderer.py` — rendering and UI
* `score_manager.py` — local data storage system
* `config.py` — global constants
* `config.py` — shared helper functions and color mapping

---

## Screenshots

![Gameplay](screenshots/menu.png)

![Gameplay](screenshots/gameplay.png)

![Gameplay](screenshots/game_over.png)

---

## Future Improvements

* Online leaderboard
* ️Settings menu (volume, controls)
* Difficulty levels
* More visual effects and animations
* Mobile version

---

## License

MIT License

---

## Author

Dovgash Matvey
