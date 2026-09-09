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
        'M': [*[(x, 0) for x in range(2)], *[(x, 1) for x in range(2)]],
    }

    COLORS = {
        "I": "cyan",
        "O": "yellow",
        "T": "magenta",
        "S": "green",
        "Z": "red",
        "J": "blue",
        "L": "white",
    }

    @staticmethod
    def get_pivot(key):
        if key == 'I':
            return (1.5, 1.5)

        elif key == 'O':
            return None

        else:
            return (1, 1)

    def __init__(self, board: Grid) -> None:
        """Initialize a block"""
        self.block_name = random.choice(['I', 'J', 'L', 'O', 'S', 'T', 'Z'])
        self.block_shape = self.BLOCK_SHAPES[self.block_name]
        self.color = self.COLORS[self.block_name]
        self.dx = random.randint(0, 6)
        self.dy = 0
        self.symbol = '1'
        self.pivot = self.get_pivot(self.block_name)
        self.board = board

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

    def can_move(self, dx, grid: Grid):
        for x, y in self.get_block_position():
            new_x = x + dx

            if new_x < 0 or new_x >= 10 or grid.get_cell(new_x, y).get_metadata('filled') is True:
                return False

        return True

    def move(self, dir, value, grid):
        dx = -value if dir == 'a' else value

        if self.can_move(dx, grid):
            self.dx += dx

    def can_spawn(self, grid: Grid):
        matching_pixels = [pixel for pixel in grid.get_all_cells(include_empty=False) if pixel.get_metadata('filled') is True and pixel.y == 0]
        if len(matching_pixels) > 0:
            return False
        pixels = self.get_block_position()
        for x, y in pixels:
            if x < 0 or x >= grid.cols:
                return False

            if y < 0 or y >= grid.rows:
                return False
            
            if grid.get_cell(x, y).get_metadata('filled') is True:
                return False

        return True

    def rotate(self):
        if not self.pivot:
            return self
        
        pivotX, pivotY = self.pivot
        
        rotated = []
        for pixelX, pixelY in self.block_shape:
            new_x = pivotX - (pixelY - pivotY)
            new_y = pivotY + (pixelX - pivotX)
            rotated.append((new_x, new_y))


        block = self.fix_rotate_collision(rotated)
        if block is not None:
            self.block_shape = block
        return self

    def get_position_local(self, shape):
        moved_block = []
        for x, y in shape:
            moved_block.append((x + self.dx, y + self.dy))

        return moved_block
    
    def fix_rotate_collision(self, rotated):
        KICKS = [
            (0, 0),
            (-1, 0),
            (1, 0),
            (-2, 0),
            (2, 0),
            (0, -1),
            (0, 1),
        ]

        for kick in KICKS:
            onboard = self.get_position_local(rotated)
            block = self.apply_kick(onboard, kick)
            if not self.is_colliding(block):
                return self.apply_kick(rotated, kick)

    def is_colliding(self, block):
        board = self.board
        for pixelx, pixely in block:
            try:
                cell = board.get_cell(pixelx, pixely)
                if cell.get_metadata('filled') is True:
                    return True
            except ValueError:
                return True

        return False

    def apply_kick(self, block, kick):
        applied = []
        kickX, kickY = kick
        for x, y in block:
            applied.append((x + kickX, y + kickY))

        return applied
            

class Pixel:
    def __init__(self, color, x, y) -> None:
            """Initialize a pixel"""
            self.color = color
            self.x = x
            self.y = y

    def line_clear(self, line_number):
        """Return true if block is deleted"""
        if line_number == self.y:
            return True

        if line_number > self.y:
            self.y += 1

        return False
