from game.config import MAP_WIDTH, MAP_HEIGHT


class Board:
    def __init__(self):
        self.grid = [[" " for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self._generate_walls()

    def _generate_walls(self):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if i == 0 or i == MAP_HEIGHT - 1 or j == 0 or j == MAP_WIDTH - 1:
                    self.grid[i][j] = "*"

    def check_collision(self, cells) -> bool:
        for r, c in cells:
            if not (0 <= r < MAP_HEIGHT and 0 <= c < MAP_WIDTH):
                return True
            if self.grid[r][c] != " ":
                return True
        return False

    def lock_piece(self, piece):
        """Fixes the figure in place"""
        for r, c in piece.cells:
            self.grid[r][c] = piece.symbol

    def clear_lines(self) -> int:
        """Remove full rows from the grid and insert new empty rows at the top."""
        lines = 0
        for i in range(1, MAP_HEIGHT - 1):
            if all(self.grid[i][j] != " " for j in range(1, MAP_WIDTH - 1)):
                lines += 1
                del self.grid[i]
                self.grid.insert(1, ["*"] + [" " for _ in range(MAP_WIDTH - 2)] + ["*"])
        return lines
