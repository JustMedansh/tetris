from ttygrid import Grid, Cell
from blocks import Block, Pixel
import time
import sys
from termcolor import colored
from blessed import Terminal

global_symbol = '█'
score = 0

def main():
    term = Terminal()
    board = Grid(rows=20, cols=10, mode="custom")
    pixels: list[Pixel] = [] 

    with term.cbreak(), term.hidden_cursor():
        for i in range(50):
            # BEFORE FALLING BLOCK START
            falling_block = Block(board)
            m = 0
            if not falling_block.can_spawn(board):
                sys.exit(f"Game over!\nScore: {score}")

            print("PASSED SPAWN:", falling_block.get_block_position())
            # BEFORE FALLING BLOCK END
            while True:
                # FALLING BLOCK START
                m += 1
                key = term.inkey(timeout=0.02)
                if key in ['a', 'd']:
                    falling_block.move(key, 1, board)

                if key == 's':
                    if not falling_block.fall(board):
                        break

                if key == 'q':
                    falling_block.rotate()

                time.sleep(0.02)
                if m % 3 == 0:
                    if not falling_block.fall(board):
                        break

                board.clear_term()
                print_and_render(board, pixels, falling_block)
                # FALLING BLOCK END
            # AFTER FALLING BLOCK START

            pixels.extend(decompose(falling_block))
            check_line_clear(board, pixels)
            # AFTER FALLING BLOCK END
            
        pixels.extend(decompose(falling_block))
        print_and_render(board, pixels)


def check_line_clear(board: Grid, pixels: list[Pixel]):
    global score
    for i in range(20):
            matching_pixels = [pixel for pixel in pixels if pixel.y == i]
            if len(matching_pixels) == board.cols:
                score += 1
                for pixel in pixels.copy():
                    if pixel.line_clear(i):
                        pixels.remove(pixel)

    return board, pixels


def automated_line_clear(board, pixels):
    for _ in range(19, 0, -1):
        for pixel in pixels.copy():
            if pixel.line_clear(19):
                pixels.remove(pixel)
        time.sleep(0.2)
        print_and_render(board, pixels)

def decompose(block: Block) -> list[Pixel]:
    pixels = []
    for px, py in block.get_block_position():
        pixels.append(Pixel(block.color, px, py))

    return pixels

def print_and_render(board: Grid, blocks, falling=None):
    render_blocks(board, blocks)
    if falling is not None:
        render_one_block(board, falling)

    print('─'*board.cols, end="")
    # print(board.render(block_renderer))
    print(board.render())
    print('─'*board.cols, end="")

    print()

def block_renderer(cell: Cell):
    if cell.symb == '█':
        color = cell.get_metadata('color')
        return colored('██', color)

    else:
        return ''

def render_blocks(grid: Grid, pixels: list[Pixel]) -> Grid:
    grid.redraw_frame(grid.gen_cell_map(grid.rows, grid.cols, ' '))

    for pixel in pixels:
        grid.draw_cells(Cell(pixel.x, pixel.y, global_symbol, {'color': pixel.color, 'filled': True}))

    return grid

def render_one_block(grid: Grid, block: Block) -> Grid:
    for pixel_x, pixel_y in block.get_block_position():
        grid.draw_cells(Cell(pixel_x, pixel_y, global_symbol, {'color': block.color}))

    return grid

if __name__ == "__main__":
    main()