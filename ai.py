import math
from constants import ROWS, COLS, BLACK, WHITE

# A simple weight matrix for positional strategy
# Corners are high value, squares next to corners are negative
POSITION_WEIGHTS = [
    [ 120, -20,  20,   5,   5,  20, -20, 120],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [  20,  -5,  15,   3,   3,  15,  -5,  20],
    [   5,  -5,   3,   3,   3,   3,  -5,   5],
    [   5,  -5,   3,   3,   3,   3,  -5,   5],
    [  20,  -5,  15,   3,   3,  15,  -5,  20],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [ 120, -20,  20,   5,   5,  20, -20, 120]
]

def evaluate_board(board, color):
    # This function calculates the "score" of the board from the perspective of 'color'
    score = 0
    opponent = WHITE if color == BLACK else BLACK

    for row in range(ROWS):
        for col in range(COLS):
            if board.grid[row][col] == color:
                score += POSITION_WEIGHTS[row][col]
            elif board.grid[row][col] == opponent:
                score -= POSITION_WEIGHTS[row][col]
    
    return score

import copy # We need to simulate moves on fake boards

def minimax(board, depth, alpha, beta, maximizing_player, current_color):
    # Determine the opponent's color
    opponent_color = WHITE if current_color == BLACK else BLACK
    
    valid_moves = board.get_valid_moves(current_color)
    
    # Base Case: We've reached the depth limit OR the game is over (no valid moves)
    if depth == 0 or not valid_moves:
        return evaluate_board(board, BLACK), None # We assume the AI always plays as BLACK for scoring

    best_move = None

    if maximizing_player:
        max_eval = -math.inf
        for move, flipped_pieces in valid_moves.items():
            # Create a copy of the board to simulate the move
            temp_board = copy.deepcopy(board)
            temp_board.place_piece(move[0], move[1], current_color, flipped_pieces)
            
            # Recursively call minimax for the opponent's turn
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, False, opponent_color)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                
            # Alpha-Beta Pruning logic
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break # Prune the tree!
                
        return max_eval, best_move

    else:
        min_eval = math.inf
        for move, flipped_pieces in valid_moves.items():
            temp_board = copy.deepcopy(board)
            temp_board.place_piece(move[0], move[1], current_color, flipped_pieces)
            
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, True, opponent_color)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
                
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
                
        return min_eval, best_move