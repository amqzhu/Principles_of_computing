"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(100)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def score(board):
    """
    Given a board, get score back
    """
    if board.check_win() == provided.PLAYERX:
        return 1
    elif board.check_win() == provided.PLAYERO:
        return -1
    elif board.check_win() == provided.DRAW:
        return 0
    else:
        return None

def make_new_board(old_board, player, move_pos):
    """
    Put player on old board at move_pos to make new board
    """
    board = old_board.clone()
    board.move(move_pos[0], move_pos[1], player)
    return board   

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() is not None:
        return score(board), (-1,-1)
    else:
        all_moves = board.get_empty_squares()
        
        best_score = None
        best_move = (-1,-1)
        
        for move in all_moves:
            new_board = make_new_board(board, player, move)
            new_player = provided.switch_player(player)
            
            current_score = mm_move(new_board, new_player)[0]
                        
            if player == provided.PLAYERX:
                if current_score > best_score or best_score is None:
                    best_score = current_score
                    best_move = move
                if best_score == 1:
                    break
            else:
                if current_score < best_score or best_score is None:
                    best_score = current_score
                    best_move = move
                if best_score == -1:
                    break
                    
        return best_score, best_move
            

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
