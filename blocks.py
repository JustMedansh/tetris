import random
from ttygrid import Grid, Cell

class Block:
    BLOCK_SHAPES = {
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "J": [(0, 0), (0, 1), (1, 1), (2, 1)],
        "L": [(2, 0), (0, 1), (1, 1), (2, 1)],
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
        "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
        "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
    }

    COLORS = {
        "I": "cyan",
        "O": "yellow",
        "T": "magenta",
        "S": "green",
        "Z": "red",
        "J": "blue",
        "L": "white"
    }

    def __init__(self) -> None:
        """Initialize a block"""
        self.block_name = random.choice(['I', 'J', 'L', 'O', 'S', 'T', 'Z'])
        self.block_shape = self.BLOCK_SHAPES[self.block_name]
        self.color = self.COLORS[self.block_name]
        self.dx = 0
        self.dy = 0
        self.symbol = '1'

    def will_collide(self, grid: Grid) -> bool:
        """Return True if block will collide when moved down"""
        position = self.get_block_position()
        for pixel_x, pixel_y in position:
            try:
                filled = grid.get_cell(pixel_x, pixel_y + 1).get_metadata('filled')
                # filed can be None, or True
                if filled:
                    raise ValueError
            except ValueError:
                return True
            
        return False

    def get_block_position(self) -> list[tuple[int, int]]:
        """Return current position of block as list"""
        moved_block = []
        for x, y in self.block_shape:
            moved_block.append((x + self.dx, y + self.dy))

        return moved_block

    def fall(self, grid: Grid) -> bool:
        """If the block can't fall, return False. Otherwise return True and move the object down."""
        if self.will_collide(grid):
            return False

        self.dy += 1
        return True
