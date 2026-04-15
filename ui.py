import pygame
from constants import WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, LINE_COLOR, BLACK_PIECE, WHITE_PIECE, BACKGROUND_GREEN, BLACK

def draw_grid(win):
    # Draw horizontal and vertical lines
    for row in range(ROWS):
        pygame.draw.line(win, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 2)
    for col in range(COLS):
        pygame.draw.line(win, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), 2)

def draw_pieces(win, board):
    # Loop through the 2D array and draw a circle if a piece exists
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.grid[row][col]
            if piece != 0:
                color = BLACK_PIECE if piece == BLACK else WHITE_PIECE
                
                # Calculate the exact center pixel of the square
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                radius = SQUARE_SIZE // 2 - 10  # -10 leaves a nice margin so pieces don't touch the lines
                
                pygame.draw.circle(win, color, (center_x, center_y), radius)

def draw_board(win, board):
    # Master function to draw the whole screen
    win.fill(BACKGROUND_GREEN)
    draw_grid(win)
    draw_pieces(win, board)
    pygame.display.update()