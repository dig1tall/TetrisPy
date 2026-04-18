from game.config import ALL_SHAPES


class Piece:
    def __init__(self, shape_type):
        self.type = shape_type
        self.cells = [[p[0], p[1]] for p in ALL_SHAPES[shape_type]]
        self.symbol = str(shape_type)

    def move(self, dr, dc):
        for cell in self.cells:
            cell[0] += dr
            cell[1] += dc

    def get_rotated_cells(self, cw) -> list[list[int]]:
        if self.type == 0:
            return self.cells
        center = self.cells[1]
        new_cells = []
        for c in self.cells:
            dr, dc = c[0] - center[0], c[1] - center[1]
            nr, nc = (
                (center[0] + dc, center[1] - dr)
                if cw
                else (center[0] - dc, center[1] + dr)
            )
            new_cells.append([nr, nc])
        return new_cells
