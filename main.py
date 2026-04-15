import pygame
from constants import WIDTH, HEIGHT
from board import Board
from ui import draw_board

# Initialize Pygame
pygame.init()

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello AI - Minimax with Alpha-Beta Pruning")

def main():
    run = True
    clock = pygame.time.Clock()
    
    # Initialize the board state
    game_board = Board()

    while run:
        clock.tick(60) 
        
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw the board and pieces
        draw_board(WIN, game_board)

    pygame.quit()

if __name__ == "__main__":
    main()