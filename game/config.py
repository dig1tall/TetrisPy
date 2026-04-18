# game/config.py

TILE_SIZE = 30  # Size of a single block
GRID_X, GRID_Y = 50, 50  # Screen offset for the game board
ROUNDNESS = 0.25  # Corner radius factor for block drawing

MAP_HEIGHT, MAP_WIDTH = 22, 12  # Internal grid size
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 750  # Pygame window resolution

# Tetromino Shape Definitions
ALL_SHAPES = [
    [(1, 5), (1, 6), (2, 5), (2, 6)],  # O-shape
    [(1, 4), (1, 5), (1, 6), (1, 7)],  # I-shape
    [(2, 5), (2, 6), (1, 6), (1, 7)],  # S-shape
    [(1, 5), (1, 6), (2, 6), (2, 7)],  # Z-shape
    [(2, 5), (2, 6), (2, 7), (1, 5)],  # L-shape
    [(2, 5), (2, 6), (2, 7), (1, 7)],  # J-shape
    [(2, 5), (2, 6), (2, 7), (1, 6)],  # T-shape
]
