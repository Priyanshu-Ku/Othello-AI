import pygame
pygame.font.init()
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
    
def draw_game_over(win, black_score, white_score):
    font = pygame.font.SysFont("arial", 40, bold=True)
    
    if black_score > white_score:
        message = f"AI Wins! Black: {black_score} | White: {white_score}"
    elif white_score > black_score:
        message = f"You Win! Black: {black_score} | White: {white_score}"
    else:
        message = f"Tie Game! Score: {black_score}"

    # Render the text
    text = font.render(message, True, (255, 0, 0)) # Red text
    
    # Create a semi-transparent background box for readability
    bg_rect = pygame.Rect(WIDTH//2 - text.get_width()//2 - 10, HEIGHT//2 - text.get_height()//2 - 10, text.get_width() + 20, text.get_height() + 20)
    pygame.draw.rect(win, (0, 0, 0), bg_rect)
    
    # Draw the text
    win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()