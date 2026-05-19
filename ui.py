import pygame
from constants import (WIDTH, HEIGHT, BOARD_HEIGHT, PANEL_HEIGHT, ROWS, COLS,
                       SQUARE_SIZE, LINE_COLOR, BLACK_PIECE, WHITE_PIECE,
                       BACKGROUND_GREEN, BLACK, PANEL_COLOR, TEXT_COLOR,
                       BUTTON_COLOR, HIGHLIGHT)

pygame.font.init()

def draw_grid(win):
    # Draw horizontal and vertical board borders cleanly up to the board region
    for row in range(ROWS + 1): 
        pygame.draw.line(win, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 2)
    for col in range(COLS + 1):
        pygame.draw.line(win, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, BOARD_HEIGHT), 2)

def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.grid[row][col]
            if piece != 0:
                color = BLACK_PIECE if piece == BLACK else WHITE_PIECE
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                radius = SQUARE_SIZE // 2 - 10
                pygame.draw.circle(win, color, (center_x, center_y), radius)

def draw_panel(win, board, current_turn, game_started):
    # Draw dark panel background canvas
    pygame.draw.rect(win, PANEL_COLOR, (0, BOARD_HEIGHT, WIDTH, PANEL_HEIGHT))
    font = pygame.font.SysFont("arial", 22, bold=True)

    if not game_started:
        # Option 1: Render the "Start Game" Button overlay centered on the panel
        button_rect = pygame.Rect(WIDTH // 2 - 80, BOARD_HEIGHT + 25, 160, 50)
        pygame.draw.rect(win, BUTTON_COLOR, button_rect, border_radius=8)
        text = font.render("START GAME", True, WHITE_PIECE)
        win.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))
    else:
        # Option 2: Live player piece counts
        black_score, white_score = board.get_score()
        black_text = font.render(f"AI (Black): {black_score}", True, TEXT_COLOR)
        white_text = font.render(f"You (White): {white_score}", True, TEXT_COLOR)
        win.blit(black_text, (40, BOARD_HEIGHT + 35))
        win.blit(white_text, (WIDTH - white_text.get_width() - 40, BOARD_HEIGHT + 35))

        # Option 3: Dynamic next turn indicator text
        turn_str = "Turn: AI (Black)" if current_turn == BLACK else "Turn: You (White)"
        turn_color = HIGHLIGHT if current_turn == BLACK else WHITE_PIECE
        turn_text = font.render(turn_str, True, turn_color)
        win.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, BOARD_HEIGHT + 35))

def draw_board(win, board, current_turn, game_started):
    win.fill(BACKGROUND_GREEN)
    draw_grid(win)
    draw_pieces(win, board)
    draw_panel(win, board, current_turn, game_started)
    pygame.display.update()

def draw_game_over(win, black_score, white_score):
    font = pygame.font.SysFont("arial", 40, bold=True)
    if black_score > white_score:
        message = f"AI Wins! Black: {black_score} | White: {white_score}"
    elif white_score > black_score:
        message = f"You Win! Black: {black_score} | White: {white_score}"
    else:
        message = f"Tie Game! Score: {black_score}"

    text = font.render(message, True, (255, 0, 0))
    bg_rect = pygame.Rect(WIDTH//2 - text.get_width()//2 - 10, BOARD_HEIGHT//2 - text.get_height()//2 - 10, text.get_width() + 20, text.get_height() + 20)
    pygame.draw.rect(win, (0, 0, 0), bg_rect)
    win.blit(text, (WIDTH//2 - text.get_width()//2, BOARD_HEIGHT//2 - text.get_height()//2))
    pygame.display.update()