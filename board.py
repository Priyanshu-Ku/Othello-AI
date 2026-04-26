from constants import ROWS, COLS, EMPTY, BLACK, WHITE

class Board:
    def __init__(self):
        self.grid = self.create_starting_grid()

    def create_starting_grid(self):
        grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        grid[3][3] = WHITE
        grid[3][4] = BLACK
        grid[4][3] = BLACK
        grid[4][4] = WHITE
        return grid

    # --- NEW METHODS BELOW ---

    def is_on_board(self, row, col):
        return 0 <= row < ROWS and 0 <= col < COLS

    def get_flipped_pieces(self, row, col, color):
        flipped_pieces = []
        # 8 directions: (row_change, col_change)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        opponent = WHITE if color == BLACK else BLACK

        for dr, dc in directions:
            r, c = row + dr, col + dc
            temp_flipped = []

            # Keep moving in the direction while we see opponent pieces
            while self.is_on_board(r, c) and self.grid[r][c] == opponent:
                temp_flipped.append((r, c))
                r += dr
                c += dc

            # If we stopped on our own color, the trapped pieces are officially flipped!
            if self.is_on_board(r, c) and self.grid[r][c] == color and temp_flipped:
                flipped_pieces.extend(temp_flipped)

        return flipped_pieces

    def get_valid_moves(self, color):
        # Returns a dictionary where keys are (row, col) and values are a list of pieces to flip
        moves = {}
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == EMPTY:
                    flipped = self.get_flipped_pieces(r, c, color)
                    if flipped:
                        moves[(r, c)] = flipped
        return moves

    def place_piece(self, row, col, color, flipped_pieces):
        # Place the new piece
        self.grid[row][col] = color
        # Flip the trapped pieces
        for r, c in flipped_pieces:
            self.grid[r][c] = color
            
    
    def get_score(self):
        black_score = 0
        white_score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == BLACK:
                    black_score += 1
                elif self.grid[row][col] == WHITE:
                    white_score += 1
        return black_score, white_score