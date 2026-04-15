import pygame
from constants import WIDTH, HEIGHT, BACKGROUND_GREEN

# Initialize Pygame
pygame.init()

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello AI - Minimax with Alpha-Beta Pruning")

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        # Cap the frame rate at 60 FPS
        clock.tick(60) 
        
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # We will handle mouse clicks here later
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        # Draw the background
        WIN.fill(BACKGROUND_GREEN)
        
        # Update the display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()