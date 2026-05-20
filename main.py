import pygame
import math
import copy
from constants import WIDTH, HEIGHT, BOARD_HEIGHT, SQUARE_SIZE, BLACK, WHITE
from board import Board
from ui import draw_board, draw_game_over
from ai import minimax, POSITION_WEIGHTS

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello AI - Minimax with Alpha-Beta Pruning")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def get_best_hint(game_board, valid_moves):
    best_move = None
    best_score = -math.inf
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    
    # ==============================================================
    # RULE 1: INSTANT CORNER CAPTURE
    # If a corner is open, take it immediately and skip all math.
    # ==============================================================
    for move in valid_moves.keys():
        if move in corners:
            return move

    safe_moves = {}

    # ==============================================================
    # RULE 2 & 3: THE IRONCLAD DEFENSIVE FILTER
    # Delete negative scores and corner-giving moves.
    # ==============================================================
    for move, flipped_pieces in valid_moves.items():
        r, c = move
        
        # Rule 2: NEVER step on a negative score (Avoid 'X' and 'C' danger squares)
        if POSITION_WEIGHTS[r][c] < 0:
            continue # Skip this move entirely
            
        # Rule 3: NEVER let the AI capture a corner
        temp_board = copy.deepcopy(game_board)
        temp_board.place_piece(r, c, WHITE, flipped_pieces)
        ai_next_moves = temp_board.get_valid_moves(BLACK)
        
        gives_corner = False
        for ai_move in ai_next_moves.keys():
            if ai_move in corners:
                gives_corner = True
                break
                
        # If it passed both strict rules, it is officially a "Safe Move"
        if not gives_corner:
            safe_moves[move] = flipped_pieces

    # ==============================================================
    # FALLBACK SAFETY NET
    # If the AI trapped you and EVERY move breaks a rule, relax the 
    # negative score rule so the hint button doesn't break.
    # ==============================================================
    if len(safe_moves) == 0:
        for move, flipped_pieces in valid_moves.items():
            temp_board = copy.deepcopy(game_board)
            temp_board.place_piece(move[0], move[1], WHITE, flipped_pieces)
            ai_next_moves = temp_board.get_valid_moves(BLACK)
            gives_corner = any(ai_move in corners for ai_move in ai_next_moves.keys())
            
            # Allow negative scores, but STILL refuse to give up corners
            if not gives_corner:
                safe_moves[move] = flipped_pieces

    # If you are completely doomed and have no choice, evaluate everything
    moves_to_evaluate = safe_moves if len(safe_moves) > 0 else valid_moves

    # ==============================================================
    # RULE 4: GRANDMASTER DECISION ON REMAINING SAFE MOVES
    # ==============================================================
    for move, flipped_pieces in moves_to_evaluate.items():
        temp_board = copy.deepcopy(game_board)
        temp_board.place_piece(move[0], move[1], WHITE, flipped_pieces)
        
        score, _ = minimax(temp_board, 4, -math.inf, math.inf, False, BLACK)
        score_for_white = -score 
        
        if score_for_white > best_score:
            best_score = score_for_white
            best_move = move
            
    return best_move

def main():
    run = True
    clock = pygame.time.Clock()
    game_board = Board()
    
    current_turn = BLACK 
    game_started = False  
    active_hint = None   

    while run:
        clock.tick(60) 
        
        # Render frame tracking hint configurations
        draw_board(WIN, game_board, current_turn, game_started, hint_pos=active_hint)

        if game_started:
            black_score, white_score = game_board.get_score()
            empty_squares = game_board.get_empty_count()

            if black_score > white_score and (white_score + empty_squares) < black_score:
                draw_board(WIN, game_board, current_turn, game_started)
                draw_game_over(WIN, black_score, white_score)
                pygame.time.delay(5000)
                run = False
                continue

            if white_score > black_score and (black_score + empty_squares) < white_score:
                draw_board(WIN, game_board, current_turn, game_started)
                draw_game_over(WIN, black_score, white_score)
                pygame.time.delay(5000)
                run = False
                continue

            valid_moves = game_board.get_valid_moves(current_turn)
            
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
                    active_hint = None 

            # --- AI TURN (BLACK) ---
            if current_turn == BLACK and valid_moves:
                # Set 'ai_thinking=True' to print text cleanly underneath the turn block
                draw_board(WIN, game_board, current_turn, game_started, ai_thinking=True)
                pygame.time.delay(600) 

                score, move = minimax(game_board, 1, -math.inf, math.inf, True, BLACK)
                
                if move:
                    pieces_to_flip = valid_moves[move]
                    game_board.place_piece(move[0], move[1], BLACK, pieces_to_flip)
                    
                    # Keep thinking text visible alongside the gold ring highlight placement
                    draw_board(WIN, game_board, current_turn, game_started, highlight_pos=move, ai_thinking=True)
                    pygame.time.delay(1200) 
                    
                    current_turn = WHITE
                    active_hint = None 

        # --- EVENT HANDLING LOOP ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if not game_started:
                    if (WIDTH // 2 - 80 <= pos[0] <= WIDTH // 2 + 80) and (BOARD_HEIGHT + 25 <= pos[1] <= BOARD_HEIGHT + 75):
                        game_started = True
                else:
                    # Check HINT button click coordinates
                    if (WIDTH - 140 <= pos[0] <= WIDTH - 30) and (BOARD_HEIGHT + 25 <= pos[1] <= BOARD_HEIGHT + 65):
                        if current_turn == WHITE and valid_moves:
                            active_hint = get_best_hint(game_board, valid_moves)
                    
                    # Check board space quadrant selection
                    elif pos[1] < BOARD_HEIGHT and current_turn == WHITE:
                        row, col = get_row_col_from_mouse(pos)
                        if (row, col) in valid_moves:
                            pieces_to_flip = valid_moves[(row, col)]
                            game_board.place_piece(row, col, WHITE, pieces_to_flip)
                            current_turn = BLACK
                            active_hint = None 

    pygame.quit()

if __name__ == "__main__":
    main()