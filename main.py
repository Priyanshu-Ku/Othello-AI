import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE
from board import Board
from ui import draw_board

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
    
    current_turn = BLACK # Black goes first

    while run:
        clock.tick(60) 
        
        # Get all valid moves for the current player
        valid_moves = game_board.get_valid_moves(current_turn)
        
        # If the player has no valid moves, their turn is skipped
        if not valid_moves:
            current_turn = WHITE if current_turn == BLACK else BLACK
            valid_moves = game_board.get_valid_moves(current_turn)
            # If NEITHER player has valid moves, the game is over (we'll handle this later)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                # Check if the clicked square is a valid move
                if (row, col) in valid_moves:
                    pieces_to_flip = valid_moves[(row, col)]
                    game_board.place_piece(row, col, current_turn, pieces_to_flip)
                    
                    # Switch turns
                    current_turn = WHITE if current_turn == BLACK else BLACK

        draw_board(WIN, game_board)

    pygame.quit()

if __name__ == "__main__":
    main()