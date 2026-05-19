# --- SCREEN & GRID SETTINGS ---
WIDTH = 640
BOARD_HEIGHT = 640
PANEL_HEIGHT = 100
HEIGHT = BOARD_HEIGHT + PANEL_HEIGHT # 740 total height window
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# --- COLORS (RGB) ---
BACKGROUND_GREEN = (34, 139, 34)
PANEL_COLOR = (40, 40, 40)         # Dark charcoal dashboard panel
LINE_COLOR = (0, 0, 0)
BLACK_PIECE = (0, 0, 0)
WHITE_PIECE = (255, 255, 255)
HIGHLIGHT = (255, 215, 0)         # Gold highlight color for indicators
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (30, 144, 255)     # Dodger Blue action button

# --- PIECE REPRESENTATIONS ---
EMPTY = 0
BLACK = 1
WHITE = -1