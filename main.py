import pygame
import math
from constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE
from board import Board
from ui import draw_board
from ai import minimax # Import our new AI function

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
    
    current_turn = BLACK # AI goes first

    while run:
        clock.tick(60) 
        
        valid_moves = game_board.get_valid_moves(current_turn)
        
        if not valid_moves:
            current_turn = WHITE if current_turn == BLACK else BLACK
            valid_moves = game_board.get_valid_moves(current_turn)

        # --- AI TURN (BLACK) ---
        if current_turn == BLACK and valid_moves:
            # depth=3 is a good balance of speed and smarts. Higher depth = smarter but slower.
            # alpha is negative infinity, beta is positive infinity initially
            score, move = minimax(game_board, 3, -math.inf, math.inf, True, BLACK)
            
            if move:
                # The AI chose a move, execute it!
                pygame.time.delay(500) # Add a small delay so the AI doesn't move instantly (looks better)
                pieces_to_flip = valid_moves[move]
                game_board.place_piece(move[0], move[1], BLACK, pieces_to_flip)
                current_turn = WHITE

        # --- HUMAN TURN (WHITE) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and current_turn == WHITE:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                if (row, col) in valid_moves:
                    pieces_to_flip = valid_moves[(row, col)]
                    game_board.place_piece(row, col, WHITE, pieces_to_flip)
                    current_turn = BLACK

        draw_board(WIN, game_board)

    pygame.quit()

if __name__ == "__main__":
    main()