from ttygrid import Grid, Cell
from blocks import Block
import time


def main():
    board = Grid(rows=20, cols=10, mode="custom")
    blocks = []

    for _ in range(11):
        falling_block = Block()
        while True:
            time.sleep(0.02)
            if not falling_block.fall(board):
                break

            board.clear_term()
            print_and_render(board, blocks, falling_block)
        blocks.append(falling_block)
    print_and_render(board, blocks, falling_block)


def print_and_render(board, blocks, falling):
    render_blocks(board, blocks)
    render_one_block(board, falling)

    print('─'*board.cols, end="")
    print(board)
    print('─'*board.cols, end="")

    print()

def render_blocks(grid: Grid, blocks: list[Block]) -> Grid:
    grid.redraw_frame(grid.gen_cell_map(grid.rows, grid.cols, ' '))

    for block in blocks:
        for pixel_x, pixel_y in block.get_block_position():
            grid.draw_cells(Cell(pixel_x, pixel_y, '█', {'color': block.color, 'filled': True}))

    return grid

def render_one_block(grid: Grid, block: Block) -> Grid:
    for pixel_x, pixel_y in block.get_block_position():
        grid.draw_cells(Cell(pixel_x, pixel_y, '█', {'color': block.color}))

    return grid

if __name__ == "__main__":
    main()