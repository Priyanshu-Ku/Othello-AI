# --- SCREEN & GRID SETTINGS ---
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# --- COLORS (RGB) ---
BACKGROUND_GREEN = (34, 139, 34)  # Classic Othello board color
LINE_COLOR = (0, 0, 0)
BLACK_PIECE = (0, 0, 0)
WHITE_PIECE = (255, 255, 255)
HIGHLIGHT = (255, 215, 0)         # Color to show valid AI/Player moves

# --- PIECE REPRESENTATIONS ---
EMPTY = 0
BLACK = 1
WHITE = -1