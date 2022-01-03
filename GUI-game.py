import pygame
from grid import Grid
import tkinter as tk

# FPS setting
FPS = 60
clock = pygame.time.Clock()

# Color objects
COLORS = [(255, 255, 255), (238, 195, 115)]

# Set up caption
pygame.display.set_caption("Knight's Tour Puzzle")


# ------------------------------------ Tkinter window---------------------------------------#
## take user input
def show_entry_fields():
    global ROWS, COLS
    ROWS = int(e1.get().strip())
    COLS = int(e2.get().strip())
    window.quit()
    window.destroy()


TITLE_FONT = ("Arial", 20)
LABEL_FONT = ("Arial", 16)

window = tk.Tk()
window.title("Knight's Tour Puzzle")
tk.Label(window,
         text="Enter your board dimensions:", font=TITLE_FONT).grid(row=0, columnspan=2, pady=10, sticky="W")
tk.Label(window,
         text="Number of rows:", font=LABEL_FONT).grid(row=1, sticky="W")
tk.Label(window,
         text="Number of columns:", font=LABEL_FONT).grid(row=2, sticky="W")

e1 = tk.Entry(window)
e2 = tk.Entry(window)

e1.grid(row=1, column=1)
e2.grid(row=2, column=1)

tk.Button(window,
          text='Submit', font=LABEL_FONT, command=show_entry_fields).grid(row=3,
                                                         column=1,
                                                         sticky=tk.W,
                                                         pady=10)

tk.mainloop()

# ------------------------------------ Pygame window---------------------------------------#
SMALL_CELL = 80
BIG_CELL = 100


def define_cell(X, Y):
    max_count = max(X, Y)
    if max_count >= 8:
        return SMALL_CELL
    else:
        return BIG_CELL


# cell size
CELL_SIZE = define_cell(ROWS, COLS)

grid = Grid(ROWS, COLS)


WIN_WIDTH = ROWS * CELL_SIZE
WIN_HEIGHT = COLS * CELL_SIZE


def main():
    pygame.init()
    surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    chess = pygame.image.load("Assets/chess-pawn.png")
    cross = pygame.image.load("Assets/cross.png")

    def draw_board(game_grid):
        # draw the cells
        for row in range(game_grid.Y):
            color_index = row % 2
            for col in range(game_grid.X):
                cell = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                surface.fill(COLORS[color_index], cell)
                color_index = (color_index + 1) % 2

    def mark(x, y, item):
        width_offset = (CELL_SIZE - item.get_width()) // 2
        height_offset = (CELL_SIZE - item.get_height()) // 2
        surface.blit(item, ((x - 1) * CELL_SIZE + width_offset, (grid.Y - y) * CELL_SIZE + height_offset))

    def mark_visited():
        if len(grid.visited) > 1:
            for x, y in grid.visited[:-1]:
                mark(x, y, cross)

    def mark_current_move():
        if grid.visited:
            x, y = grid.visited[-1]
            mark(x, y, chess)

    def mark_possible_move():
        if grid.possible_moves:
            for count, x, y in grid.count_possible_moves:
                font = pygame.font.SysFont('arial', 54)
                text = font.render(str(count), True, (0, 0, 0))
                mark(x, y, text)

    def transform(x, y):
        board_col = x // CELL_SIZE + 1
        board_row = grid.Y - (y // CELL_SIZE)
        return board_col, board_row

    def show_message(content):
        font = pygame.font.SysFont('arial', 24)
        text = font.render(content, True, (255, 0, 0))

        temp_surface = pygame.Surface(text.get_size())
        temp_surface.fill((220, 220, 220))
        temp_surface.blit(text, (0, 0))

        width_offset = text.get_width() // 2
        height_offset = text.get_height() // 2
        surface.blit(temp_surface, (WIN_WIDTH / 2 - width_offset, WIN_HEIGHT / 2 - height_offset))

    run = True
    while run:
        # run the while loop 60 times per second
        clock.tick(FPS)

        # show current board
        draw_board(grid)
        mark_visited()
        mark_current_move()
        mark_possible_move()
        # win message
        if len(grid.visited) == grid.size:
            show_message("Congratulations! You win!")

        # lose message
        if grid.visited != [] and grid.possible_moves == []:
            show_message(f"Game over. {len(grid.visited)} squares visited")

        for event in pygame.event.get():
            # quit if user close the window
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    grid.undo()

            if event.type == pygame.MOUSEBUTTONUP:
                x_corr, y_corr = pygame.mouse.get_pos()
                col, row = transform(x_corr, y_corr)
                grid.update(col, row)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
