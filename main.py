import pygame
import math
from constants import WIDTH, HEIGHT, BOARD_HEIGHT, SQUARE_SIZE, BLACK, WHITE
from board import Board
from ui import draw_board, draw_game_over
from ai import minimax

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello AI - Minimax with Alpha-Beta Pruning")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game_board = Board()
    
    current_turn = BLACK 
    game_started = False  # Set to True when the panel button is pressed

    while run:
        clock.tick(60) 
        
        # Continuously render layout updates passing dashboard states
        draw_board(WIN, game_board, current_turn, game_started)

        if game_started:
            valid_moves = game_board.get_valid_moves(current_turn)
            
            if not valid_moves:
                next_turn = WHITE if current_turn == BLACK else BLACK
                next_valid_moves = game_board.get_valid_moves(next_turn)
                
                if not next_valid_moves:
                    black_score, white_score = game_board.get_score()
                    draw_board(WIN, game_board, current_turn, game_started)
                    draw_game_over(WIN, black_score, white_score)
                    pygame.time.delay(5000)
                    run = False
                    continue
                else:
                    current_turn = next_turn
                    valid_moves = next_valid_moves

            # --- AI TURN (BLACK) ---
            if current_turn == BLACK and valid_moves:
                # 1. Update panel to show the AI is calculating
                draw_board(WIN, game_board, current_turn, game_started)
                
                # If you want to explicitly show a "Thinking..." text, we can let Pygame refresh
                font = pygame.font.SysFont("arial", 22, bold=True)
                thinking_text = font.render("AI is thinking...", True, (255, 69, 0)) # Orange-Red text
                # Overwrite the middle section of the panel briefly
                pygame.draw.rect(WIN, (40, 40, 40), (WIDTH // 2 - 100, BOARD_HEIGHT + 25, 200, 50))
                WIN.blit(thinking_text, (WIDTH // 2 - thinking_text.get_width() // 2, BOARD_HEIGHT + 35))
                pygame.display.update()

                # 2. Run the Minimax search tree evaluation
                score, move = minimax(game_board, 3, -math.inf, math.inf, True, BLACK)
                
                if move:
                    # Increase delay to 1500ms (1.5 seconds) for a natural human-like pace
                    pygame.time.delay(1500) 
                    
                    pieces_to_flip = valid_moves[move]
                    game_board.place_piece(move[0], move[1], BLACK, pieces_to_flip)
                    current_turn = WHITE

        # --- EVENT HANDLING LOOP ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if not game_started:
                    # Check button geometry context: (WIDTH // 2 - 80 <= x <= WIDTH // 2 + 80)
                    # and (BOARD_HEIGHT + 25 <= y <= BOARD_HEIGHT + 75)
                    if (WIDTH // 2 - 80 <= pos[0] <= WIDTH // 2 + 80) and (BOARD_HEIGHT + 25 <= pos[1] <= BOARD_HEIGHT + 75):
                        game_started = True
                else:
                    # Capture moves strictly inside the board quadrant area
                    if pos[1] < BOARD_HEIGHT and current_turn == WHITE:
                        row, col = get_row_col_from_mouse(pos)
                        if (row, col) in valid_moves:
                            pieces_to_flip = valid_moves[(row, col)]
                            game_board.place_piece(row, col, WHITE, pieces_to_flip)
                            current_turn = BLACK

    pygame.quit()

if __name__ == "__main__":
    main()