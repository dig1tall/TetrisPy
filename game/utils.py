from typing import Tuple


def get_shape_color(shape_type) -> Tuple[int, int, int]:
    """Return the RGB color for a given tetromino shape type."""
    colors = {
        0: (255, 203, 0),
        1: (102, 191, 255),
        2: (230, 41, 55),
        3: (0, 228, 48),
        4: (255, 161, 0),
        5: (0, 121, 241),
        6: (200, 122, 255),
    }
    return colors.get(shape_type, (130, 130, 130))
