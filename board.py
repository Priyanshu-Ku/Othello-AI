from constants import ROWS, COLS, EMPTY, BLACK, WHITE

class Board:
    def __init__(self):
        self.grid = self.create_starting_grid()

    def create_starting_grid(self):
        # Create an 8x8 grid filled with 0s (EMPTY)
        grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        
        # Standard Othello starting position in the center
        grid[3][3] = WHITE
        grid[3][4] = BLACK
        grid[4][3] = BLACK
        grid[4][4] = WHITE
        
        return grid