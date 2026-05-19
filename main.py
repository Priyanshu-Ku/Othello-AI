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
        
        draw_board(WIN, game_board, current_turn, game_started)

        if game_started:
            # ==============================================================
            # NEW: EARLY TERMINATION DETECTOR (No Fruitful Comeback Possible)
            # ==============================================================
            black_score, white_score = game_board.get_score()
            empty_squares = game_board.get_empty_count()

            # If AI is winning, check if White can mathematically catch up
            if black_score > white_score and (white_score + empty_squares) < black_score:
                draw_board(WIN, game_board, current_turn, game_started)
                draw_game_over(WIN, black_score, white_score)
                pygame.time.delay(5000)
                run = False
                continue

            # If White is winning, check if AI can mathematically catch up
            if white_score > black_score and (black_score + empty_squares) < white_score:
                draw_board(WIN, game_board, current_turn, game_started)
                draw_game_over(WIN, black_score, white_score)
                pygame.time.delay(5000)
                run = False
                continue
            # ==============================================================

            valid_moves = game_board.get_valid_moves(current_turn)
            
            # Standard Othello block for handling skipped turns or filled boards
            if not valid_moves:
                next_turn = WHITE if current_turn == BLACK else BLACK
                next_valid_moves = game_board.get_valid_moves(next_turn)
                
                if not next_valid_moves:
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
                # ==============================================================
                # PHASE 1: THE THINK PHASE (Visual Warning Before Calculation)
                # ==============================================================
                # Redraw the current board state
                draw_board(WIN, game_board, current_turn, game_started)
                
                # Render the "AI is thinking..." overlay text
                font = pygame.font.SysFont("arial", 22, bold=True)
                thinking_text = font.render("AI is thinking...", True, (255, 69, 0)) # Orange-Red
                pygame.draw.rect(WIN, (40, 40, 40), (WIDTH // 2 - 100, BOARD_HEIGHT + 25, 200, 50))
                WIN.blit(thinking_text, (WIDTH // 2 - thinking_text.get_width() // 2, BOARD_HEIGHT + 35))
                pygame.display.update()
                
                # Pause for 600ms BEFORE computing so the user actually reads the text
                pygame.time.delay(600) 

                # ==============================================================
                # PHASE 2: THE ACTION PHASE (Compute, Move, and Highlight)
                # ==============================================================
                # Now run the Minimax search tree evaluation
                score, move = minimax(game_board, 3, -math.inf, math.inf, True, BLACK)
                
                if move:
                    pieces_to_flip = valid_moves[move]
                    # Execute the piece placement and flip logic
                    game_board.place_piece(move[0], move[1], BLACK, pieces_to_flip)
                    
                    # Redraw the updated board state with the gold highlight ring
                    draw_board(WIN, game_board, current_turn, game_started, highlight_pos=move)
                    
                    # Re-render the text to maintain visual consistency on the panel
                    pygame.draw.rect(WIN, (40, 40, 40), (WIDTH // 2 - 100, BOARD_HEIGHT + 25, 200, 50))
                    WIN.blit(thinking_text, (WIDTH // 2 - thinking_text.get_width() // 2, BOARD_HEIGHT + 35))
                    pygame.display.update()
                    
                    # Pause for 1200ms AFTER the move so the gold ring highlight can be analyzed
                    pygame.time.delay(1200) 
                    
                    # Shift turn context back to the player
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